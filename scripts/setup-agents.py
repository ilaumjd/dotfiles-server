#!/usr/bin/env python3
"""Link shared Pi and Maki configuration without installing tools or packages."""

import argparse
from pathlib import Path
import shutil
import tempfile

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
    parser.parse_args()
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


if __name__ == '__main__':
    main()
