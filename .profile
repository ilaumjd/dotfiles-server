# ~/.profile: executed by the command interpreter for login shells.
# This file is not read by bash(1), if ~/.bash_profile or ~/.bash_login
# exists.
# see /usr/share/doc/bash/examples/startup-files for examples.
# the files are located in the bash-doc package.

# if running bash
if [ -n "$BASH_VERSION" ]; then
    if [ -f "$HOME/.bashrc" ]; then
	. "$HOME/.bashrc"
    fi
fi

# PATH: user's private bin
if [ -d "$HOME/bin" ] ; then
    PATH="$HOME/bin:$PATH"
fi

# mise shims — on PATH for login shells (covers non-interactive SSH like "ssh host command").
# Interactive shells get mise via .bashrc -> mise activate.
export PATH="$HOME/.local/share/mise/shims:$PATH"

export MACHINE_NAME=tencent
