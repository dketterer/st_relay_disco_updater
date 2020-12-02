#!/usr/bin/env bash

systemctl stop strelaysrv.service
source /opt/rh/rh-python36/enable
python strelaydiscoupdater.py https://api.github.com/repos/syncthing/relaysrv/releases/latest strelaysrv --target_dir /usr/local/bin
systemctl start strelaysrv.service