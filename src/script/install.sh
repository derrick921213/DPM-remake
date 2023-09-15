#!/bin/bash
#__author__:derrick921213
cd /tmp
sudo apt update -y && sudo apt install python3-venv patchelf python-argcomplete -y
sudo pip3 install pyzshcomplete
git clone https://github.com/derrick921213/DPM-remake.git DPM_SRC
if [ "$?" != '0' ]; then
    echo "git Error"
    exit 1
fi
cd DPM_SRC
sudo make install
if [ "$?" != '0' ]; then
    echo "make Error"
    exit 1
fi
activate-global-python-argcomplete --user
activate_pyzshcomplete
cp ~/.zshrc ~/.zshrc.bak
cp ~/.bashrc ~/.bashrc.bak
echo 'export PATH="~/.local/bin:$PATH"' >>~/.zshrc
echo 'autoload -U bashcompinit;bashcompinit' >>~/.zshrc
echo 'eval "$(register-python-argcomplete dpm)"' >>~/.zshrc
echo 'export PATH="~/.local/bin:$PATH"' >>~/.bashrc
echo 'eval "$(register-python-argcomplete dpm)"' >>~/.bashrc
echo [DPM] Install successful.
