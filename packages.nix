let
  nixpkgs = fetchTarball {
    url = "https://github.com/NixOS/nixpkgs/archive/nixos-25.11.tar.gz";
  };
  pkgs = import nixpkgs {};
in
pkgs.buildEnv {
  name = "user-packages";
  paths = with pkgs; [
    atuin
    bat
    btop
    carapace
    curl
    delta
    fastfetch
    fd
    fzf
    git
    htop
    jq
    lazydocker
    lazygit
    neovim
    patch
    ripgrep
    screen
    sqlite
    stow
    tmux
    vim
    zoxide
  ];
}

