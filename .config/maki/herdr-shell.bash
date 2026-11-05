maki() (
    trap 'printf "\033]7501;state=clear\033\\"' EXIT
    command maki "$@"
)
