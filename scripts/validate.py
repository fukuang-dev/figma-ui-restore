#!/usr/bin/env python3
"""Validate this package's metadata, references and redistributable file set."""
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
IGNORED = {'.git', '__pycache__', 'dist', 'outputs', '.venv'}


def package_files(root=ROOT):
    return sorted(p for p in root.rglob('*') if p.is_file() and not any(
        part in IGNORED for part in p.relative_to(root).parts))


def validate():
    manifest = json.loads((ROOT / 'plugin.json').read_text(encoding='utf-8'))
    assert manifest['name'] == 'figma-ui-restore'
    assert re.fullmatch(r'\d+\.\d+\.\d+', manifest['version'])
    assert manifest['license'] == 'MIT'
    marketplace = json.loads((ROOT / '.agents/plugins/marketplace.json').read_text(encoding='utf-8'))
    entry = marketplace['plugins'][0]
    assert entry['name'] == manifest['name']
    assert (ROOT / entry['source']['path']).resolve() == ROOT
    assert entry['policy']['installation'] == 'AVAILABLE'
    assert entry['policy']['authentication'] in {'ON_USE', 'ON_INSTALL'}

    skill = ROOT / 'skills' / manifest['name']
    text = (skill / 'SKILL.md').read_text(encoding='utf-8')
    # This package deliberately uses a tiny YAML subset; not a general YAML parser.
    frontmatter = re.match(r'\A---\nname: ([a-z0-9-]+)\ndescription: ("[^\n]*")\n---\n', text)
    assert frontmatter, 'Invalid skill frontmatter for this package'
    assert frontmatter[1] == manifest['name']
    description = json.loads(frontmatter[2])
    assert 0 < len(description) <= 1024
    assert not re.search(r'^\s*\[TODO:', text, re.M)
    yaml = (skill / 'agents/openai.yaml').read_text(encoding='utf-8')
    fields = dict((key, json.loads(value)) for key, value in re.findall(r'^  (\w+): (".*")$', yaml, re.M))
    assert {'display_name', 'short_description', 'default_prompt'} <= fields.keys()
    assert 25 <= len(fields['short_description']) <= 64
    assert '$figma-ui-restore' in fields['default_prompt']

    count = 0
    files = package_files()
    assert files
    for file in files:
        assert not file.is_symlink(), f'Symlink cannot be packaged: {file}'
        relative = file.relative_to(ROOT)
        assert not any(part.startswith('.env') for part in relative.parts), relative
        if file.suffix in {'.md', '.json', '.yaml', '.py', '.html', '.css', '.js', '.svg'}:
            content = file.read_text(encoding='utf-8')
            # Patterns are built here so the validator's own source is distributable.
            forbidden = ['Jillion' + 'Pay', 'jillion' + 'tech', '/Users' + '/', 'BEGIN ' + 'OPENSSH PRIVATE KEY']
            assert not any(value.lower() in content.lower() for value in forbidden), f'Private source leaked: {relative}'
        if file.suffix != '.md':
            continue
        for link in re.findall(r'!?\[[^\]]*\]\(([^)\s]+)\)', file.read_text(encoding='utf-8')):
            if re.match(r'[a-zA-Z][a-zA-Z0-9+.-]*:', link) or link.startswith('#'):
                continue
            destination = (file.parent / link.split('#')[0]).resolve()
            assert destination.is_relative_to(ROOT) and destination.exists(), f'Broken local link: {relative}: {link}'
            count += 1
    assert all((ROOT / file).is_file() for file in ['README.md', 'README.en.md', 'LICENSE', 'CHANGELOG.md'])
    print(f'PASS: metadata, {count} local Markdown links, and {len(files)} distributable files')
    return manifest


if __name__ == '__main__':
    validate()
