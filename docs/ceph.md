# Manual install of a Ceph Cluster.

## Daemon container

This Dockerfile may be used to bootstrap a Ceph cluster with all the Ceph daemons running. To run a certain type of daemon, simply use the name of the daemon as `$1`. Valid values are:

- `mon` deploys a Ceph monitor
- `osd` deploys an OSD using the method specified by `OSD_TYPE`
- `osd_directory` deploys **one or multiple OSDs in a single container** using a prepared directory (used in scenario where the operator doesn't want to use `--privileged=true`)
- `osd_directory_single` deploys an **single OSD per container** using a prepared directory (used in scenario where the operator doesn't want to use `--privileged=true`)
- `osd_ceph_disk` deploys an OSD using ceph-disk, so you have to provide a whole device (ie: /dev/sdb)
- `mds` deploys a MDS
- `rgw` deploys a Rados Gateway

## Usage

You can use this container to bootstrap any Ceph daemon.

- `CLUSTER` is the name of the cluster (DEFAULT: ceph)

## SELinux

If SELinux is enabled, run the following commands:

```
sudo chcon -Rt svirt_sandbox_file_t /etc/ceph
sudo chcon -Rt svirt_sandbox_file_t /var/lib/ceph
```

## KV backends

We currently support one KV backend to store our configuration flags, keys and maps: etcd.

There is a `ceph.defaults` config file in the image that is used for defaults to bootstrap daemons. It will add the keys if they are not already present. You can either pre-populate the KV store with your own settings, or provide a ceph.defaults config file. To supply your own defaults, make sure to mount the /etc/ceph/ volume and place your ceph.defaults file there.

Important variables in `ceph.defaults` to add/change when you bootstrap an OSD:

- `/osd/osd_journal_size`
- `/osd/cluster_network`
- `/osd/public_network`

Note: `cluster_network` and `public_network` are currently not populated in the defaults, but can be passed as environment variables with `-e CEPH_PUBLIC_NETWORK=...` for more flexibility

## Populate Key Value store

```
docker run -d --net=host \
-e KV_TYPE=etcd \
-e KV_IP=127.0.0.1 \
-e KV_PORT=2379 \
ceph/daemon populate_kvstore
```

## Zap a device

Sometimes you might want to destroy partition tables from a disk. For this you can use the `zap_device` scenario that works as follow:

```
docker run -d --privileged=true \
-v /dev/:/dev/ \
-e OSD_DEVICE=/dev/sdd \
ceph/daemon zap_device
```

## Deploy a monitor

A monitor requires some persistent storage for the docker container. If a KV store is used, `/etc/ceph` will be auto-generated from data kept in the KV store. `/var/lib/ceph`, however, _must_ be provided by a docker volume. The ceph mon will periodically store data into `/var/lib/ceph`, including the latest copy of the CRUSH map. If a mon restarts, it will attempt to download the latest monmap and CRUSH map from other peer monitors. However, if all mon daemons have gone down, monitors must be able to recover their previous maps. The docker volume used for `/var/lib/ceph` should be backed by some durable storage, and must be able to survive container and node restarts.

Without KV store, run:

```
docker run -d --net=host \
-v /etc/ceph:/etc/ceph \
-v /var/lib/ceph/:/var/lib/ceph/ \
-e MON_IP=192.168.0.20 \
-e CEPH_PUBLIC_NETWORK=192.168.0.0/24 \
ceph/daemon mon
```

With KV store, run:

```
docker run -d --net=host \
-v /var/lib/ceph:/var/lib/ceph \
-e MON_IP=192.168.0.20 \
-e CEPH_PUBLIC_NETWORK=192.168.0.0/24 \
-e KV_TYPE=etcd \
-e KV_IP=192.168.0.20 \
ceph/daemon mon
```

List of available options:

- `MON_NAME`: name of the monitor (default to hostname)
- `CEPH_PUBLIC_NETWORK`: CIDR of the host running Docker, it should be in the same network as the `MON_IP`
- `CEPH_CLUSTER_NETWORK`: CIDR of a secondary interface of the host running Docker. Used for the OSD replication traffic
- `MON_IP`: IP address of the host running Docker
- `NETWORK_AUTO_DETECT`: Whether and how to attempt IP and network autodetection. Meant to be used without `--net=host`.
- `NEW_USER_KEYRING`: if specified, it will be imported to keyrings. Works in demo mode only.

  - 0 = Do not detect (default)
  - 1 = Detect IPv6, fallback to IPv4 (if no globally-routable IPv6 address detected)
  - 4 = Detect IPv4 only
  - 6 = Detect IPv6 only

## Deploy a Manager daemon
Since luminous, a manager daemon is mandatory, see [docs](https://docs.ceph.com/en/latest/mgr/)

Without KV store, run:
```
docker run -d --net=host \
-v /etc/ceph:/etc/ceph \
-v /var/lib/ceph/:/var/lib/ceph/ \
ceph/daemon mgr
```

With KV store, run:
```
docker run -d --net=host \
-v /var/lib/ceph:/var/lib/ceph \
-e KV_TYPE=etcd \
-e KV_IP=192.168.0.20 \
ceph/daemon mgr
```

## Deploy an OSD

There are four available `OSD_TYPE` values:

- `<none>` - if no `OSD_TYPE` is set; one of `disk`, `activate` or `directory` will be used based on autodetection of the current OSD bootstrap state
- `activate` - the daemon expects to be passed a block device of a `ceph-disk`-prepared disk (via the `OSD_DEVICE` environment variable); no bootstrapping will be performed
- `directory` - the daemon expects to find the OSD filesystem(s) already mounted in `/var/lib/ceph/osd/`
- `disk` - the daemon expects to be passed a block device via the `OSD_DEVICE` environment variable
- `prepare` - the daemon expects to be passed a block device and run `ceph-disk` prepare to bootstrap the disk (via the `OSD_DEVICE` environment variable)

Options for OSDs (TODO: consolidate these options between the types):

- `JOURNAL_DIR` - if provided, new OSDs will be bootstrapped to use the specified directory as a common journal area. This is usually used to store the journals for more than one OSD on a common, separate disk. This currently only applies to the `directory` OSD type.
- `JOURNAL` - if provided, the new OSD will be bootstrapped to use the specified journal file (if you do not wish to use the default). This is currently only supported by the `directory` OSD type
- `OSD_DEVICE` - mandatory for `activate` and `disk` OSD types; this specifies which block device to use as the OSD
- `OSD_JOURNAL` - optional override of the OSD journal file. this only applies to the `activate` and `disk` OSD types
- `OSD_FORCE_EXT4` - in case the osd data on ext4 is not automatically recognized (i.e. hidden by overlayfs) you can force them by settings this to `yes`.

### Without OSD_TYPE

If the operator does not specify an `OSD_TYPE` autodetection happens:

- `disk` is used if no bootstrapped OSD is found.
- `activate` is used if a bootstrapped OSD is found and `OSD_DEVICE` is also provided.
- `directory` is used if a bootstrapped OSD is found and no `OSD_DEVICE` is provided.

Without KV backend:

```
docker run -d --net=host \
--pid=host \
--privileged=true \
-v /etc/ceph:/etc/ceph \
-v /var/lib/ceph/:/var/lib/ceph/ \
-v /dev/:/dev/ \
-v /run/udev/:/run/udev/ \
-e OSD_DEVICE=/dev/vdd \
ceph/daemon osd
```

With KV backend:

```
docker run -d --net=host \
--privileged=true \
--pid=host \
-v /dev/:/dev/ \
-v /run/udev/:/run/udev/ \
-e OSD_DEVICE=/dev/vdd \
-e KV_TYPE=etcd \
-e KV_IP=192.168.0.20 \
ceph/daemon osd
```

### Ceph disk

Without KV backend:

```
docker run -d --net=host \
--privileged=true \
--pid=host \
-v /etc/ceph:/etc/ceph \
-v /var/lib/ceph/:/var/lib/ceph/ \
-v /dev/:/dev/ \
-v /run/udev/:/run/udev/ \
-e OSD_DEVICE=/dev/vdd \
-e OSD_TYPE=disk \
ceph/daemon osd
```

Using bluestore:

```
docker run -d --net=host \
--privileged=true \
--pid=host \
-v /etc/ceph:/etc/ceph \
-v /var/lib/ceph/:/var/lib/ceph/ \
-v /dev/:/dev/ \
-v /run/udev/:/run/udev/ \
-e OSD_DEVICE=/dev/vdd \
-e OSD_TYPE=disk \
-e OSD_BLUESTORE=1 \
ceph/daemon osd
```

Using dmcrypt:

```
docker run -d --net=host \
--privileged=true \
--pid=host \
-v /etc/ceph:/etc/ceph \
-v /var/lib/ceph/:/var/lib/ceph/ \
-v /dev/:/dev/ \
-v /run/udev/:/run/udev/ \
-e OSD_DEVICE=/dev/vdd \
-e OSD_TYPE=disk \
-e OSD_DMCRYPT=1 \
ceph/daemon osd
```

With KV backend:

```
docker run -d --net=host \
--privileged=true \
--pid=host \
-v /dev/:/dev/ \
-v /run/udev/:/run/udev/ \
-e OSD_DEVICE=/dev/vdd \
-e OSD_TYPE=disk \
-e KV_TYPE=etcd \
-e KV_IP=192.168.0.20 \
ceph/daemon osd
```

Using bluestore with KV backend:

```
docker run -d --net=host \
--privileged=true \
--pid=host \
-v /dev/:/dev/ \
-v /run/udev/:/run/udev/ \
-e OSD_DEVICE=/dev/vdd \
-e OSD_TYPE=disk \
-e KV_TYPE=etcd \
-e KV_IP=192.168.0.20 \
-e OSD_BLUESTORE=1 \
ceph/daemon osd
```

Using dmcrypt with KV backend:

```
docker run -d --net=host \
--privileged=true \
--pid=host \
-v /dev/:/dev/ \
-v /run/udev/:/run/udev/ \
-e OSD_DEVICE=/dev/vdd \
-e OSD_TYPE=disk \
-e KV_TYPE=etcd \
-e KV_IP=192.168.0.20 \
-e OSD_DMCRYPT=1 \
ceph/daemon osd
```

List of available options:

- `OSD_DEVICE` is the OSD device
- `OSD_JOURNAL` is the journal for a given OSD
- `HOSTNAME` is used to place the OSD in the CRUSH map

If you do not want to use `--privileged=true`, please fall back on the second example.

### Ceph disk activate

This function is balance between ceph-disk and osd directory where the operator can use ceph-disk outside of the container (directly on the host) to prepare the devices. Devices will be prepared with `ceph-disk prepare`, then they will get activated inside the container. A priviledged container is still required as ceph-disk needs to access /dev/. So this has minimum value compare to the ceph-disk but might fit some use cases where the operators want to prepare their devices outside of a container.

```
docker run -d --net=host \
--privileged=true \
--pid=host \
-v /etc/ceph:/etc/ceph \
-v /var/lib/ceph/:/var/lib/ceph/ \
-v /dev/:/dev/ \
-v /run/udev/:/run/udev/ \
-e OSD_DEVICE=/dev/vdd \
-e OSD_TYPE=activate \
ceph/daemon osd
```

### Ceph OSD directory

There are a number of environment variables which are used to configure the execution of the OSD:

- `CLUSTER` is the name of the ceph cluster (defaults to `ceph`)

If the OSD is not already created (key, configuration, OSD data), the following environment variables will control its creation:

- `WEIGHT` is the of the OSD when it is added to the CRUSH map (default is `1.0`)
- `JOURNAL` is the location of the journal (default is the `journal` file inside the OSD data directory)
- `HOSTNAME` is the name of the host; it is used as a flag when adding the OSD to the CRUSH map

The old option `OSD_ID` is now unused. Instead, the script will scan for each directory in `/var/lib/ceph/osd` of the form `<cluster>-<osd_id>`.

To create your OSDs simply run the following command:

`docker exec <mon-container-id> ceph osd create`.

Note that we now default to dropping root privileges, so it is important to set the proper ownership for your OSD directories. The Ceph OSD runs as UID:167, GID:167, so:

`chown -R 167:167 /var/lib/ceph/osd/`

#### Multiple OSDs

There is a problem when attempting run run multiple OSD containers on a single docker host. See issue #19.

There are two workarounds, at present:

- Run each OSD with the `--pid=host` option
- Run multiple OSDs within the same container

To run multiple OSDs within the same container, simply bind-mount each OSD datastore directory:

- `docker run -v /osds/1:/var/lib/ceph/osd/ceph-1 -v /osds/2:/var/lib/ceph/osd/ceph-2`

### Ceph OSD directory single

Ceph OSD directory single has a similar design to Ceph OSD directory since they both aim to run OSD processes from an already bootstrapped directory. So we assume the OSD directory has been populated already. The major different is that Ceph OSD directory single has a much simpler implementation since it only runs a single OSD process per container. It doesn't do anything with the journal as it assumes journal's symlink was provided during the initialization sequence of the OSD.

This scenario goes through the OSD directory (`/var/lib/ceph/osd`) and looks for OSDs that don't have a lock held by any other OSD. If no lock is found, the OSD process starts. If all the OSDs are already running, we gently exit 0 and explain that all the OSDs are already running.

**Important note**: if you are aiming at running multiple OSD containers on a same machine (things that you will likely do with Ceph anyway), you must enable `--pid=host`. However if you are running Docker 1.12 (based on <https://github.com/docker/docker/pull/22481>), you can just share the same PID namespace for the OSD containers only using: `--pid=container:<id>`.

#### BTRFS and journal

If your OSD is BTRFS and you want to use PARALLEL journal mode, you will need to run this container with `--privileged` set to true. Otherwise, `ceph-osd` will have insufficient permissions and it will revert to the slower WRITEAHEAD mode.

#### Note

Re: [<https://github.com/Ulexus/docker-ceph/issues/5>]

A user has reported a consterning (and difficult to diagnose) problem wherein the OSD crashes frequently due to Docker running out of sufficient open file handles. This is understandable, as the OSDs use a great many ports during periods of high traffic. It is, therefore, recommended that you increase the number of open file handles available to Docker.

On CoreOS (and probably other systemd-based systems), you can do this by creating the a file named `/etc/systemd/system/docker.service.d/limits.conf` with content something like:

```
[Service]
LimitNOFILE=4096
```

## Deploy a MDS

By default, the MDS does _NOT_ create a ceph filesystem. If you wish to have this MDS create a ceph filesystem (it will only do this if the specified `CEPHFS_NAME` does not already exist), you _must_ set, at a minimum, `CEPHFS_CREATE=1`. It is strongly recommended that you read the rest of this section, as well.

For most people, the defaults for the following optional environment variables are fine, but if you wish to customize the data and metadata pools in which your CephFS is stored, you may override the following as you wish:

- `CEPHFS_CREATE`: Whether to create the ceph filesystem (0 = no / 1 = yes), if it doesn't exist. Defaults to 0 (no)
- `CEPHFS_NAME`: The name of the new ceph filesystem and the basis on which the later variables are created. Defaults to `cephfs`
- `CEPHFS_DATA_POOL`: The name of the data pool for the ceph filesystem. If it does not exist, it will be created. Defaults to `${CEPHFS_NAME}_data`
- `CEPHFS_DATA_POOL_PG`: The number of placement groups for the data pool. Defaults to `8`
- `CEPHFS_METADATA_POOL`: The name of the metadata pool for the ceph filesystem. If it does not exist, it will be created. Defaults to `${CEPHFS_NAME}_metadata`
- `CEPHFS_METADATA_POOL_PG`: The number of placement groups for the metadata pool. Defaults to `8`

Without KV backend, run:

```
docker run -d --net=host \
-v /var/lib/ceph/:/var/lib/ceph/ \
-v /etc/ceph:/etc/ceph \
-e CEPHFS_CREATE=1 \
ceph/daemon mds
```

With KV backend, run:

```
docker run -d --net=host \
-e CEPHFS_CREATE=1 \
-e KV_TYPE=etcd \
-e KV_IP=192.168.0.20 \
ceph/daemon mds
```

List of available options:

- `MDS_NAME` is the name the MDS server (DEFAULT: mds-$(hostname)). One thing to note is that metadata servers are not machine-restricted. They are not bound by their data directories and can move around the cluster. As a result, you can run more than one MDS on a single machine. If you plan to do so, you better set this variable and do something like: `mds-$(hostname)-a`, `mds-$(hostname)-b`etc...

## Deploy a Rados Gateway

For the Rados Gateway, we deploy it with `civetweb` enabled by default. However it is possible to use different CGI frontends by simply giving remote address and port.

Without kv backend, run:

```
docker run -d --net=host \
-v /var/lib/ceph/:/var/lib/ceph/ \
-v /etc/ceph:/etc/ceph \
ceph/daemon rgw
```

With kv backend, run:

```
docker run -d --net=host \
-e KV_TYPE=etcd \
-e KV_IP=192.168.0.20 \
ceph/daemon rgw
```

List of available options:

- `RGW_CIVETWEB_PORT` is the port to which civetweb is listening on (DEFAULT: 8080)
- `RGW_NAME`: default to hostname

Administration via [radosgw-admin](https://docs.ceph.com/en/latest/man/8/radosgw-admin/) from the Docker host if the `RGW_NAME` variable hasn't been supplied:

`docker exec <containerId> radosgw-admin -n client.rgw.$(hostname) -k /var/lib/ceph/radosgw/$(hostname)/keyring <commands>`

If otherwise, `$(hostname)` has to be replaced by the value of `RGW_NAME`.

To enable an external CGI interface instead of civetweb set:

- `RGW_REMOTE_CGI=1`
- `RGW_REMOTE_CGI_HOST=192.168.0.1`
- `RGW_REMOTE_CGI_PORT=9000`

And run the container like this `docker run -d -v /etc/ceph:/etc/ceph -v /var/lib/ceph/:/var/lib/ceph -e CEPH_DAEMON=RGW -e RGW_NAME=myrgw -p 9000:9000 -e RGW_REMOTE_CGI=1 -e RGW_REMOTE_CGI_HOST=192.168.0.1 -e RGW_REMOTE_CGI_PORT=9000 ceph/daemon`

## Deploy a REST API

This is pretty straightforward. The `--net=host` is not mandatory, if you don't use it do not forget to expose the `RESTAPI_PORT`.
Only available in luminous.

```
docker run -d --net=host \
-e KV_TYPE=etcd \
-e KV_IP=192.168.0.20 \
ceph/daemon restapi
```

List of available options:

- `RESTAPI_IP` is the IP address to listen on (DEFAULT: 0.0.0.0)
- `RESTAPI_PORT` is the listening port of the REST API (DEFAULT: 5000)
- `RESTAPI_BASE_URL` is the base URL of the API (DEFAULT: /api/v0.1)
- `RESTAPI_LOG_LEVEL` is the log level of the API (DEFAULT: warning)
- `RESTAPI_LOG_FILE` is the location of the log file (DEFAULT: /var/log/ceph/ceph-restapi.log)

## Deploy a RBD mirror

This is pretty straightforward. The `--net=host` is not mandatory, with KV we do:

```
docker run -d --net=host \
-e KV_TYPE=etcd \
-e KV_IP=192.168.0.20 \
ceph/daemon rbd_mirror
```

Without KV we do:

```
docker run -d --net=host \
ceph/daemon rbd_mirror
```


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
