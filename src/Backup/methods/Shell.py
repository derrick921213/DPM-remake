from sys import platform as plat
import sys,os
class system_shell:
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