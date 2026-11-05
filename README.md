# Server dotfiles

Shared shell and CLI configuration for VPS (`ubuntu`) and Tiny (`iam`).
Canonical repository: `git@github.com:ilaumjd/dotfiles-server.git`, branch `master`.
Both machines keep their checkout at `~/dotfiles`.

## Live configuration

The following files are symlinked from the checkout into the home directory:

- `.bashrc`, `.bash_aliases`, `.profile`, `.pam_environment`
- `.config/mise/config.toml`
- `.config/nvim/init.lua`, `.config/tmux/tmux.conf`
- `.config/git/config`, `.config/git/ignore`
- `.config/bat/config`, `.config/atuin/config.toml`

Edit tracked files, commit and push, then run `git -C ~/dotfiles pull --ff-only`
on the other server. Open a new shell to load shell changes. Tool installation
is separate: run `mise install` when ready to install the configured tools.
Some applications replace symlinks when saving; check links after such edits.

## Machine-specific files

SSH keys, SSH configuration, tokens, and services stay outside this repository.
`.config/mise/github_tokens.toml` is ignored and must never be committed.
Git credential helpers belong in `~/.gitconfig.local`, included by the shared
Git configuration. Preserve each machine's existing helper settings there.

The PAM mise path uses `@{HOME}` so it resolves for both server users. Whether
PAM loads this file depends on the host's PAM policy. Interactive mise activation
and `~/.local/bin` setup are also configured by the shell files.

Both servers default to the rootful Podman socket. The optional Herdr shell hook
loads only when `~/.config/maki/herdr-shell.bash` exists.

## Pi and Maki

Pi and Maki share configuration across both servers. Mise manages their tool
versions independently; the configuration sync does not install or pin tools
or Pi packages. To apply after pulling:

```sh
python3 ~/dotfiles/scripts/setup-agents.py
```

The script backs up replaced configuration files before linking them. Pi uses the
shared `~/.pi/agent/settings.json` and Herdr extension. Maki uses the shared
`~/.config/maki` Lua configuration, permission rules, manifest, and shell hook.
Maki defaults to Opus with the Rose Pine Moon theme; Pi keeps Tiny's existing
model selection and thinking settings.

Provider credentials remain host-local: Pi's `~/.pi/agent/auth.json` and Maki's
`~/.local/state/maki/auth/` are never tracked. Sessions, model catalogs, npm
dependencies, Telegram bot configuration, and caches also remain local.
After an application saves settings, check `git -C ~/dotfiles diff` and rerun
the script if it replaced a configuration symlink. Commit intentional changes,
push, and pull on the other server to share them.
