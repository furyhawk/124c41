# linux

## misc
```shell
ln -s original symlink
```

## test

```shell
bash ./scripts/linter.sh

bash ./scripts/check_type.sh
```

## docker

[Run the Docker daemon as a non-root user (Rootless mode) | Docker Documentation](https://docs.docker.com/engine/security/rootless/)

[Docker+Wasm (Beta) | Docker Documentation](https://docs.docker.com/desktop/wasm/)

## brew
```sh
brew upgrade --cask --greedy
```

## QEMU
stty cols 120 rows 80

## DockSTARTer
```sh
sudo pacman -Sy curl docker git
bash -c "$(curl -fsSL https://get.dockstarter.com)"
sudo reboot
ds
```

```sh
useradd -m archie
passwd archie
```

## Enabling sudo
After installing and logging in, you will find that the default user does not have sudo privileges. Open a terminal and use the following commands to enable it.

```sh
set USERNAME=`whoami`
su -p
# /usr/sbin/usermod -aG sudo $USERNAME
```

https://wiki.archlinux.org/title/sudo
## sway

```sh
export WLR_NO_HARDWARE_CURSORS=1

pacman -S spice-vdagent
set $menu bemenu-run --no-exec | xargs swaymsg exec --
```


```sh
sudo apt-get install ubuntu-desktop
sudo systemctl set-default graphical.target
```

## WSL time not updated
```sh
apt-get -o Acquire::Check-Valid-Until=false -o Acquire::Check-Date=false update
```

## find largest file in directory recursively using find
```sh
sudo du -a / | sort -n -r | head -n 20
```

## edge

```sh
sudo add-apt-repository "deb [arch=amd64] https://packages.microsoft.com/repos/edge stable main"
sudo apt update
sudo apt install microsoft-edge-stable
```

## zsh

```sh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

autoload predict-on
predict-on

```


```sh
uname -a
netstat -ltup
```