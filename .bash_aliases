### .bash_aliases

# carapace
export CARAPACE_BRIDGES='zsh,fish,bash,inshellisense'
source <(carapace _carapace)

# fzf
export FZF_DEFAULT_OPTS='--height 10 --border'
eval "$(fzf --bash)"

# lazygit
alias lg='lazygit'

# zoxide
alias cd='z'
eval "$(zoxide init bash)"

# atuin
eval "$(atuin init bash --disable-up-arrow)"
