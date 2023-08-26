#!/bin/bash
#__author__:derrick921213
export PATH="~/.local/bin:$PATH"
py=$(python3 -c "import os" >/dev/null)

if [ "$?" != '0' ]; then
    echo "Python not install"
    exit 1
fi
pip3 install --user pyinstaller requests argcomplete pyzshcomplete
activate-global-python-argcomplete --user
activate_pyzshcomplete
curl -H "Cache-Control: no-cache" -o dpm.py https://raw.githubusercontent.com/derrick921213/Derrick_package_manager-DPM-/main/dpm.py?$(date +%s)
pyinstaller -F dpm.py >/dev/null 2>&1
if [ "$?" != "0" ]; then
    echo "Install Error!!"
    exit 1
fi
sudo mv dist/dpm /usr/local/bin
sudo rm -rf __pycache__ dist build dpm.spec dpm.py
cp ~/.zshrc ~/.zshrc.bak
cp ~/.bashrc ~/.bashrc.bak
echo 'export PATH="~/.local/bin:$PATH"' >>~/.zshrc
echo 'autoload -U bashcompinit;bashcompinit' >>~/.zshrc
echo 'eval "$(register-python-argcomplete dpm)"' >>~/.zshrc
echo 'export PATH="~/.local/bin:$PATH"' >>~/.bashrc
echo 'eval "$(register-python-argcomplete dpm)"' >>~/.bashrc
echo [DPM] Install successful.
