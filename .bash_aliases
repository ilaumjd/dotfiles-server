### .bash_aliases

# aliases
alias cd='z'
alias ld='lazydocker'
alias lg='lazygit'

# carapace
export CARAPACE_BRIDGES='zsh,fish,bash,inshellisense'
source <(carapace _carapace)

# fzf
export FZF_DEFAULT_OPTS='--height 10 --border'
eval "$(fzf --bash)"

# zoxide
eval "$(zoxide init bash)"

# atuin
eval "$(atuin init bash --disable-up-arrow)"
