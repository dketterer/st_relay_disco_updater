# Updater Script for Synthing Discovery and Relay Server

A script that uses the Github API to fetch the latest release of [Syncthing](https://github.com/syncthing/syncthing) 
[Discovery](https://github.com/syncthing/discosrv)- or [Relay-Server](https://github.com/syncthing/relaysrv).

The scripts replaces the server executables every time it runs with the latest version, 
regardless if there is a difference between the installed and downloaded version.

Errors are send to an administrator via email.

Bash scripts can be used as Cron jobs.

Works best on Centos 7 with stdisco and strelay as systemd services.

# Assumptions

* Executables for relay and discovery server are in /usr/local/bin and are named _stdiscosrv_ and _strelaysrv_.
* Systemd units named _stdiscosrv.service_ and _strelaysrv.service_ are set up.
* Running CENTOS 7 and Python3.6 is installed via [Software Collections](https://linuxize.com/post/how-to-install-python-3-on-centos-7/). 
If not, alter the Bash files and insert the path to the python3 executable.
* You can send emails with the sendmail command. If not, change the `LOG_ERRORS_TO_MAIL` variable in the python script to `False`.

# Installation

* Copy the python file to `/opt/updater`.
* Copy the two Bash files to `/etc/cron.daily`.
* Change the email addresses in the python script to meet your specific environment.