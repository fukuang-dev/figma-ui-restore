#!/usr/bin/env python3
"""Create a release ZIP from the validated source, without local evidence or Git data."""
from pathlib import Path
import zipfile
from validate import ROOT, package_files, validate


def build():
    manifest = validate()
    name = f"figma-ui-restore-{manifest['version']}"
    destination = ROOT / 'dist' / f'{name}.zip'
    destination.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(destination, 'w', zipfile.ZIP_DEFLATED) as archive:
        for file in package_files():
            info = zipfile.ZipInfo((Path(name) / file.relative_to(ROOT)).as_posix(), date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, file.read_bytes())
    print(destination)
    return destination


if __name__ == '__main__':
    build()
