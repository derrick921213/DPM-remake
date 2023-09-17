#!/bin/bash
[ ! -d /usr/local/DPM ] && echo [DPM NOT installed] && exit 1
sudo rm -rf /usr/local/bin/dpm
sudo rm -rf /usr/local/DPM
sed -i '/eval "$(register-python-argcomplete3 dpm)"/d' .zshrc
sed -i '/eval "$(register-python-argcomplete3 dpm)"/d' .bashrc
echo [DPM] Uninstall successful.
