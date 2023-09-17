#!/bin/bash
[ ! -d /usr/local/DPM ] && echo [DPM NOT installed] && exit 1
sudo rm -rf /usr/local/bin/dpm
sudo rm -rf /usr/local/DPM
echo [DPM] Uninstall successful.
