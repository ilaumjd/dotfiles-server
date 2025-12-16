### .bash_aliases

# fzf
export FZF_DEFAULT_OPTS='--height 10 --border'
eval "$(fzf --bash)"

# lazygit
alias lg='lazygit'

# zoxide
alias cd='z'
eval "$(zoxide init bash)"
