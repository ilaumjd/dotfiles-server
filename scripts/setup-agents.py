#!/usr/bin/env python3
"""Link shared agent configuration; optionally install tools and Pi packages."""

import argparse
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
        mise = shutil.which('mise') or str(home / '.local/bin/mise')
        tools = tomllib.loads((repo / '.config/mise/config.toml').read_text())['tools']
        versions = [f'pi@{tools["pi"]}',
                    f'github:tontinton/maki@{tools["github:tontinton/maki"]}']
        subprocess.run([mise, 'install', *versions], cwd=repo, check=True)
        subprocess.run([mise, 'reshim'], cwd=repo, check=True)
        # Only reconcile extensions; do not update the pinned Pi executable.
        subprocess.run([mise, 'exec', '--', 'pi', 'update', '--extensions'],
                       cwd=home, env={**os.environ, 'CI': '1'}, check=True)


if __name__ == '__main__':
    main()
