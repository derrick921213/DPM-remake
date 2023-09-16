# PYTHON_ARGCOMPLETE_OK
# PYZSHCOMPLETE_OK
import argparse as _arg
from argparse import RawTextHelpFormatter
import argcomplete as _auto
import pyzshcomplete as _auto_zsh
from sys import platform as plat
import sys,os,json,wget,subprocess,requests,tarfile,shutil,git,re
from urllib.request import urlopen
from io import BytesIO
from colorama import Fore, Style
from git import RemoteProgress
from tqdm import tqdm
INSTALL_DIR = "/usr/local/DPM"
DOWNLOAD_TEMP = os.path.join(INSTALL_DIR,'TEMP')
BIN_DIR = '/usr/local/bin'
GIT_PATH = f'{DOWNLOAD_TEMP}/DPM_SRC' 
BACKUP_PATH = f'{DOWNLOAD_TEMP}/Backup'
VERSION = 'V1'

def compare_versions(old, new,pattern = r'\d+'):
    old_v = [int(match) for match in re.findall(pattern, old)]
    new_v = [int(match) for match in re.findall(pattern, new)]
    ret = 0
    if old_v < new_v:
        ret=1
    elif old_v > new_v:
        ret=-1
    return ret
    # return True if [int(match) for match in re.findall(pattern, old)] < [int(match) for match in re.findall(pattern, new)] else False
def prompt_sudo():
    return True if os.geteuid() == 0 else False 
class CloneProgress(RemoteProgress):
    def __init__(self):
        super().__init__()
        self.pbar = tqdm()

    def update(self, op_code, cur_count, max_count=None, message=''):
        self.pbar.total = max_count
        self.pbar.n = cur_count
        self.pbar.refresh()
class Error(Exception):
    def __init__(self, msg: str) -> None:
        self.message = msg
    def __str__(self) -> str:
        return self.message
class Action:
    def show_version(self,**kwargs):
        raise Error(VERSION)
    def installed_package_list(self, **kwargs) -> list[str]:
        installed_package = []
        try:
            for e in os.listdir('/usr/local/DPM'):
                if e == 'TEMP' or e=='dpm' :
                    continue
                installed_package.append(e)
        except FileNotFoundError: raise Error(f'{Fore.RED}未安裝 DPM 無法顯示已安裝軟體!{Style.RESET_ALL}')
        if len(installed_package) > 0: [print(e) for e in installed_package if kwargs.get('verbose')];return installed_package 
        else: raise Error(f'{Fore.RED}嘗試安裝軟體後再試一次{Style.RESET_ALL}')
    
    def extract_all_files(self,tar_file_path, extract_to): 
        with tarfile.open(tar_file_path, mode='r:gz') as tar: tar.extractall(extract_to)
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
    
    def install(self, **kwargs):
        download:'Download' = Download()
        shell:'Shell' = Shell()
        is_my:dict = download.package_list()
        verbose:bool = kwargs.get('verbose')
        kwargs["NotMy"]:list = []
        kwargs["My"]:list = []
        [kwargs['NotMy'].append(i) if i not in is_my else kwargs['My'].append(i) for i in kwargs.get('package')]
        if len(kwargs['My'])>0:
            [(os.path.exists(os.path.join(DOWNLOAD_TEMP,f'dpm_{name}.tgz')) or download.download_file(url)) for name,url in download.read_package_list(**kwargs).items()]
            for i in kwargs["My"]:
                package_location:str = os.path.join(INSTALL_DIR,i)
                if os.path.exists(os.path.join(INSTALL_DIR,i)): 
                    print(f'{Fore.YELLOW}{i}{Style.RESET_ALL} {Fore.RED}Package exist!!{Style.RESET_ALL}')
                    continue
                os.mkdir(package_location)
                self.extract_all_files(os.path.join(DOWNLOAD_TEMP,f'dpm_{i}.tgz'),package_location)
                software = os.path.join(package_location,download.read_package_info(i,path=INSTALL_DIR)['main_file'])
                os.chmod(software,0o755)
                os.symlink(software,f'{BIN_DIR}/{i}')
                print(f'{Fore.YELLOW}{i}{Style.RESET_ALL} {Fore.BLUE}Install Successed.{Style.RESET_ALL}')
                os.unlink(os.path.join(DOWNLOAD_TEMP,f'dpm_{i}.tgz'))
        if len(kwargs['NotMy'])>0:
            # 進入系統管理包程序
            print(kwargs['NotMy'])
    
    def uninstall(self, **kwargs):
        download:'Download' = Download()
        shell:'Shell' = Shell()
        is_my:dict = download.package_list()
        verbose:bool = kwargs.get('verbose')
        kwargs["NotMy"]:list = []
        kwargs["My"]:list = []
        [kwargs['NotMy'].append(i) if i not in is_my else kwargs['My'].append(i) for i in kwargs.get('package')]
        if len(kwargs['My'])>0:
            for name in kwargs['My']:
                if not os.path.exists(os.path.join(INSTALL_DIR,name)):
                    raise Error(f'{Fore.RED}{name} 不存在{Style.RESET_ALL}')
                print(f'{Fore.RED}Removeing...{Style.RESET_ALL}')
                files = os.path.join(BIN_DIR,name)
                if os.path.exists(files):
                    os.unlink(files)
                shutil.rmtree(os.path.join(INSTALL_DIR,name))
                print(f'{Fore.YELLOW}{name}{Style.RESET_ALL} {Fore.RED}Removed!!{Style.RESET_ALL}')
        if len(kwargs['NotMy'])>0:
            # 進入系統管理包程序
            print(kwargs['NotMy'])
    
    def update(self, **kwargs):
        repo_url = 'https://github.com/derrick921213/DPM-remake.git'
        os.mkdir(GIT_PATH) if not os.path.exists(GIT_PATH) else os.system(f'rm -rf {DOWNLOAD_TEMP}/*')
        git.Repo.clone_from(repo_url, GIT_PATH, branch='main', progress=CloneProgress())
        if not Shell().runcmd(f"sudo make upgrade VERSION={VERSION}",verbose=True,cwd=GIT_PATH):
            raise Error(f'{Fore.RED}Something Wrong!{Style.RESET_ALL}')
        
        pattern = r'^dpm\..*'
        files = os.listdir(INSTALL_DIR)
        matching_files = [file for file in files if re.match(pattern, file)]
        if not matching_files:
            raise Error(f'{Fore.RED}No found dpm version!{Style.RESET_ALL}')
        # p = subprocess.Popen(["sudo make upgrade"], shell=True,cwd=GIT_PATH)
        # std_out, std_err = p.communicate()
        # print(std_out.strip(), std_err)
        max_version = max(matching_files, key=lambda version: (version, compare_versions('dpm.V0',version)))
        if os.path.exists(os.path.join(BIN_DIR,'dpm')):
            os.unlink(os.path.join(BIN_DIR,'dpm'))
        os.symlink(os.path.join(INSTALL_DIR,max_version),os.path.join(BIN_DIR,'dpm'))
        shutil.rmtree(GIT_PATH)
        print("最大版本号:", max_version)
        print("Success Upgrade!")
class Download:
    
    def read_package_list(self, *args,**kwargs):
        data_json = self.package_list()
        if len(args)==0:
            verbose = kwargs.get('verbose')
            ret = {}
            is_my:dict = Download().package_list()
            kwargs["NotMy"]:list = []
            kwargs["My"]:list = []
            [kwargs['NotMy'].append(i) if i not in is_my else kwargs['My'].append(i) for i in kwargs.get('package')]
            for name in kwargs.get('My'):
                if name in data_json:
                    if verbose:
                        print(f'{Fore.YELLOW}[{name}]{Style.RESET_ALL} {Fore.GREEN}Found!!{Style.RESET_ALL}')
                    ret[name] = data_json[name]["url"]
                else:
                    raise Error(f'{Fore.YELLOW}[{name}]{Style.RESET_ALL} {Fore.RED}not found!!{Style.RESET_ALL}')
            return ret
        else:
            if args[0] in data_json:
                return data_json[args[0]]["url"]
            else:
                raise Error(f'{Fore.YELLOW}[{args[0]}]{Style.RESET_ALL} {Fore.RED}not found!!{Style.RESET_ALL}')
    
    def read_package_info(self, package,**kwargs):
        if package in Action().installed_package_list(verbose=False):
            with open(f'{os.path.join(kwargs.get("path",None),package)}/package.json','r') as f:
                package_info = json.load(f)
                return package_info
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
    
    def package_list(self,**kwargs):
        import ssl
        ssl._create_default_https_context = ssl._create_unverified_context
        url = "https://raw.githubusercontent.com/derrick921213/package_manager_server/main/package.json"
        response = urlopen(url)
        data = json.loads(response.read())
        response.close()
        return data
    
    def download_file(self, url):
        filename = url.split('/')[-1]
        wget.download(url,os.path.join(DOWNLOAD_TEMP,filename))
        print(f'{Fore.GREEN}{filename:>20}{Style.RESET_ALL}')
        return filename
class Shell:
    
    def runcmd(self,cmd:str, **kwargs:dict):
        process = subprocess.Popen(
            cmd,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
            text = True,
            shell = True,
            cwd=kwargs.get('cwd',None)
        )
        if kwargs.get('verbose',False):
            while True:
                return_code = process.poll()
                if return_code is not None:
                    break
                line = process.stdout.readline().strip()
                if line:
                    print(line)
        if kwargs.get('returncode',False):
            return process.returncode
        else:
            return process.returncode==0 if True else False
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
class Main:
    
    def __init__(self,args):
        action = Action()
        download = Download()
        self.FUNC = {
            "install": action.install,
            "uninstall": action.uninstall,
            "list": action.installed_package_list,
            "search": [
                download.package_list,
                download.read_package_list
            ],
            "update": action.install_update,
            "upgrade": action.update,
            "version": action.show_version
        }
        func_args = {
            'package': args.package,
            'verbose': args.verbose,
        }
        if args.commands == "search":
            try:
                if 'list' in func_args['package'][0] or 'ls' in func_args['package'][0]:
                    del func_args['package'][0]
                    result = self.FUNC.get(args.commands)[0](**func_args)
                    print(f'{Fore.GREEN}---------------{Style.RESET_ALL}')
                    for keys in result.keys():
                        print(f'{Fore.YELLOW}{keys}{Style.RESET_ALL}')
                    print(f"{Fore.GREEN}----{Style.RESET_ALL}{Fore.LIGHTBLUE_EX}These package can install from repository{Style.RESET_ALL}{Fore.GREEN}----{Style.RESET_ALL}")
                else:
                    self.FUNC.get(args.commands)[1](**func_args)
            except IndexError:
                pass
        else:
            self.FUNC.get(args.commands)(**func_args)

if __name__ == '__main__':
    parser = _arg.ArgumentParser(
        prog="dpm", description="DPM is a package manager", formatter_class=RawTextHelpFormatter, epilog="Further help: \n  https://github.com/derrick921213/DPM-remake/")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-v", "--verbose", action="store_true", help="開啟囉唆模式")
    parser.add_argument("commands",  choices=('search', 'install', 'list',
                        'uninstall', 'update','upgrade','version'), help="Choose one command to execute!")
    parser.add_argument("package", nargs='*',
                        help="Wants to use packages or command")
    _auto.autocomplete(parser)
    _auto_zsh.autocomplete(parser)
    args = parser.parse_args()
    try:
        if not prompt_sudo():
            raise Error(f"{Fore.RED}無法切換管理員身份{Style.RESET_ALL}")
        if not os.path.isdir(INSTALL_DIR):
            Shell().runcmd(f'mkdir -p {INSTALL_DIR}')
        if not os.path.isdir(DOWNLOAD_TEMP):
            Shell().runcmd(f'mkdir -p {DOWNLOAD_TEMP}')
        Main(args)
    except Error as e:
        print(e.message)