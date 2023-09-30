#!/bin/bash
#__author__:derrick921213
cd /tmp
function exists_in_list() {
    LIST=$1
    DELIMITER=$2
    VALUE=$3
    echo $LIST | tr "$DELIMITER" '\n' | grep -F -q -x "$VALUE"
}
os_release_info=$(cat /etc/os-release)
os_like=$(echo "$os_release_info" | grep -o 'ID_LIKE=.*' | cut -d'=' -f2 | sed 's/"//g')
os_like2=($os_like)
if exists_in_list "$os_like" " " debian; then
    sudo apt update -y && sudo apt install build-essential python3-venv patchelf software-properties-common git -y
elif exists_in_list "$os_like" " " rhel; then
    sudo dnf groupinstall "Development Tools" -y
    sudo dnf update -y &&  sudo dnf install epel-release -y && sudo dnf install python3 patchelf git python3-devel yum-utils gcc openssl-devel bzip2-devel libffi-devel zlib-devel libdnf make -y
else
    exit 1
fi

sudo pip3 install argcomplete pyzshcomplete
if [ -d "DPM_SRC" ]; then
    sudo rm -rf "DPM_SRC"
fi
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
if exists_in_list "$os_like" " " debian; then
    sudo activate-global-python-argcomplete3
    yes | activate_pyzshcomplete
    cp ~/.zshrc ~/.zshrc.bak
    cp ~/.bashrc ~/.bashrc.bak
    sed -i '8i\export PATH="~/.local/bin:$PATH"' ~/.zshrc
    sed -i '9i\autoload -U bashcompinit;bashcompinit' ~/.zshrc
    sed -i '10i\autoload -U compinit; compinit' ~/.zshrc
    sed -i '11i\eval "$(register-python-argcomplete3 dpm)"' ~/.zshrc
    echo 'export PATH="~/.local/bin:$PATH"'  >> ~/.bashrc
    echo 'eval "$(register-python-argcomplete3 dpm)"'>> ~/.bashrc
elif exists_in_list "$os_like" " " rhel; then
    activate-global-python-argcomplete
    yes | activate_pyzshcomplete
    cp ~/.zshrc ~/.zshrc.bak
    cp ~/.bashrc ~/.bashrc.bak
    sed -i '8i\export PATH="~/.local/bin:$PATH"' ~/.zshrc
    sed -i '9i\autoload -U bashcompinit;bashcompinit' ~/.zshrc
    sed -i '10i\autoload -U compinit; compinit' ~/.zshrc
    sed -i '11i\eval "$(register-python-argcomplete dpm)"' ~/.zshrc
    echo 'export PATH="~/.local/bin:$PATH"'  >> ~/.bashrc
    echo 'eval "$(register-python-argcomplete dpm)"'>> ~/.bashrc
else
    exit 1
fi
echo [DPM] Install successful.
