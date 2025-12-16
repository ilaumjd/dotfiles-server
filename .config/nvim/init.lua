-- Minimal Neovim config for VPS (no plugins)

-- Leader key
vim.g.mapleader = " "
vim.g.maplocalleader = " "

-- Options
local opt = vim.opt

opt.number = true
opt.relativenumber = false
opt.signcolumn = "yes"
opt.cursorline = true

opt.expandtab = true
opt.shiftwidth = 2
opt.tabstop = 2
opt.smartindent = true

opt.wrap = false
opt.linebreak = true
opt.scrolloff = 5
opt.sidescrolloff = 8

opt.ignorecase = true
opt.smartcase = true

opt.splitbelow = true
opt.splitright = true

opt.clipboard = "unnamedplus"
opt.mouse = "a"
opt.undofile = true
opt.termguicolors = true
opt.timeoutlen = 300

opt.completeopt = "menu,menuone,noselect"

-- Keymaps
local map = vim.keymap.set

-- Delete without yanking
map("n", "x", '"_x', { desc = "Delete char without yank" })

-- Better window navigation
map("n", "<C-h>", "<C-w>h", { desc = "Go to left window" })
map("n", "<C-j>", "<C-w>j", { desc = "Go to lower window" })
map("n", "<C-k>", "<C-w>k", { desc = "Go to upper window" })
map("n", "<C-l>", "<C-w>l", { desc = "Go to right window" })

-- Visual mode: move lines
map("x", "J", ":move '>+1<CR>gv=gv", { desc = "Move selection down" })
map("x", "K", ":move '<-2<CR>gv=gv", { desc = "Move selection up" })

-- Visual mode: better indenting
map("x", "H", "<gv", { desc = "Indent left" })
map("x", "L", ">gv", { desc = "Indent right" })

-- Exit insert mode
map("i", "jk", "<Esc>", { desc = "Exit insert mode" })

-- Clear search highlight
map("n", "<Esc>", "<cmd>nohlsearch<CR>", { desc = "Clear search highlight" })

-- File explorer
map("n", "-", "<cmd>Explore<CR>", { desc = "File explorer" })

-- Save file
map("n", "<Leader>w", "<cmd>w<CR>", { desc = "Save file" })

-- Quit
map("n", "<Leader>q", "<cmd>q<CR>", { desc = "Quit" })

-- Buffer navigation
map("n", "<S-h>", "<cmd>bprevious<CR>", { desc = "Prev buffer" })
map("n", "<S-l>", "<cmd>bnext<CR>", { desc = "Next buffer" })

-- Disable macro recording (toggle with <Leader>uq)
vim.cmd "map q <Nop>"

map("n", "<Leader>uq", function()
  vim.g._macro_enabled = not vim.g._macro_enabled
  if vim.g._macro_enabled then
    vim.cmd "unmap q"
    vim.notify "Macro recording enabled"
  else
    vim.cmd "map q <Nop>"
    vim.notify "Macro recording disabled"
  end
end, { desc = "Toggle macro recording" })

-- Highlight on yank
vim.api.nvim_create_autocmd("TextYankPost", {
  callback = function()
    vim.highlight.on_yank({ timeout = 200 })
  end,
})

-- Colorscheme (built-in)
vim.cmd.colorscheme("slate")
