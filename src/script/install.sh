#!/bin/bash
#__author__:derrick921213
cd /tmp
sudo apt update -y && sudo apt install python3-venv patchelf software-properties-common python3-argcomplete -y
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
sudo activate-global-python-argcomplete3
activate_pyzshcomplete
cp ~/.zshrc ~/.zshrc.bak
cp ~/.bashrc ~/.bashrc.bak
sed -i '8i\export PATH="~/.local/bin:$PATH"' ~/.zshrc
sed -i '9i\autoload -U bashcompinit;bashcompinit' ~/.zshrc
sed -i '10i\eval "$(register-python-argcomplete3 dpm)"' ~/.zshrc
echo 'export PATH="~/.local/bin:$PATH"'  >> ~/.bashrc
echo 'eval "$(register-python-argcomplete dpm)"'>> ~/.bashrc
echo [DPM] Install successful.
