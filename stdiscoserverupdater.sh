#!/usr/bin/env bash

systemctl stop stdiscosrv.service
source /opt/rh/rh-python36/enable
python strelaydiscoupdater.py https://api.github.com/repos/syncthing/discosrv/releases/latest stdiscosrv --target_dir /usr/local/bin
systemctl start stdiscosrv.service