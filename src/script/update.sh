#!/bin/bash
export PATH="~/.local/bin:$PATH"
[ ! -d /usr/local/DPM ] && echo "DPM is not install.See my github to install." && exit 1
[ -f ~/.local/bin/pyinstaller ] && sudo mv ~/.local/bin/pyinstaller /usr/local/bin
curl -H "Cache-Control: no-cache" -o dpm.py https://raw.githubusercontent.com/derrick921213/Derrick_package_manager-DPM-/main/dpm.py?$(date +%s)
pyinstaller -F dpm.py
sudo rm -rf /usr/local/bin/dpm
sudo mv dist/dpm /usr/local/bin
sudo rm -rf __pycache__ dist build dpm.spec dpm.py
