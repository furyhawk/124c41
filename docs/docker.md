# Docker

```sh
systemctl --user start docker-desktop
sudo groupadd docker
sudo usermod -aG docker $USER
groups ${USER}
```

```sh
curl -fsSL test.docker.com -o get-docker.sh && sh get-docker.sh
sudo apt-get install libffi-dev libssl-dev
sudo apt install python3-dev
sudo apt-get install -y python3 python3-pip
pip install "cython<3.0.0" wheel
pip install "pyyaml==5.4.1" --no-build-isolation
pip install docker-compose
sudo systemctl enable docker
```

```sh
sudo apt-get purge docker-ce
sudo apt-get purge docker-ce-cli
sudo rm -rf /var/lib/docker
```

