# PYTHON_ARGCOMPLETE_OK
# PYZSHCOMPLETE_OK
import argparse as _arg
from argparse import RawTextHelpFormatter
import argcomplete as _auto
import pyzshcomplete as _auto_zsh
from sys import platform as plat
import sys,os,json
from urllib.request import urlopen
import requests
import tarfile
from io import BytesIO
from colorama import Fore, Style
import wget
INSTALL_DIR = '/usr/local/DPM'
DOWNLOAD_TEMP = os.path.join(INSTALL_DIR,'TEMP')
class Error(Exception):
    def __init__(self, msg: str) -> None:
        self.message = msg
    def __str__(self) -> str:
        return self.message
class Action:
    def install_update(self, package, verbose=False):
        if verbose:
            if os.path.isdir(f"/usr/local/DPM/{package}") and os.path.isfile(f"/usr/local/bin/{package}"):
                error = os.system(
                    f'sudo rm -rf /usr/local/bin/{package} /usr/local/DPM/{package}')
                if error == 0:
                    local = os.system(
                        f"sudo mkdir -p /usr/local/DPM/{package};sudo chown -R $USER /usr/local/DPM/*")
                    if local == 0:
                        file = os.system(f"cd /tmp;ls | grep '^dpm_{package}'")
                        if file == 0:
                            download = Download()
                            info = download.read_package_info(package)
                            os.system(
                                f"temp=/tmp;a=`ls $temp | grep '^dpm_{package}'`;tar -xf $temp/$a -C /usr/local/DPM/{package};sudo chmod -R 555 /usr/local/DPM/*;sudo ln -s /usr/local/DPM/{package}/{info['main_file']} /usr/local/bin/{package};rm $temp/$a")
                        else:
                            print('Package NO Found')
                            sys.exit(1)
                else:
                    print('Package Error')
                    sys.exit(1)
        if os.path.isdir(f"/usr/local/DPM/{package}") and os.path.isfile(f"/usr/local/bin/{package}"):
            error = os.system(
                f'sudo rm -rf /usr/local/bin/{package} /usr/local/DPM/{package} >/dev/null 2>&1')
            if error == 0:
                local = os.system(
                    f"sudo mkdir -p /usr/local/DPM/{package};sudo chown -R $USER /usr/local/DPM/* >/dev/null 2>&1")
                if local == 0:
                    file = os.system(
                        f"cd /tmp;ls | grep '^dpm_{package}' >/dev/null 2>&1")
                    if file == 0:
                        download = Download()
                        info = download.read_package_info(package)
                        os.system(
                            f"temp=/tmp;a=`ls $temp | grep '^dpm_{package}'`&&tar -xf $temp/$a -C /usr/local/DPM/{package}&&sudo chmod -R 555 /usr/local/DPM/*&&sudo ln -s /usr/local/DPM/{package}/{info['main_file']} /usr/local/bin/{package}&&rm $temp/$a >/dev/null 2>&1")
                    else:
                        print('Package NO Found')
                        sys.exit(1)
                else:
                    print('Package Error')
                    sys.exit(1)

    def install(self, package, verbose=False):
        download = Download()
        is_my = download.package_list()
        if package in is_my:
            if verbose:
                url = download.read_package_list(package, verbose)
            else:
                url = download.read_package_list(package)
            download.download_file(url)
            local = os.system(
                f"sudo mkdir -p /usr/local/DPM/{package};sudo chown -R $USER /usr/local/DPM/*")
            if local == 0:
                if verbose:
                    file = os.system(
                        f"cd /tmp;ls | grep '^dpm_{package}'")
                    if file == 0:
                        info = download.read_package_info(package)
                        test = os.system(
                            f"temp=/tmp;a=`ls $temp | grep '^dpm_{package}'`&&tar -xf $temp/$a -C /usr/local/DPM/{package}&&sudo chmod -R 555 /usr/local/DPM/*&&sudo ln -s /usr/local/DPM/{package}/{info['main_file']} /usr/local/bin/{package}&&rm $temp/$a")
                        if test == 0:
                            print(f'[{package}] install Success')
                            sys.exit(0)
                        else:
                            print(f'[{package}] install Fail')
                            sys.exit(1)
                    else:
                        print('Package NOT FOUND')
                        sys.exit(1)
                else:
                    file = os.system(
                        f"cd /tmp;ls | grep '^dpm_{package}' >/dev/null 2>&1")
                    if file == 0:
                        info = download.read_package_info(package)
                        test1 = os.system(
                            f"temp=/tmp;a=`ls $temp | grep '^dpm_{package}'`>/dev/null 2>&1&&tar -xf $temp/$a -C /usr/local/DPM/{package}>/dev/null 2>&1&&sudo chmod -R 555 /usr/local/DPM/*>/dev/null 2>&1&&sudo ln -s /usr/local/DPM/{package}/{info['main_file']} /usr/local/bin/{package}>/dev/null 2>&1&&rm $temp/$a >/dev/null 2>&1")
                        if test1 == 0:
                            print(f'[{package}] install Success')
                            sys.exit(0)
                        else:
                            print(f'[{package}] install Fail')
                            sys.exit(1)
                    else:
                        print('Package NOT FOUND')
                        sys.exit(1)
            else:
                print('Package Error')
                sys.exit(1)
        else:
            shell = Shell()
            system = shell.system_platform()
            if system == 'linux':
                if verbose:
                    shell.linux_shell(package, install=True, verbose=True)
                shell.linux_shell(package, install=True)
            elif system == 'darwin':
                if verbose:
                    shell.mac_shell(package, install=True, verbose=True)
                shell.mac_shell(package, install=True)

    def uninstall(self, package, verbose=False):
        download = Download()
        is_my = download.package_list()
        if package in is_my:
            if len(download.installed_package_list(verbose=False)) > 0:
                if verbose:
                    if os.path.isdir(f"/usr/local/DPM/{package}"):
                        if os.system(f"sudo rm -rf /usr/local/DPM/{package} /usr/local/bin/{package}") == 0:
                            print(f"[{package}] Removed!!")
                            sys.exit(0)
                        else:
                            print(f"Remove [{package}] Error!!")
                            sys.exit(1)
                    else:
                        print(f'[{package}] not installed')
                        sys.exit(0)
                else:
                    if os.path.isdir(f"/usr/local/DPM/{package}"):
                        if os.system(f"sudo rm -rf /usr/local/DPM/{package} /usr/local/bin/{package} > /dev/null 2>&1") == 0:
                            print(f"[{package}] Removed!!")
                            sys.exit(0)
                        else:
                            print(f"Remove [{package}] Error!!")
                            sys.exit(1)
                    else:
                        print(f'[{package}] not installed')
                        sys.exit(1)
        else:
            shell = Shell()
            system = shell.system_platform()
            if system == 'linux':
                if verbose:
                    shell.linux_shell(package, uninstall=True, verbose=True)
                shell.linux_shell(package, uninstall=True)
            elif system == 'darwin':
                if verbose:
                    shell.mac_shell(package, uninstall=True, verbose=True)
                shell.mac_shell(package, uninstall=True)

    def update(self, package=None, verbose=False):
        if package is None or package == ' ':
            if verbose:
                test = os.system(
                    '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/derrick921213/Derrick_package_manager-DPM-/main/bin/update.sh?$(date +%s))"')
                if test == 0:
                    print(f"[DPM] self update successfully!!")
                    sys.exit(0)
            test2 = os.system(
                '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/derrick921213/Derrick_package_manager-DPM-/main/bin/update.sh?$(date +%s))" >/dev/null 2>&1')
            if test2 == 0:
                print(f"[DPM] self update successfully!!")
                sys.exit(0)
        else:
            download = Download()
            is_my = download.package_list()
            if package in is_my:
                if len(download.installed_package_list(verbose=False)) > 0:
                    if os.path.isdir(f"/usr/local/DPM/{package}"):
                        if os.path.isfile(f"/usr/local/DPM/{package}/package.json"):
                            with open(f"/usr/local/DPM/{package}/package.json", "r") as f:
                                installed_info = json.loads(f.read())
                                download = Download()
                                download.download_file(
                                    download.read_package_list(package, verbose=True))
                                info = download.read_package_info(package)
                                if info["version"] > installed_info["version"]:
                                    self.install_update(package, verbose)
                                else:
                                    print(f"[{package}] no update!!")
                        else:
                            print(f"[{package}] Update Error")
                    else:
                        print(f"[{package}] not installed")
                else:
                    print(f'[{package}] install first')
            else:
                shell = Shell()
                system = shell.system_platform()
                if system == 'linux':
                    if verbose:
                        shell.linux_shell(package, update=True, verbose=True)
                    shell.linux_shell(package, update=True)
                elif system == 'darwin':
                    if verbose:
                        shell.mac_shell(package, update=True, verbose=True)
                    shell.mac_shell(package, update=True)
class Download:
    def read_package_list(self, package, verbose=False):
        data_json = self.package_list()
        if package in data_json:
            if verbose:
                print(f'{Fore.YELLOW}[{package}]{Style.RESET_ALL} {Fore.GREEN}Found!!{Style.RESET_ALL}')
            return data_json[package]["url"]
        else:
            raise Error(f'{Fore.YELLOW}[{package}]{Style.RESET_ALL} {Fore.RED}not found!!{Style.RESET_ALL}')

    def read_package_info(self, package):
        url = self.read_package_list(package)
        package_json_path = 'package.json'
        response = requests.get(url)
        if response.status_code == 200:
            tgz_bytes = BytesIO(response.content)
            with tarfile.open(fileobj=tgz_bytes, mode='r:gz') as tgz:
                package_json_file = tgz.extractfile(package_json_path)
                if package_json_file:
                    package_json_content = package_json_file.read().decode('utf-8')
                    package_data = json.loads(package_json_content)
                    return package_data
        else:
            raise Error(f'{Fore.RED}Failed to fetch the tgz file.{Style.RESET_ALL}')

    def package_list(self):
        import ssl
        ssl._create_default_https_context = ssl._create_unverified_context
        url = "https://raw.githubusercontent.com/derrick921213/package_manager_server/main/package.json"
        response = urlopen(url)
        data = json.loads(response.read())
        response.close()
        return data

    def installed_package_list(self, verbose=False):
        try:
            installed_package = os.listdir('/usr/local/DPM')
        except FileNotFoundError:
            raise Error(f'{Fore.RED}未安裝 DPM 無法顯示已安裝軟體!{Style.RESET_ALL}')
        packages = len(installed_package)
        if packages > 0:
            if verbose:
                for i in installed_package:
                    print(f"{i}")
            return installed_package
        else:
            raise Error(f'{Fore.RED}嘗試安裝軟體後再試一次{Style.RESET_ALL}')

    def download_file(self, url):
        filename = url.split('/')[-1]
        wget.download(url,os.path.join(DOWNLOAD_TEMP,filename))
        return filename
class Shell:
    def system_platform(self):
        if plat == 'win32':
            print('Platform_Error:This application only on Linux or Mac')
            sys.exit(1)
        return 'linux' if plat == 'linux' else 'darwin'

    def linux_shell(self, package, install=False, uninstall=False, update=False, verbose=False):
        if install is True and uninstall is False and update is False:
            if os.system("which apt >/dev/null") == 0:
                if verbose:
                    if os.system(f"sudo apt install {package} -y") == 0:
                        print(f'[{package}] Install from apt')
                        sys.exit(0)
                if os.system(f"sudo apt install {package} -y 1>/dev/null") == 0:
                    print(f'[{package}] Install from apt')
                    sys.exit(0)
            elif os.system("which dnf >/dev/null") == 0:
                if verbose:
                    if os.system(f"sudo dnf install {package} -y") == 0:
                        print(f'[{package}] Install from dnf')
                        sys.exit(0)
                if os.system(f"sudo dnf install {package} -y 1>/dev/null") == 0:
                    print(f'[{package}] Install from dnf')
                    sys.exit(0)
            elif os.system("which yum >/dev/null") == 0:
                if verbose:
                    if os.system(f"sudo yum install {package} -y") == 0:
                        print(f'[{package}] Install from yum')
                        sys.exit(0)
                if os.system(f"sudo yum install {package} -y 1>/dev/null") == 0:
                    print(f'[{package}] Install from yum')
                    sys.exit(0)
            else:
                print('Package manager not found')
                sys.exit(1)
        elif install is False and uninstall is True and update is False:
            if os.system("which apt >/dev/null") == 0:
                if verbose:
                    if os.system(f"sudo apt remove {package} -y") == 0:
                        print(f'[{package}] Uninstall from apt')
                        sys.exit(0)
                if os.system(f"sudo apt remove {package} -y 1>/dev/null") == 0:
                    print(f'[{package}] Uninstall from apt')
                    sys.exit(0)
            elif os.system("which dnf >/dev/null") == 0:
                if verbose:
                    if os.system(f"sudo dnf install {package} -y ") == 0:
                        print(f'[{package}] Uninstall from dnf')
                        sys.exit(0)
                if os.system(f"sudo dnf install {package} -y 1>/dev/null") == 0:
                    print(f'[{package}] Uninstall from dnf')
                    sys.exit(0)
            elif os.system("which yum >/dev/null") == 0:
                if verbose:
                    if os.system(f"sudo yum remove {package} -y ") == 0:
                        print(f'[{package}] Uninstall from yum')
                        sys.exit(0)
                if os.system(f"sudo yum remove {package} -y 1>/dev/null") == 0:
                    print(f'[{package}] Uninstall from yum')
                    sys.exit(0)
            else:
                print('Package manager not found')
                sys.exit(1)
        elif install is False and uninstall is False and update is True:
            if os.system("which apt >/dev/null") == 0:
                if verbose:
                    if os.system(f"sudo apt update {package} -y") == 0:
                        print(f'[{package}] update from apt')
                        sys.exit(0)
                if os.system(f"sudo apt update {package} -y 1>/dev/null") == 0:
                    print(f'[{package}] update from apt')
                    sys.exit(0)
            elif os.system("which dnf >/dev/null") == 0:
                if verbose:
                    if os.system(f"sudo dnf update {package} -y") == 0:
                        print(f'[{package}] update from dnf')
                        sys.exit(0)
                if os.system(f"sudo dnf update {package} -y 1>/dev/null") == 0:
                    print(f'[{package}] update from dnf')
                    sys.exit(0)
            elif os.system("which yum >/dev/null") == 0:
                if verbose:
                    if os.system(f"sudo yum update {package} -y") == 0:
                        print(f'[{package}] update from yum')
                        sys.exit(0)
                if os.system(f"sudo yum update {package} -y 1>/dev/null") == 0:
                    print(f'[{package}] update from yum')
                    sys.exit(0)
            else:
                print('Package manager not found')
                sys.exit(1)
        else:
            print("Application Error")
            sys.exit(1)

    def mac_shell(self, package, install=False, uninstall=False, update=False, verbose=False):
        if install is True and uninstall is False and update is False:
            if os.system("which brew >/dev/null") == 0:
                if verbose:
                    if os.system(f"brew install {package}") == 0:
                        print(f'[{package}] Install from Homebrew')
                        sys.exit(0)
                if os.system(f"brew install {package} 1>/dev/null") == 0:
                    print(f'[{package}] Install from Homebrew')
                    sys.exit(0)
            else:
                print('Homebrew not found')
                sys.exit(1)
        elif install is False and uninstall is True and update is False:
            if verbose:
                if os.system(f"brew uninstall {package}") == 0:
                    print(f'[{package}] was Removed from Homebrew')
                    sys.exit(0)
            if os.system(f"brew uninstall {package} 1>/dev/null") == 0:
                print(f'[{package}] was Removed from Homebrew')
                sys.exit(0)
            else:
                print(f"Remove [{package}] Error!!")
                sys.exit(1)
        elif install is False and update is False and update is True:
            if verbose:
                if os.system(f"brew upgrade {package}") == 0:
                    print(f'[{package}] was Upgraded from Homebrew')
                    sys.exit(0)
            if os.system(f"brew upgrade {package} 1>/dev/null") == 0:
                print(f'[{package}] was Upgraded from Homebrew')
                sys.exit(0)
            else:
                print(f"Upgrade [{package}] Error!!")
                sys.exit(1)
        else:
            print("Application Error")
            sys.exit(1)
class main:
    def __init__(self, args, package, verbose=False):
        act = Action()
        if package:
            _package = " ".join(package)
        else:
            _package = None
        match args:
            case "install":
                act.install(_package, verbose)
            case "uninstall":
                act.uninstall(_package, verbose)
            case "list":
                Download().installed_package_list(verbose=True)
            case "search":
                if 'list' in package[0] or 'ls' in package[0]:
                    download = Download()
                    packages = download.package_list()
                    print('---------------')
                    for keys in packages.keys():
                        print(keys)
                    print("----These package can install from repository----")
                else:
                    Download().read_package_list(_package, verbose=True)
            case "update":
                act.update(_package, verbose)


if __name__ == '__main__':
    parser = _arg.ArgumentParser(
        prog="dpm", description="DPM is a package manager", formatter_class=RawTextHelpFormatter, epilog="Further help: \n  https://github.com/derrick921213/DPM-remake/")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-v", "--verbose", action="store_true", help="開啟囉唆模式")
    parser.add_argument("commands",  choices=('search', 'install', 'list',
                        'uninstall', 'update'), help="Choose one command to execute!")
    parser.add_argument("package", nargs='*',
                        help="Wants to use packages or command")
    _auto.autocomplete(parser)
    _auto_zsh.autocomplete(parser)
    args = parser.parse_args()
    try:
        if args.verbose:
            main(args.commands, args.package, verbose=True)
        else:
            main(args.commands, args.package)
    except Error as e:
        print(e.message)