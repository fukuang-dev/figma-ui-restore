#!/usr/bin/env python3
"""Install only the skill, using the Python standard library. Never overwrite."""
import argparse
from pathlib import Path
import shutil
import tempfile

SOURCE = Path(__file__).resolve().parents[1] / 'skills' / 'figma-ui-restore'


def install(parent: Path, dry_run: bool = False) -> Path:
    # System aliases such as macOS /var -> /private/var are legitimate. Only
    # refuse redirects inside the selected project/home skill containers.
    for part in [parent, parent.parent]:
        if part.is_symlink():
            raise ValueError(f'Refusing a symlinked destination: {part}')
    destination = parent / SOURCE.name
    if destination.exists() or destination.is_symlink():
        raise ValueError(f'Already exists: {destination}. Back up and remove the old installation first.')
    if not (SOURCE / 'SKILL.md').is_file():
        raise ValueError('Run the installer from a complete checkout or release archive.')
    if any(p.is_symlink() for p in SOURCE.rglob('*')):
        raise ValueError('Refusing a skill source containing symlinks.')
    if dry_run:
        print(f'Would install: {SOURCE} -> {destination}')
        return destination
    parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.figma-ui-restore-', dir=parent) as temporary:
        staged = Path(temporary) / SOURCE.name
        shutil.copytree(SOURCE, staged)
        if destination.exists() or destination.is_symlink():
            raise ValueError(f'Destination appeared during installation: {destination}')
        staged.rename(destination)
    print(f'Installed: {destination}')
    print('Open your target project and invoke $figma-ui-restore. Restart Codex if it is not discovered.')
    return destination


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    scope = parser.add_mutually_exclusive_group(required=True)
    scope.add_argument('--project', type=Path, help='Existing project root; installs into .agents/skills/')
    scope.add_argument('--user', action='store_true', help='Install into ~/.agents/skills/')
    parser.add_argument('--dry-run', action='store_true', help='Print the destination without creating files')
    args = parser.parse_args()
    try:
        if args.project is not None:
            root = args.project.expanduser().absolute()
            if not root.is_dir():
                raise ValueError(f'Project root does not exist: {root}')
            parent = root / '.agents' / 'skills'
        else:
            parent = Path.home() / '.agents' / 'skills'
        install(parent, args.dry_run)
    except (ValueError, OSError) as error:
        parser.exit(1, f'Installation failed: {error}\n')


if __name__ == '__main__':
    main()
