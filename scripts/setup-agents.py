#!/usr/bin/env python3
"""Link shared agent configuration; optionally install tools and Pi packages."""

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import tomllib

FILES = (
    '.pi/agent/settings.json',
    '.pi/agent/extensions/herdr-agent-state.ts',
    '.config/maki/init.lua',
    '.config/maki/plugin.toml',
    '.config/maki/permissions.toml',
    '.config/maki/herdr-shell.bash',
    '.config/maki/lua/herdr_status.lua',
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--install', action='store_true',
                        help='Install pinned Pi/Maki versions and configured Pi packages')
    args = parser.parse_args()
    repo = Path(__file__).resolve().parent.parent
    home = Path.home()
    backup = None
    for name in FILES:
        source, target = repo / name, home / name
        if not source.is_file():
            raise FileNotFoundError(source)
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists() and target.resolve() == source.resolve():
            continue
        if target.exists() or target.is_symlink():
            if backup is None:
                backup_root = home / '.local/state/dotfiles-backups'
                backup_root.mkdir(parents=True, exist_ok=True)
                backup = Path(tempfile.mkdtemp(prefix='agents-', dir=backup_root))
            saved = backup / name
            saved.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(target, saved, follow_symlinks=False)
            target.unlink()
        target.symlink_to(source)
    print(f'Linked {len(FILES)} agent configuration files.')
    if backup:
        print(f'Previous files saved in {backup}')
    if args.install:
        local_mise = home / '.local/bin/mise'
        # A Snap command in /snap/bin is a launcher; use its actual executable.
        snap_mise = Path('/snap/mise/current/bin/mise')
        mise = (str(snap_mise) if snap_mise.is_file() else
                str(local_mise) if local_mise.is_file() else shutil.which('mise'))
        if not mise:
            raise FileNotFoundError('Install mise before running --install')
        tools = tomllib.loads((repo / '.config/mise/config.toml').read_text())['tools']
        pi_tool = f'github:earendil-works/pi@{tools["github:earendil-works/pi"]}'
        versions = [pi_tool,
                    f'github:tontinton/maki@{tools["github:tontinton/maki"]}']
        subprocess.run([mise, 'install', *versions], cwd=repo, check=True)
        subprocess.run([mise, 'reshim'], cwd=repo, check=True)
        # Snap's launcher cannot dispatch shims named after another executable.
        # Use the native mise executable for these two command shims.
        native_mise = Path(mise)
        for command in ('pi', 'maki'):
            shim = home / '.local/share/mise/shims' / command
            if shim.is_symlink():
                shim.unlink()
            if not shim.exists():
                shim.symlink_to(native_mise)
        # Invoke the installed executable directly: `mise exec` may install every
        # missing global tool or pick an unrelated `pi` from the system PATH.
        pi_root = Path(subprocess.check_output([mise, 'where', pi_tool], text=True).strip())
        pi = next(p for p in [pi_root / 'pi', pi_root / 'pi/pi'] if p.is_file())
        node_root = Path(subprocess.check_output(
            [mise, 'where', f'node@{tools["node"]}'], text=True).strip())
        env = {**os.environ, 'CI': '1',
               'PATH': str(node_root / 'bin') + os.pathsep + os.environ.get('PATH', '')}
        packages = json.loads((repo / '.pi/agent/settings.json').read_text())['packages']
        for package in packages:
            name, version = package.removeprefix('npm:').rsplit('@', 1)
            installed = home / '.pi/agent/npm/node_modules' / name / 'package.json'
            if installed.is_file() and json.loads(installed.read_text())['version'] == version:
                print(f'Already installed: {package}')
                continue
            subprocess.run([str(pi), 'install', package],
                           cwd=home, env=env, check=True)


if __name__ == '__main__':
    main()
