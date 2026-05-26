### .bash_aliases

alias cd='z'
alias ld='lazydocker'
alias lg='lazygit'

# ========== tmux helpers ==========
alias ta='tmux attach'
alias tls='tmux list-sessions'

th() {
  local session_name
  session_name=$(basename "$PWD")
  if tmux has-session -t "$session_name" 2>/dev/null; then
    tmux attach-session -t "$session_name"
  else
    tmux new-session -s "$session_name"
  fi
}

tks() {
  if ! command -v fzf &>/dev/null; then
    echo "fzf not installed. Sessions:"
    tmux list-sessions
    return 1
  fi
  local sel session_name
  sel=$(tmux list-sessions | fzf --prompt='Kill session> ') || return
  session_name=$(echo "$sel" | cut -d':' -f1)
  tmux kill-session -t "$session_name"
}
