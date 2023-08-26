#!/bin/bash
[ ! -d /usr/local/DPM ] && echo [DPM NOT installed] && exit 1
sudo rm -rf /usr/local/bin/dpm
sudo rm -rf /usr/local/DPM
rm -f ~/.bashrc ~/.zshrc
mv ~/.zshrc.bak ~/.zshrc
mv ~/.bashrc.bak ~/.bashrc
echo [DPM] Uninstall successful.
