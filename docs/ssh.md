# ssh

```sh
sudo pacman -S openssh
sudo systemctl enable --now sshd
```

If the username on your local machine matches the one on the server you are trying to connect to, you can just type: ssh host_ip_address And hit Enter.
```sh
ssh your_username@host_ip_address
```

To open SSH port on Manjaro, you can follow these steps 1:

Make sure sshd (ssh daemon) is active and listening to incoming connections on the computer you are trying to access: systemctl status sshd If it’s inactive, start it using: systemctl start sshd To automatically start it on boot: systemctl enable sshd

Also allow incoming connections in your firewall.

$ ssh-keygen -t rsa -b 2048
Generating public/private rsa key pair.
Enter file in which to save the key (/home/username/.ssh/id_rsa):
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in /home/username/.ssh/id_rsa.
Your public key has been saved in /home/username/.ssh/id_rsa.pub.

$ ssh-copy-id id@server
id@server's password: