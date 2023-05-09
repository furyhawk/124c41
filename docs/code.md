# code

## install vscode
```sh
git clone https://AUR.archlinux.org/visual-studio-code-bin.git
cd visual-studio-code-bin
makepkg -s
sudo pacman -U *code-bin-*.pkg.tar.zst
cd ../ && sudo rm -rfv visual-studio-code-bin/
```