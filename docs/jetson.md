# Nvidia Jetson AGX Xavier

## Ubuntu Version
```sh
$ cat /etc/lsb-release
```
## L4T Version
```sh
$ cat /etc/nv_tegra_release
```
## Kernel Version
```sh
$ uname -a
```
## CPU Information
```sh
$ lscpu
```

## Hardware Information
```sh
$ sudo lshw
```
## Disk Usage
```sh
$ df -h
```

## Running Processes
```sh
$ top
```
## List USB Devices
```sh
$ lsusb
```
## USB Devices
List the USB devices and associated drivers.
```sh
$ usb-devices
```
## Force Recovery Mode
Place the Jetson into Force Recovery Mode
```sh
$ sudo reboot –-force forced-recovery
```

## dmesg
dmesg prints the kernel message buffer. The messages typically consist of messages produced by device drivers. Useful when working with new hardware, e.g. USB devices. On newer installations (Newer Ubuntu 14.04, Ubuntu 16.04), you can monitor the dmesg buffer:
```sh
$ sudo dmesg –follow
```
## Xorg
Xorg is the Ubuntu display server. You can monitor the Xorg log in real time:
```sh
$ sudo tail -f /var/log/Xorg.0.log
```
## List Partitions
```sh
sudo gdisk -l /dev/mmcblk0
```
## Serial USB devices
From: https://unix.stackexchange.com/questions/144029/command-to-determine-ports-of-a-device-like-dev-ttyusb0

Below is a quick and dirty bash script which walks through devices in /sys looking for USB devices with a ID_SERIAL attribute. Typically only real USB devices will have this attribute, and so we can filter with it. If we don’t, you’ll see a lot of things in the list that aren’t physical devices.
```sh
#!/bin/bash

for sysdevpath in $(find /sys/bus/usb/devices/usb*/ -name dev); do
(
syspath=”${sysdevpath%/dev}”
devname=”$(udevadm info -q name -p $syspath)”
[[ “$devname” == “bus/”* ]] && continue
eval “$(udevadm info -q property –export -p $syspath)”
[[ -z “$ID_SERIAL” ]] && continue
echo “/dev/$devname – $ID_SERIAL”
)
done
```

https://docs.nvidia.com/jetson/jetpack/install-jetpack/index.html#sd-card-image

https://docs.nvidia.com/sdk-manager/docker-containers/index.html

https://docs.nvidia.com/jetson/archives/l4t-archived/l4t-3261/index.html#page/Tegra%20Linux%20Driver%20Package%20Development%20Guide/updating_jetson_and_host.html#

https://docs.nvidia.com/jetson/archives/r35.3.1/DeveloperGuide/text/SD/FlashingSupport.html#flashing-to-an-sd-card

