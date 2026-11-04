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
