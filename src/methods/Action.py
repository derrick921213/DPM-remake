import os,sys,json
from . import *
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