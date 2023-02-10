# test

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