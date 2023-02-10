# Samba

This document describes how to mount CIFS shares permanently. The shares
might be hosted on a Windows computer/server, or on a Linux/UNIX server
running [Samba](https://help.ubuntu.com/community/Samba "wikilink").
This document also applies to SMBFS shares, which are similar to CIFS
but are deprecated and should be avoided if possible
([link](https://bugzilla.samba.org/show_bug.cgi?id=1920#c0 "wikilink")).

(This document does *not* describe how to host the shares yourself, only
how to access shares that are hosted somewhere else. For hosting shares,
use [Samba](https://help.ubuntu.com/community/Samba "wikilink").)

## Prerequisites

We're assuming that:

- Network connections have been configured properly.
- Your local (Ubuntu) username is `ubuntuusername`.
- Share username on Windows computer is `msusername`.
- Share password on Windows computer is `mspassword`.
- The Windows computer's name is `servername` this can be either an IP address or an assigned name).
- The name of the share is `sharename`.
- You want to mount the share in `/media/windowsshare`.

## CIFS installation

On older systems:

## Mounting unprotected (guest) network folders

First, let's create the mount directory. You will need a separate
directory for each mount. 

Then edit your /etc/fstab file (with root privileges) to add this line: 

Where

- **guest** indicates you don't need a password to access the share,
- **uid=1000** makes the Linux user specified by the id the owner of the mounted share, allowing them to rename files,
- **iocharset=utf8** allows access to files with names in non-English languages. This doesn't work with shares of devices like the Buffalo Tera Station, or Windows machines that export their shares using ISO8895-15.
- If there is any **space in the server path**, you need to replace it by \040, for example //servername/My\040Documents`

After you add the entry to /etc/fstab type:  This will (re)mount all
entries listed in /etc/fstab.

## Mount password protected network folders

The quickest way to auto-mounting a password-protected share is to edit
/etc/fstab (with root privileges), to add this line: 

This is not a good idea however: /etc/fstab is readable by everyone and
so is your Windows password in it. The way around this is to use a
credentials file. This is a file that contains just the username and
password.

Using a text editor, create a file for your remote servers logon
credential:

Enter your Windows username and password in the file:

Save the file, exit the editor.

Change the permissions of the file to prevent unwanted access to your
credentials:

Then edit your /etc/fstab file (with root privileges) to add this line
(replacing the insecure line in the example above, if you added it):

Save the file, exit the editor.

Finally, test the fstab entry by issuing:

If there are no errors, you should test how it works after a reboot.
Your remote share should mount automatically.

### Special permissions

If you need special permission (like chmod etc.), you'll need to add a
*uid* (short for 'user id') or *gid* (for 'group id') parameter to the
share's mount options.

### Mount password protected shares using libpam\_mount (Ubuntu 9.04)

In addition to the initial assumptions, we're assuming that

- **Your username and password are the same on the Ubuntu machine and on the network drive.**

Install libpam-mount: 

Edit /etc/security/pam\_mount.conf.xml using your preferred text editor.

First, we're moving the user specific config bits to a file which users
can actually edit themselves: remove the commenting tags ( ) surrounding
the section called <luserconf name=".pam_mount.conf.xml" />. Save the
file when done. With this in place, users can create their own
\~/.pam\_mount.conf.xml.

Add the following:

## Troubleshooting

### Login errors

If you get the error "mount error(13) permission denied", then the
server denied your access. Here are the first things to check:

- Are you using a valid username and password? Does that account really have access to this folder?
- Do you have whitespace in your credentials file? It should be ``, not ``.
- Do you need a domain? For example, if you are told that your username is ``, then actually your username is `` and your domain is ``. The fstab entry should read: `` Or:
- The security and version settings are interrelated. SMB1 is insecure and no longer supported by default. At first, try to not specify either security or version: do not specify `` or ``. If you still have authentication errors then you may need to specify either `` or `` or both. You can try the options listed at the `[`mount.cifs`` 
 ``man`` 
 ``page`](http://manpages.ubuntu.com/manpages/raring/en/man8/mount.cifs.8.html "wikilink")`. The man page list leaves out the option `` for some reason, but you should try that one as well (`[`see`` 
 ``discussion`](https://bugs.launchpad.net/ubuntu/+source/cifs-utils/+bug/1113395 "wikilink")`).`

### Unprotected network folder won't automount

I've had a situation where an unprotected network folder wouldn't
automount during bootup, but after manually entering "sudo mount -a" was
mounted correctly. I solved this by replacing the "guest" option by
"username=guest,password=". If anyone has an explanation for this,
please leave a comment.

### Mount during login instead of boot

If for some reason/etc/rc0.d/S31umountnfs.sh (networking problems for
example) the automatic mounting during boot doesn't work, you can add
the "noauto" parameter to your smbfs fstab entry and then have the share
mounted at login.

In /etc/fstab: 

In /etc/rc.local: 

### Slow shutdown due to a CIFS/Network Manager bug

If you use Network Manager, and are getting really slow shutdowns, it's
probably because NM shuts down before unmounting the network shares.
That will cause CIFS to hang and wait for 60 seconds or so. Here's how
to fix it:/etc/rc0.d/S31umountnfs.sh

Ubuntu 12.04 already runs **umountnfs.sh** at reboot and shutdown by
default (/etc/rc0.d/S31umountnfs.sh and /etc/rc6.d/S31umountnfs.sh) so
this is no longer necessary.

-----

### CIFS Options Deprecated

20 Feb 2008 TW

Using dmask or fmask in the fstab file produces the following warnings:
WARNING: CIFS mount option 'dmask' is deprecated. Use 'dir\_mode'
instead. WARNING: CIFS mount option 'fmask' is deprecated. Use
'file\_mode' instead.

Instead use this format: file\_mode=0777,dir\_mode=0777 . Or in some
cases you might need to use file\_mode=0777,dir\_mode=0777,nounix ([see
discussion](http://superuser.com/a/410561 "wikilink"))

-----

\== Use of tilde in pathnames such as "credentials=\~/.smbcredentials"
==

20 Feb 2008 TW

Curiously, using credentials=\~/.smbcredentials in fstab didn't work. I
had to use the full path, i.e. /home/username/.smbcredentials

(This is likely because the tilde "\~" is only a shell short-hand alias
for "$HOME"; it isn't something recognized system-wide by all programs,
especially not in a system file table where the concept of "HOME"
doesn't really exist. -Ian\!)

-----

CategoryDocumentation
