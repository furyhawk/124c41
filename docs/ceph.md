# Manual install of a Ceph Cluster.

### Fetching software.

First of I want to check that I have all the latest packages in my debian system.
```
apt update
apt upgrade
```

Next we fetch the keys and ceph packages, in this case we download the pacific packages for buster.
```
wget -q -O- 'https://download.ceph.com/keys/release.asc' | sudo apt-key add -
echo deb https://download.ceph.com/debian-pacific/ buster main | sudo tee /etc/apt/sources.list.d/ceph.list
apt update
apt install ceph ceph-common
```

Last we need to download the smartmontools for our nodes. This is so we can monitor our hard drives for hardware issues.
```
echo deb http://deb.debian.org/debian buster-backports main >> /etc/apt/sources.list
apt update
apt install smartmontools/buster-backports
```

A reboot when you have installed packages is always a good thing and if you need to do some extra hardware changes this is a good place to do so.
```
shutdown -r now
```

### Configure node 1

First we will create a ceph configuration file.
```
sudo vi /etc/ceph/ceph.conf
```

The most important things to specify is the id and ips of your cluster monitors. A unique cluster id that you will reuse for all your nodes. And lastly a public network range that you want your monitors to be available over. The cluster network is a good addition if you have the resources to route the recovery traffic on a backbone network.
```
[global]
fsid = {cluster uuid}
mon initial members = {id1}, {id2}, {id2}
mon host = {ip1}, {ip2}, {ip3}
public network = {network range for your public network}
cluster network = {network range for your cluster network}
auth cluster required = cephx
auth service required = cephx
auth client required = cephx
```

Next we create keys for admin, monitors and boostrapping our drives. These keys will then be merged with the monitor key so the initial setup will have the keys used for other operations.
```
sudo ceph-authtool --create-keyring /tmp/monkey --gen-key -n mon. --cap mon 'allow *'
sudo ceph-authtool --create-keyring /etc/ceph/ceph.client.admin.keyring --gen-key -n client.admin --cap mon 'allow *' --cap osd 'allow *' --cap mds 'allow *' --cap mgr 'allow *'
sudo ceph-authtool --create-keyring /var/lib/ceph/bootstrap-osd/ceph.keyring --gen-key -n client.bootstrap-osd --cap mon 'profile bootstrap-osd'
sudo ceph-authtool /tmp/monkey --import-keyring /etc/ceph/ceph.client.admin.keyring
sudo ceph-authtool /tmp/monkey --import-keyring /var/lib/ceph/bootstrap-osd/ceph.keyring
```

Make the monitor key available to the ceph user so we don't get an permission error when we start our services.
```
sudo chown ceph:ceph /tmp/monkey
```

Next up we create a monitor map so the monitors will know of each other. The monitors keeps track on other resources but for high availability the monitors needs to know who is in charge.
```
monmaptool --create --add {node1-id} {node1-ip} --fsid {cluster uuid} /tmp/monmap
monmaptool --add {node2-id} {node2-ip} --fsid {cluster uuid} /tmp/monmap
monmaptool --add {node3-id} {node3-ip} --fsid {cluster uuid} /tmp/monmap
```

Starting a new monitor is as easy as creating a new directory, creating the filesystem for and starting the service.
```
sudo -u ceph mkdir /var/lib/ceph/mon/ceph-{node1-id}
sudo -u ceph ceph-mon --mkfs -i {node1-id} --monmap /tmp/monmap --keyring /tmp/monkey
sudo systemctl start ceph-mon@{node1-id}
```

Next up we need a manager so we could configure and monitor our cluster through a visual dashboard. First we create a new key, put that key in a newly created directory and start the service. Enabling a dashboard is as easy as running the command for enabling, creating / assigning a certificate and creating a new admin user.
```
sudo ceph auth get-or-create mgr.{node1-id} mon 'allow profile mgr' osd 'allow *' mds 'allow *'
sudo -u ceph mkdir /var/lib/ceph/mgr/ceph-{node1-id}
sudo -u ceph vi /var/lib/ceph/mgr/ceph-{node1-id}/keyring
sudo systemctl start ceph-mgr@{node1-id}
sudo ceph mgr module enable dashboard
sudo ceph dashboard create-self-signed-cert
sudo ceph dashboard ac-user-create admin -i passwd administrator
```

### Setting up more nodes.

First of we need to copy over the configuration, monitor map and all the keys over to our new host.
```
sudo scp {user}@{server}:/etc/ceph/ceph.conf /etc/ceph/ceph.conf
sudo scp {user}@{server}:/etc/ceph/ceph.client.admin.keyring /etc/ceph/ceph.client.admin.keyring
sudo scp {user}@{server}:/var/lib/ceph/bootstrap-osd/ceph.keyring /var/lib/ceph/bootstrap-osd/ceph.keyring
sudo scp {user}@{server}:/tmp/monmap /tmp/monmap
sudo scp {user}@{server}:/tmp/monkey /tmp/monkey
```

Next up we setup the monitor node exactly as we did with the first node.
```
sudo -u ceph mkdir /var/lib/ceph/mon/ceph-{node2-id}
sudo -u ceph ceph-mon --mkfs -i {node2-id} --monmap /tmp/monmap --keyring /tmp/monkey
sudo systemctl start ceph-mon@{node2-id}
sudo ceph -s
sudo ceph mon enable-msgr2
```

Then we setup the manager node exactly as we did with the first node.
```
sudo ceph auth get-or-create mgr.{node2-id} mon 'allow profile mgr' osd 'allow *' mds 'allow *'
sudo -u ceph mkdir /var/lib/ceph/mgr/ceph-{node2-id}
sudo -u ceph vi /var/lib/ceph/mgr/ceph-{node2-id}/keyring
sudo systemctl start ceph-mgr@{node2-id}
```

### Adding storage

When the cluster is up and running and all monitors are in qourum you could add storage services. This is easily done via the volume command. First prepare a disk so it will be known by the cluster and have the keys and configuration copied to the management directory. Next up you activate the service so your storage nodes will be ready to use. This will be done for all the harddrives you want to add to your network.
```
sudo ceph-volume lvm prepare --data /dev/sdb 
sudo ceph-volume lvm activate {osd-number} {osd-uuid}
```

### Post configuration

Last but not least you want to ensure that all the services starts after a reboot. In debian you do that by enabling the services.
```
sudo systemctl enable ceph-mon@{node-id}
sudo systemctl enable ceph-mgr@{node-id}
sudo systemctl enable ceph-osd@{osd-number}
```
