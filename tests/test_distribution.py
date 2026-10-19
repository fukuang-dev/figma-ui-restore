import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def run(*args):
    return subprocess.run([sys.executable, str(ROOT / 'scripts/install.py'), *map(str, args)],
                          capture_output=True, text=True)


class InstallationTests(unittest.TestCase):
    def test_install_in_project_with_spaces_and_refuse_overwrite(self):
        with tempfile.TemporaryDirectory(prefix='restore project ') as folder:
            project = Path(folder)
            self.assertEqual(run('--project', project).returncode, 0)
            installed = project / '.agents/skills/figma-ui-restore'
            source = ROOT / 'skills/figma-ui-restore'
            for file in source.rglob('*'):
                if file.is_file():
                    self.assertEqual(file.read_bytes(), (installed / file.relative_to(source)).read_bytes())
            marker = installed / 'local-note.md'
            marker.write_text('Preserve my local changes.')
            self.assertNotEqual(run('--project', project).returncode, 0)
            self.assertEqual(marker.read_text(), 'Preserve my local changes.')

    def test_dry_run_does_not_create_configuration(self):
        with tempfile.TemporaryDirectory() as folder:
            self.assertEqual(run('--project', folder, '--dry-run').returncode, 0)
            self.assertEqual(list(Path(folder).iterdir()), [])

    def test_reject_missing_project(self):
        with tempfile.TemporaryDirectory() as folder:
            self.assertNotEqual(run('--project', Path(folder) / 'missing').returncode, 0)
            self.assertEqual(list(Path(folder).iterdir()), [])

    @unittest.skipIf(sys.platform == 'win32', 'Symlink creation requires additional Windows privileges')
    def test_refuse_redirected_project_destination(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            project = root / 'project'
            outside = root / 'outside'
            project.mkdir()
            outside.mkdir()
            (project / '.agents').symlink_to(outside, target_is_directory=True)
            self.assertNotEqual(run('--project', project).returncode, 0)
            self.assertEqual(list(outside.iterdir()), [])

    def test_user_install_is_tested_with_mock_home_only(self):
        spec = importlib.util.spec_from_file_location('restore_installer', ROOT / 'scripts/install.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as folder:
            destination = module.install(Path(folder) / '.agents/skills')
            self.assertTrue((destination / 'SKILL.md').is_file())


class PackageTests(unittest.TestCase):
    def test_release_excludes_local_evidence_and_can_install(self):
        result = subprocess.run([sys.executable, str(ROOT / 'scripts/package.py')], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        archive = Path(result.stdout.strip().splitlines()[-1])
        with zipfile.ZipFile(archive) as package, tempfile.TemporaryDirectory() as folder:
            names = package.namelist()
            self.assertTrue(any(name.endswith('/skills/figma-ui-restore/SKILL.md') for name in names))
            self.assertFalse(any(any(part in {'.git', 'outputs', 'dist', '__pycache__'} for part in Path(name).parts) for name in names))
            package.extractall(folder)
            unpacked = next(Path(folder).iterdir())
            project = Path(folder) / 'destination'
            project.mkdir()
            installed = subprocess.run([sys.executable, str(unpacked / 'scripts/install.py'), '--project', str(project)],
                                       capture_output=True, text=True)
            self.assertEqual(installed.returncode, 0, installed.stderr)


if __name__ == '__main__':
    unittest.main()
