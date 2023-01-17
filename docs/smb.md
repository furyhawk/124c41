# Samba

[Samba](https://www.samba.org/) is the standard Windows interoperability
suite of programs for Linux and Unix. Since 1992, Samba has provided
secure, stable and fast file and print services for all clients using
the [SMB/CIFS](wikipedia:Server_Message_Block "wikilink") protocol, such
as all versions of DOS and Windows, OS/2, Linux and many others.

To share files through Samba, see [\#Server](#Server "wikilink")
section; to access files shared through Samba on other machines, please
see [\#Client](#Client "wikilink") section.

## Server

### Installation

[Install](Install "wikilink") the  package.

Samba is configured in the  configuration file, which is extensively
documented in .

Because the  package does not provide this file, one needs to create it
**before** starting .

A documented example as in  from the [Samba git
repository](https://git.samba.org/samba.git/?p=samba.git;a=blob_plain;f=examples/smb.conf.default;hb=HEAD)
may be used to setup .

#### Enabling and starting services

To provide basic file sharing through SMB,
[enable/start](enable/start "wikilink") . See  for details.

If you want to make your server accessible via NetBIOS host name, set
the desired name in the  option in  and
[enable/start](enable/start "wikilink") . See  for details.

#### Make the server discoverable

[Install](Install "wikilink") the  package, then
[enable/start](enable/start "wikilink")  to make the samba server
discoverable with [Zeroconf](Zeroconf "wikilink"). It should work for
most non-Windows file managers (macOS Finder, various GUI-based file
managers on Linux & BSD etc.)

If  is not running, the server will still be accessible, just not
discoverable, i.e. it will not show up in file managers, but you can
still connect to the server directly by IP or domain.

Windows Explorer relies on the WS-Discovery protocol instead; see
[\#Windows 1709 or up does not discover the samba server in Network
view](#Windows_1709_or_up_does_not_discover_the_samba_server_in_Network_view "wikilink").

#### Configure firewall

If you are using a [firewall](firewall "wikilink"), do not forget to
open required ports (usually 137-139 + 445). For a complete list, see
[Samba port usage](https://www.samba.org/~tpot/articles/firewall.html).

##### UFW Rule

A [Ufw](Ufw "wikilink") App Profile for SMB/CIFS is included by default
with the default installation of UFW in .

Allow Samba by running  as root.

If you deleted the profile, create/edit  and add the following content:

`[Samba]`  
`title=LanManager-like file and printer server for Unix`  
`description=The Samba software suite is a collection of programs that implements the SMB/CIFS protocol for unix systems, allowing you to serve files and printers to Windows, NT, OS/2 and DOS clients. This protocol is sometimes also referred to as the LanManager or NetBIOS protocol.`  
`ports=137,138/udp|139,445/tcp`

Then load the profile into UFW run  as root.

Then finally, allow Samba by running  as root.

##### firewalld service

To configure [firewalld](firewalld "wikilink") to allow Samba in the
**home** zone, run:

`# firewall-cmd --permanent --add-service={samba,samba-client,samba-dc} --zone=home`

The three services listed are:

- : for sharing files with others.

- : to browse shares on other machines on the network.

- : for [Samba/Active Directory domain
  controller](Samba/Active_Directory_domain_controller "wikilink").

ensures the changes remain after  is [restarted](restart "wikilink").

### Basic configuration

#### User management

The following section describes creating a local (tdbsam) database of
Samba users. For user authentication and other purposes, Samba can also
be bound to an Active Directory domain, can itself serve as an Active
Directory domain controller, or can be used with an LDAP server.

##### Adding a user

Samba requires a Linux user account - you may use an existing user
account or create a [new
one](Users_and_groups#User_management "wikilink").

Although the user name is shared with Linux system, Samba uses a
password separate from that of the Linux user accounts. Replace  with
the chosen Samba user account:

`# smbpasswd -a `*`samba_user`*

Depending on the [server
role](https://www.samba.org/samba/docs/man/manpages-3/smb.conf.5.html#SERVERROLE),
existing [File permissions and
attributes](File_permissions_and_attributes "wikilink") may need to be
altered for the Samba user account.

If you want the new user only to be allowed to remotely access the file
server shares through Samba, you can restrict other login options：

- disabling shell - 
- disabling SSH logons - edit , change option 

Also see [Security](Security "wikilink") for hardening your system.

##### Listing users

Samba users can be listed using the  command:

`# pdbedit -L -v`

##### Changing user password

To change a user password, use :

`# smbpasswd `*`samba_user`*

#### Creating an anonymous share

1\. Create a Linux user which anonymous Samba users will be mapped to.

`# useradd guest -s /bin/nologin`

2\. Add the following to :

Anonymous users will now be mapped to the Linux user  and have the
ability to access any directories defined in , which is configured to be
 in the example above.

Make sure that the Linux user  has the proper permissions to access
files in .

Also, make sure shares have been properly defined as per the *Share
Definitions* section of
[smb.conf.default](https://git.samba.org/samba.git/?p=samba.git;a=blob_plain;f=examples/smb.conf.default;hb=HEAD).

### Advanced configuration

#### Enable symlink following

Then, [restart](restart "wikilink") .

#### Enable server-side copy for macOS clients

Server-side copy eliminates the need to transfer data between the server
and the client when copying files on the server. This is enabled by
default, but it doesn't work with macOS clients. If you have macOS
clients, you need to add the following configuration to  and then
[restart](restart "wikilink") .

#### Enable Usershares

Usershares is a feature that gives non-root users the capability to add,
modify, and delete their own share definitions. See .

1. Create a directory for usershares: 
2. Create a [user group](user_group "wikilink"): 
3. Change the owner of the directory to  and the group to : 
4. Change the permissions of the  directory so that users in the group 
   can create files. This command also sets [sticky
   bit](Wikipedia:Sticky_bit "wikilink"), which is important to prevent
   users from deleting usershares of other users: 

Set the following parameters in the  configuration file:

Add the user to the *sambashare* group. Replace  with the name of your
user:

`# gpasswd sambashare -a `*`your_username`*

[Restart](Restart "wikilink")  and  services.

Log out and log back in.

If you want to share paths inside your home directory you must make it
accessible for the group *others*.

In the GUI, you can use [Thunar](Thunar "wikilink") or
[Dolphin](Dolphin "wikilink") - right click on any directory and share
it on the network.

In the CLI, use one of the following commands, replacing italic
*sharename*, *user*, ... :

`# net usershare add `*`sharename`*` `*`abspath`*` [`*`comment`*`] [`*`user`*`:{R|D|F}] [guest_ok={y|n}]`  
`# net usershare delete `*`sharename`*  
`# net usershare list `*`wildcard-sharename`*  
`# net usershare info `*`wildcard-sharename`*

#### Set and forcing permissions

Permissions may be applied to both the server and shares:

See  for a full overview of possible permission flags and settings.

#### Restrict protocols for better security

[Append](Append "wikilink")  and  in  to force usage of a minimum and
maximum protocol:

See  in  for an overview of supported protocols.

For compatibility with older clients and/or servers, you might need to
set  or , but please note that this makes you vulnerable to exploits in
SMB1 including ransomware attacks.

[Clients](#Manual_mounting "wikilink") using  may need to specify the
correct , e.g.:

`# mount -t cifs //`*`SERVER`*`/`*`sharename`*` /mnt/`*`mountpoint`*` -o username=`*`username`*`,password=`*`password`*`,iocharset=`*`utf8`*`,vers=`*`3.1.1`*

See  for more information.

#### Use native SMB transport encryption

Native SMB transport encryption is available in SMB version 3.0 or
newer. Clients supporting this type of encryption include Windows 8 and
newer, Windows server 2012 and newer, and smbclient of Samba 4.1 and
newer.

To use native SMB transport encryption by default, set the  parameter
globally and/or by share. Possible values are ,  (default value), , or :

To configure encryption for on the client side, use the option .

See  for more information, especially the paragraphs *Effects for SMB1*
and *Effects for SMB2*.

#### Disable printer sharing

By default Samba shares printers configured using
[CUPS](CUPS "wikilink").

If you do not want printers to be shared, use the following settings:

#### Block certain file extensions on Samba share

Samba offers an option to block files with certain patterns, like file
extensions. This option can be used to prevent dissemination of viruses
or to dissuade users from wasting space with certain files. More
information about this option can be found in .

#### Improve throughput

The default settings should be sufficient for most users. However
setting the 'socket options' correct can improve performance, but
getting them wrong can degrade it by just as much. Test the effect
before making any large changes.

Read the  man page before applying any of the options listed below.

The following settings should be [appended](Append "wikilink") to the 
section of .

Setting a deadtime is useful to stop a server's resources from being
exhausted by a large number of inactive connections:

`deadtime = 30`

The usage of sendfile may make more efficient use of the system CPU's
and cause Samba to be faster:

`use sendfile = yes`

Setting min receivefile size allows zero-copy writes directly from
network socket buffers into the filesystem buffer cache (if available).
It may improve performance but user testing is recommended:

`min receivefile size = 16384`

Increasing the receive/send buffers size and socket optimize flags might
be useful to improve throughput. It is recommended to test each flag
separately as it may cause issues on some networks:

`socket options = IPTOS_LOWDELAY TCP_NODELAY IPTOS_THROUGHPUT SO_RCVBUF=131072 SO_SNDBUF=131072`

#### Enable access for old clients/devices

Latest versions of Samba no longer offer older authentication methods
and protocols which are still used by some older clients (IP cameras,
etc). These devices usually require Samba server to allow NTMLv1
authentication and NT1 version of the protocol, known as CIFS. For these
devices to work with latest Samba, you need to add these two
configuration parameters into  section:

`server min protocol = NT1`  
`ntlm auth = yes`

Anonymous/guest access to a share requires just the first parameter. If
the old device will access with username and password, you also need the
add the second line too.

#### Enable Spotlight searching

Spotlight allows supporting clients (e.g. MacOS Finder) to quickly
search shared files.

Install and start/enable [OpenSearch](OpenSearch "wikilink"). Install ,
configure the directories you want to index in , and start/enable  for
periodic indexing.

Edit  as described in the [Samba
wiki](https://wiki.samba.org/index.php/Spotlight_with_Elasticsearch_Backend#Samba)
to enable Spotlight per share, and restart  to apply the changes.

## Client

Install  for an -like command line interface. See  for commonly used
commands.

For a lightweight alternative (without support for listing public
shares, etc.), [install](install "wikilink")  that provides .

Depending on the [desktop environment](desktop_environment "wikilink"),
GUI methods may be available. See [\#File manager
configuration](#File_manager_configuration "wikilink") for use with a
file manager.

### List public shares

The following command lists public shares on a server:

`$ smbclient -L `*`hostname`*` -U%`

Alternatively, running  will show a tree diagram of all the shares. It
uses broadcast queries and is therefore not advisable on a network with
a lot of computers, but can be helpful for diagnosing if you have the
correct sharename. The  () option suppresses the password prompt.

### NetBIOS/WINS host names

Samba clients handle NetBIOS host names automatically by default (the
behavior is controlled by the  option in ). Other programs (including )
typically use [Name Service Switch](Name_Service_Switch "wikilink"),
which does not handle NetBIOS by default.

The  package provides a libnss driver to resolve NetBIOS host names. To
use it, [install](install "wikilink") it along with the  package (which
provides the *winbindd* daemon), [start/enable](start/enable "wikilink")
 and add  to the  line in :

Now, during host resolving (e.g. when using  or just ), *winbindd* will
resolve the host name by sending queries using NetBIOS Name Service
(NBNS, also known as WINS) protocol.

By default it sends a broadcast query to your local network. If you have
a WINS server, you can add  to  and [restart](restart "wikilink") , then
*winbindd* and other Samba clients will send unicast queries to the
specified IP.

If you want to resolve your local host name (specified in the  option in
), [start/enable](start/enable "wikilink") , which will handle incoming
queries.

You can test WINS resolution with . By default it sends broadcast
queries to your local network regardless of the  option.

Note that WINS resolution requires incoming traffic originating from
port 137.

#### Disable NetBIOS/WINS support

When not using NetBIOS/WINS host name resolution, it may be preferred to
disable this protocol:

Finally [disable](disable "wikilink")/[stop](stop "wikilink") .

### Manual mounting

Mount the share using  as . Not all the options listed below are needed
or desirable:

`# mount --mkdir -t cifs //`*`SERVER`*`/`*`sharename`*` /mnt/`*`mountpoint`*` -o username=`*`username`*`,password=`*`password`*`,workgroup=`*`workgroup`*`,iocharset=`*`utf8`*`,uid=`*`username`*`,gid=`*`group`*

The options  and  corresponds to the local (e.g. client)
[user](user "wikilink")/[user group](user_group "wikilink") to have
read/write access on the given path.

- — The server name.

- — The shared directory.

- — The local directory where the share will be mounted.

- — See  for more information.

#### Storing share passwords

Storing passwords in a world readable file is not recommended. A safer
method is to use a credentials file instead, e.g. inside :

For the mount command replace  with .

The credential file should explicitly readable/writeable to root:

`# chown root:root /etc/samba/credentials`  
`# chmod 700 /etc/samba/credentials`  
`# chmod 600 /etc/samba/credentials/share`

### Automatic mounting

#### Using NetworkManager and GIO/gvfs

[NetworkManager](NetworkManager#Network_services_with_NetworkManager_dispatcher "wikilink")
can be configured to run a script on network status change. This script
uses the *gio* command so that it mounts the Samba shares automatically,
the same way your file manager does, as explained
[below](#File_manager_configuration "wikilink"). The script also safely
unmounts the Samba shares before the relevant network connection is
disabled by listening for the  and  events. Make the script is
[executable](executable "wikilink") after creating it.

Create a symlink inside  to catch the  events:

`# ln -s /etc/NetworkManager/dispatcher.d/30-samba.sh /etc/NetworkManager/dispatcher.d/pre-down.d/30-samba.sh`

#### As mount entry

This is a simple example of a  [mount entry](fstab "wikilink") that
requires authentication:

#### As systemd unit

Create a new  file inside , e.g. . See  for details.

path to share

path to mount the share

share mounting options

To use , [start](start "wikilink") the unit and
[enable](enable "wikilink") it to run on system boot.

##### automount

To automatically mount a share (when accessed, like autofs), one may use
the following automount unit:

[Disable](Disable "wikilink")/[stop](stop "wikilink") the  unit, and
[enable](enable "wikilink")/[start](start "wikilink")  to automount the
share when the mount path is being accessed.

#### smbnetfs

First, check if you can see all the shares you are interested in
mounting:

`$ smbtree -U `*`remote_user`*

If that does not work, find and modify the following line in 
accordingly:

`domain master = auto`

Now [restart](restart "wikilink")  and .

If everything works as expected, [install](install "wikilink") .

Then, add the following line to :

`user_allow_other`

Now copy the directory  to your home directory:

`$ cp -a /etc/smbnetfs/.smb ~`

Then create a link to :

`$ ln -sf /etc/samba/smb.conf ~/.smb/smb.conf`

If a username and a password are required to access some of the shared
folders, edit  to include one or more entries like this:

It is also possible to add entries for specific hosts to be mounted by
smbnetfs, if necessary. More details can be found in .

If you are using the [Dolphin](Dolphin "wikilink") or [GNOME
Files](GNOME_Files "wikilink"), you may want to add the following to  to
avoid "Disk full" errors as smbnetfs by default will report 0 bytes of
free space:

When you are done with the configuration, you need to run

`$ chmod 600 ~/.smb/smbnetfs.*`

Otherwise, smbnetfs complains about 'insecure config file permissions'.

Finally, to mount your Samba network neighbourhood to a directory of
your choice, call

`$ smbnetfs `*`mount_point`*

##### Daemon

The Arch Linux package also maintains an additional system-wide
operation mode for smbnetfs. To enable it, you need to make the said
modifications in the directory .

Then, you can start and/or enable the  [daemon](daemon "wikilink") as
usual. The system-wide mount point is at .

#### autofs

See [Autofs](Autofs "wikilink") for information on the kernel-based
automounter for Linux.

### File manager configuration

#### GNOME Files, Nemo, Caja, Thunar and PCManFM

In order to access samba shares through GNOME Files, Nemo, Caja, Thunar
or PCManFM, install the  package.

Press  and enter  in the location bar to access your share.

The mounted share is likely to be present at  or  in the filesystem.

#### KDE

KDE applications (like Dolphin) has the ability to browse Samba shares
built in. Use the path  to browse the files. If you want to access files
from on non-KDE application, you can install .

To use a GUI in the KDE System Settings, you will need to install the 
package.

#### Other graphical environments

There are a number of useful programs, but they may need to have
packages created for them. This can be done with the Arch package build
system. The good thing about these others is that they do not require a
particular environment to be installed to support them, and so they
bring along less baggage.

- 
- LinNeighborhood, RUmba, xffm-samba plugin for Xffm are not available
  in the official repositories or the AUR. As they are not officially
  (or even unofficially supported), they may be obsolete and may not
  work at all.

## Tips and tricks

### Discovering network shares

If nothing is known about other systems on the local network, and
automated tools such as [smbnetfs](#smbnetfs "wikilink") are not
available, you can manually probe for Samba shares.

First, [install](install "wikilink") the  and  packages.

Use [nmap](nmap "wikilink") to scan your local network to find systems
with TCP port 445 open, which is the port used by the SMB protocol. Note
that you may need to use  or set a custom [ping scan
type](nmap#Ping_scan_types "wikilink") (e.g. ) because Windows systems
are usually firewalled.

The first result is another system; the second happens to be the client
from where this scan was performed.

Now you can connect to there IP addresses directly, but if you want to
use NetBIOS host names, you can use  to check for NetBIOS names. Note
that this will not work if NetBIOS is disabled on the server.

Regardless of the output, look for **\<20\>**, which shows the host with
open services.

Use  to list which services are shared on these systems. You can use
NetBIOS host name ( in this example) instead of IP when available. If
prompted for a password, pressing enter should still display the list:

### Remote control of Windows computer

Samba offers a set of tools for communication with Windows. These can be
handy if access to a Windows computer through remote desktop is not an
option, as shown by some examples.

Send shutdown command with a comment:

`$ net rpc shutdown -C "comment" -I IPADDRESS -U USERNAME%PASSWORD`

A forced shutdown instead can be invoked by changing -C with comment to
a single -f. For a restart, only add -r, followed by a -C or -f.

Stop and start services:

`$ net rpc service stop SERVICENAME -I IPADDRESS -U USERNAME%PASSWORD`

To see all possible net rpc command:

`$ net rpc`

## Troubleshooting

### Failed to start Samba SMB/CIFS server

Possible solutions:

- Check  on syntactic errors with .
- Set correct permissions for  and [restart](restart "wikilink") :

`# chmod 0755 /var/cache/samba/msg`

### Permission issues on SELinux

[SELinux](SELinux "wikilink") not allow samba to access user home
directories by default, to solve this, run:

`# setsebool -P samba_enable_home_dirs 1`

Similarly,  and  make Samba has the ability to read or "read and write"
all files.

### Permission issues on AppArmor

If using a [share path](#Creating_an_anonymous_share "wikilink") located
outside of a home or usershares directory, whitelist it in . E.g.:

### No dialect specified on mount

The client is using an unsupported SMB/CIFS version that is required by
the server.

See [\#Restrict protocols for better
security](#Restrict_protocols_for_better_security "wikilink") for more
information.

### Unable to overwrite files, permissions errors

Possible solutions:

- Append the mount option  to the 
  [entry](#As_mount_entry "wikilink").
- Add  to the  section of the server's .

### Windows clients keep asking for password even if Samba shares are created with guest permissions

Set  inside the  section of :

`map to guest = Bad Password`

If you are still using Samba \< 4.10.10, use  instead of .

### Windows 7 connectivity problems - mount error(12): cannot allocate memory

A known Windows 7 bug that causes "mount error(12): cannot allocate
memory" on an otherwise perfect cifs share on the Linux end can be fixed
by setting a few registry keys on the Windows box as follows:

- (set to )

- (set to )

Alternatively, start Command Prompt in Admin Mode and execute the
following:

`reg add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management" /v "LargeSystemCache" /t REG_DWORD /d 1 /f`  
`reg add "HKLM\SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters" /v "Size" /t REG_DWORD /d 3 /f`

Do one of the following for the settings to take effect:

- Restart Windows
- Restart the Server service via services.msc
- From the Command Prompt run: 'net stop lanmanserver' and 'net start
  lanmanserver' - The server may automatically restart after stopping
  it.

[Original
article](https://web.archive.org/web/20150819153712/http://alan.lamielle.net/2009/09/03/windows-7-nonpaged-pool-srv-error-2017/).

### Windows 10 1709 and up connectivity problems - "Windows cannot access" 0x80004005

This error affects some machines running Windows 10 version 1709 and
later. It is not related to SMB1 being disabled in this version but to
the fact that Microsoft disabled insecure logons for guests on this
version for some, but not others.

To fix, open Group Policy Editor (). Navigate to *Computer
configuration\\administrative templates\\network\\Lanman Workstation \>
Enable insecure guest logons* and enable it. Alternatively,change the
following value in the registry:

`[HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\LanmanWorkstation\Parameters]`  
`"AllowInsecureGuestAuth"=dword:1`

### Error: Failed to retrieve printer list: NT\_STATUS\_UNSUCCESSFUL

If you are a home user and using samba purely for file sharing from a
server or NAS, you are probably not interested in sharing printers
through it. If so, you can prevent this error from occurring by adding
the following lines to your :

[Restart](Restart "wikilink") the samba service, , and then check your
logs:

`# cat /var/log/samba/smbd.log`

and the error should now no longer be appearing.

### Sharing a folder fails

It means that while you are sharing a folder from *Dolphin* (file
manager) and everything seems ok at first, after restarting *Dolphin*
the share icon is gone from the shared folder, and also some output like
this in terminal (*Konsole*) output:

`‘net usershare’ returned error 255: net usershare: usershares are currently disabled`

To fix it, enable usershare as described in [\#Enable
Usershares](#Enable_Usershares "wikilink").

### "Browsing" network fails with "Failed to retrieve share list from server"

And you are using a firewall (iptables) because you do not trust your
local (school, university, hotel) network. This may be due to the
following: When the smbclient is browsing the local network it sends out
a broadcast request on udp port 137. The servers on the network then
reply to your client but as the source address of this reply is
different from the destination address iptables saw when sending the
request for the listing out, iptables will not recognize the reply as
being "ESTABLISHED" or "RELATED", and hence the packet is dropped. A
possible solution is to add:

`iptables -t raw -A OUTPUT -p udp -m udp --dport 137 -j CT --helper netbios-ns`

to your iptables setup.

For [Uncomplicated Firewall](Uncomplicated_Firewall "wikilink"), you
need to add  to the end of the following line in 

`IPT_MODULES="nf_conntrack_ftp nf_nat_ftp nf_conntrack_irc nf_nat_irc"`

and then run the following commands as root:

`echo 1 > /proc/sys/net/netfilter/nf_conntrack_helper`  
`ufw allow CIFS`  
`ufw reload`

To make this change persistent across reboots, add the following line at
the end of :

`net.netfilter.nf_conntrack_helper=1`

### Protocol negotiation failed: NT\_STATUS\_INVALID\_NETWORK\_RESPONSE

The client probably does not have access to shares. Make sure clients'
IP address is in  line in .

Another problem could be, that the client uses an invalid protocol
version. To check this try to connect with the  where you specify the
maximum protocol version manually:

`$ smbclient -U `<user name>` -L //`<server name>` -m <protocol version: e. g. SMB2> -W `<domain name>

If the command was successful then create a configuration file:

### Connection to SERVER failed: (Error NT\_STATUS\_UNSUCCESSFUL)

You are probably passing a wrong server name to . To find out the server
name, run  on the server and look at "Transient hostname" line

### Connection to SERVER failed: (Error NT\_STATUS\_CONNECTION\_REFUSED)

Make sure that the server has started. The shared directories should
exist and be accessible.

### Protocol negotiation failed: NT\_STATUS\_CONNECTION\_RESET

Probably the server is configured not to accept protocol SMB1. Add
option  in . Or just pass argument  to .

### Password Error when correct credentials are given (error 1326)

[Samba 4.5](https://www.samba.org/samba/history/samba-4.5.0.html) has
NTLMv1 authentication disabled by default. It is recommend to install
the latest available upgrades on clients and deny access for unsupported
clients.

If you still need support for very old clients without NTLMv2 support
(e.g. Windows XP), it is possible force enable NTLMv1, although this is
**not recommend** for security reasons:

If NTLMv2 clients are unable to authenticate when NTLMv1 has been
enabled, create the following file on the client: 

This change also affects samba shares mounted with **mount.cifs**. If
after upgrade to Samba 4.5 your mount fails, add the **sec=ntlmssp**
option to your mount command, e.g.

`mount.cifs //server/share /mnt/point -o sec=ntlmssp,...`

See the  man page: **ntlmssp** - Use NTLMv2 password hashing
encapsulated in Raw NTLMSSP message. The default in mainline kernel
versions prior to v3.8 was **sec=ntlm**. In v3.8, the default was
changed to **sec=ntlmssp**.

### Mapping reserved Windows characters

Starting with kernel 3.18, the cifs module uses the ["mapposix" option
by
default](https://git.kernel.org/cgit/linux/kernel/git/torvalds/linux.git/commit/?id=2baa2682531ff02928e2d3904800696d9e7193db).
When mounting a share using unix extensions and a default Samba
configuration, files and directories containing one of the seven
reserved Windows characters  are listed but cannot be accessed.

Possible solutions are:

- Use the undocumented  mount option for cifs

`# mount.cifs //server/share /mnt/point -o nomapposix`

- Configure Samba to remap  ("SFM", Services for Mac) style characters
  to the correct native ones using
  [fruit](https://www.mankier.com/8/vfs_fruit)

<!-- end list -->

- Manually remap forbidden characters using
  [catia](https://www.mankier.com/8/vfs_catia)

The latter approach (using catia or fruit) has the drawback of filtering
files with unprintable characters.

### Folder shared inside graphical environment is not available to guests

This section presupposes:

1. Usershares are configured following [previous
   section](#Enable_Usershares "wikilink")
2. A shared folder has been created as a non-root user from GUI
3. Guests access has been set to shared folder during creation
4. Samba service has been restarted at least once since last  file
   modification

For clarification purpose only, in the following sub-sections is
assumed:

- Shared folder is located inside user home directory path ()
- Shared folder name is *MySharedFiles*
- Guest access is read-only.
- Windows users will access shared folder content without login prompt

#### Verify correct samba configuration

Run the following command from a terminal to test configuration file
correctness:

`$ testparm`

#### Verify correct shared folder creation

Run the following commands from a terminal:

`$ cd /var/lib/samba/usershares`  
`$ ls`

If everything is fine, you will notice a file named 

Read the file contents using the following command:

`$ cat mysharedfiles`

The terminal output should display something like this:

#### Verify folder access by guest

Run the following command from a terminal. If prompted for a password,
just press Enter:

`$ smbclient -L localhost`

If everything is fine, MySharedFiles should be displayed under  column

Run the following command in order to access the shared folder as guest
(anonymous login)

`$ smbclient -N //localhost/MySharedFiles`

If everything is fine samba client prompt will be displayed:

`smb: \>`

From samba prompt verify guest can list directory contents:

`smb: \> ls`

If the  error is displayed, the issue is likely to be with Unix
directory permissions. Ensure that your samba user has access to the
folder and all parent folders. You can test this by sudoing to the user
and attempting to list the mount directory, and all of its parents.

### Mount error: Host is down

This error might be seen when mounting shares of Synology NAS servers.
Use the mount option  to solve it.

### Software caused connection abort

File managers that utilizes  can show the error  when writing a file to
a share/server. This may be due to the server running SMB/CIFS version
1, which many routers use for USB drive sharing (e.g. Belkin routers).
To write to these shares specify the CIFS version with the option .
E.g.:

This can also happen after updating Samba to version 4.11, which
deactivates SMB1 as default, and accessing any Samba share. You can
reenable it by adding

### Connection problem (due to authentification error)

Be sure that you do not leave any space characters before your username
in Samba client configuration file as follows:

The correct format is:

### Windows 1709 or up does not discover the samba server in Network view

With Windows 10 version 1511, support for SMBv1 and thus NetBIOS device
discovery was disabled by default. Depending on the actual edition,
later versions of Windows starting from version 1709 ("Fall Creators
Update") do not allow the installation of the SMBv1 client anymore. This
causes hosts running Samba not to be listed in the Explorer's "Network
(Neighborhood)" views. While there is no connectivity problem and Samba
will still run fine, users might want to have their Samba hosts to be
listed by Windows automatically.  implements a Web Service Discovery
host daemon. This enables (Samba) hosts, like your local NAS device, to
be found by Web Service Discovery Clients like Windows. The default
settings should work for most installations, all you need to do is start
enable .

If the default configuration (advertise itself as the machine hostname
in group "WORKGROUP") should be all you need in most cases. If you need,
you can change configuration options by passing additional arguments to
wsdd by adding them in  (see the manual page for wsdd for details).

does the same thing, but is written in C instead of Python. By default,
it will look for the  and  values in .

### IOS Files can no longer copy-to Samba share on Arch Linux beginning with IOS 14.5

Beginning with IOS 14.5 attempting to transfer from a device running IOS
using the "Files" app to a samba share on Arch Linux will result in the
error:

`The operation couldn't be completed`  
`Operation canceled`

To correct this problem, add add the following to the global section of
your  and [restart](restart "wikilink") . Comment optional:

`## addition for IOS Files transfer-to server`  
`vfs object = fruit streams_xattr`

See <https://apple.stackexchange.com/q/424681> Apple.Stackexchange.com -
"The operation couldn't be completed"/"Operation canceled" error message
when saving to a Samba share via Files app.

### Slow initial connections from certain clients without other performance problems

Some SMB clients, such as Solid Explorer for Android, take significantly
longer to connect to Samba if they fail to resolve the NetBIOS name.
Enabling  will greatly speed up initial connections if this is the case.
Since this is a bug in the client software, please report such cases to
the authors of conflicting software.

## See also

- [Official website](https://www.samba.org/)
- [Samba: An
  Introduction](https://www.samba.org/samba/docs/SambaIntro.html)
- [Samba 3.2.x HOWTO and Reference
  Guide](https://www.samba.org/samba/docs/Samba-HOWTO-Collection.pdf)
  (outdated but still most extensive documentation)
- [Wikipedia](Wikipedia:Samba_\(software\) "wikilink")
- [Gentoo:Samba/Guide](Gentoo:Samba/Guide "wikilink")
- [Debian:Samba/ServerSimple](Debian:Samba/ServerSimple "wikilink")
- [KSMBD](https://docs.kernel.org//filesystems/cifs/ksmbd.html) - A
  linux kernel server which implements SMB3 protocol in kernel space
  for sharing files over network.

[Category:Network sharing](Category:Network_sharing "wikilink")
[Category:Servers](Category:Servers "wikilink")
