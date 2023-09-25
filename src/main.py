# PYTHON_ARGCOMPLETE_OK
# PYZSHCOMPLETE_OK
import argparse as _arg
from argparse import RawTextHelpFormatter
import argcomplete as _auto
import pyzshcomplete as _auto_zsh
# from sys import platform as plat
import platform as plat
import sys,os,json,wget,subprocess,requests,tarfile,shutil,git,re
from urllib.request import urlopen
from io import BytesIO
from colorama import Fore, Style
from git import RemoteProgress
from tqdm import tqdm
import pwd
INSTALL_DIR = "/usr/local/DPM"
DOWNLOAD_TEMP = os.path.join(INSTALL_DIR,'TEMP')
BIN_DIR = '/usr/bin'
GIT_PATH = f'{DOWNLOAD_TEMP}/DPM_SRC'
BACKUP_PATH = f'{DOWNLOAD_TEMP}/Backup'
VERSION = 'V1'
system_type = plat.system()
dist_name, dist_version,dist_like = (None,None,None)
def get_linux_distribution():
    try:
        with open('/etc/os-release', 'r') as f:
            lines = f.readlines()
            dist_info = {}
            for line in lines:
                parts = line.strip().split('=')
                if len(parts) == 2:
                    key, value = parts[0], parts[1].strip('"')
                    dist_info[key] = value
            return dist_info.get('NAME'), dist_info.get('VERSION'),dist_info.get('ID_LIKE')
    except FileNotFoundError:
        return None, None, None
if system_type == "Linux":
    dist_name, dist_version,dist_like = get_linux_distribution()
    dist_like = dist_like.split(' ')
def compare_versions(old, new,pattern = r'\d+'):
    old_v = [int(match) for match in re.findall(pattern, old)]
    new_v = [int(match) for match in re.findall(pattern, new)]
    ret = 0
    if old_v < new_v:
        ret=1
    elif old_v > new_v:
        ret=-1
    return ret
def compare_software_version(old: str, new: str) -> bool:
    old_list = list(map(int, old.split('.')))
    new_list = list(map(int, new.split('.')))
    if len(old_list) < 3 or len(new_list) < 3:
        raise ValueError(f'{Fore.RED}Software version wrong!{Style.RESET_ALL}')
    for old_num, new_num in zip(old_list, new_list):
        if old_num < new_num:
            return True
    return False
def check_sudo():
    return True if os.geteuid() == 0 else False
def demote(user_uid, user_gid):
    def result():
        os.setgid(user_gid)
        os.setuid(user_uid)
    return result
def exec_cmd(cmd,username):
    # get user info from username
    pw_record = pwd.getpwnam(username)
    homedir = pw_record.pw_dir
    user_uid = pw_record.pw_uid
    user_gid = pw_record.pw_gid
    env = os.environ.copy()
    env.update({'HOME': homedir, 'LOGNAME': username, 'PWD': os.getcwd(), 'USER': username})
    proc = subprocess.Popen(cmd,shell=True,text=True,env=env,preexec_fn=demote(user_uid, user_gid),stdout=subprocess.PIPE)
    return proc
class mac:
    def __init__(self,packages:list,**kwargs):
        self.original_user = os.environ.get("SUDO_USER")
        self.packages = packages
        self.kwargs = kwargs
        # super().__init__(packages,**kwargs)
    def install(self):
        pk_name = " ".join(self.packages)
        command = f"brew install {pk_name}"
        process = exec_cmd(command,self.original_user)
        if self.kwargs.get('verbose'):
            while True:
                return_code = process.poll()
                if return_code is not None:
                    break
                line = process.stdout.readline().strip()
                if line:
                    print(line)
        process.wait()
    def uninstall(self): 
        pk_name = " ".join(self.packages)
        command = f"brew uninstall {pk_name}"
        process = exec_cmd(command,self.original_user)
        if self.kwargs.get('verbose'):
            while True:
                return_code = process.poll()
                if return_code is not None:
                    break
                line = process.stdout.readline().strip()
                if line:
                    print(line)
        process.wait()
    def update(self): 
        command = f"brew update"
        process = exec_cmd(command,self.original_user)
        if self.kwargs.get('verbose'):
            while True:
                return_code = process.poll()
                if return_code is not None:
                    break
                line = process.stdout.readline().strip()
                if line:
                    print(line)
        process.wait()
class ubuntu:
    def __init__(self,packages:list,**kwargs):
        # super().__init__(packages,**kwargs)
        self.packages = packages
        self.kwargs = kwargs
    try:
        import apt,sys,re
        from apt import debfile
        def install(self,package_name):
            cache = apt.Cache()
            cache.update()
            for package_name in self.packages:
                if re.search(r'\.deb$', package_name) is not None :
                    package_name = debfile.DebPackage(package_name, cache)
                    if package_name.check():
                        package = cache[package_name.pkgname]
                        if not package.is_installed: package_name.install()
                        else: print(f"{package_name.pkgname} is already installed.") 
                    else: print(f"{package._failure_string}")
                else:
                    package = cache[package_name]
                    if package.is_installed: print(f"{package_name} is already installed.")
                    else:
                        package.mark_install()
                        cache.commit()
        def uninstall(self):
            cache = apt.Cache()
            cache.update()
            for package_name in self.packages:
                package = cache[package_name]
                if package.is_installed:
                    package.mark_delete()
                    cache.commit()
                    print(f"{package_name} 已移除。")
                else: print(f"{package_name} 未安装，无需移除。")
        def update(self):
            try:
                cache = apt.Cache()
                cache.update()
                cache.open(None)
                cache.upgrade()
                cache.commit()
                print("Software package list has been successfully updated.")
            except Exception as e:
                print(f"Failed to update software package list: {e}")
    except ModuleNotFoundError:
        pass
class rhel:
    def __init__(self):
        print('RHEL')
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
                if e == 'TEMP' or e.startswith('dpm.') :
                    continue
                installed_package.append(e)
        except FileNotFoundError: raise Error(f'{Fore.RED}未安裝 DPM 無法顯示已安裝軟體!{Style.RESET_ALL}')
        if len(installed_package) > 0: [print(e) for e in installed_package if kwargs.get('verbose')];return installed_package
        else: raise Error(f'{Fore.RED}嘗試安裝軟體後再試一次{Style.RESET_ALL}')
    def extract_all_files(self,tar_file_path, extract_to):
        with tarfile.open(tar_file_path, mode='r:gz') as tar: tar.extractall(extract_to)
    def install_update(self, **kwargs):
        download = Download()
        is_my:dict = download.package_list()
        kwargs["NotMy"]:list = []
        kwargs["My"]:list = [] 
        [kwargs['NotMy'].append(i) if i not in is_my else kwargs['My'].append(i) for i in kwargs.get('package')]
        if len(kwargs['package'])==0:
            all_package = self.installed_package_list()
            for name in all_package:
                new = download.read_package_info(name,remote=True)["version"]
                old = download.read_package_info(name,path=INSTALL_DIR)["version"]
                if compare_software_version(old,new):
                    print(f'{Fore.GREEN}{name}{Style.RESET_ALL}\t{Fore.RED}{old}{Style.RESET_ALL}\t->\t{Fore.YELLOW}{new}{Style.RESET_ALL}')
                    [download.download_file(url) for name,url in download.read_package_list(**kwargs).items()]
                    package_location:str = os.path.join(INSTALL_DIR,name)
                    if not os.path.exists(os.path.join(INSTALL_DIR,name)):
                        raise Error(f'{Fore.YELLOW}{name}{Style.RESET_ALL} {Fore.RED}Not installed!{Style.RESET_ALL}')
                    shutil.rmtree(os.path.join(INSTALL_DIR,name))
                    os.unlink(f'{BIN_DIR}/{name}')
                    os.mkdir(package_location)
                    self.extract_all_files(os.path.join(DOWNLOAD_TEMP,f'dpm_{name}.tgz'),package_location)
                    software = os.path.join(package_location,download.read_package_info(name,path=INSTALL_DIR)['main_file'])
                    os.chmod(software,0o755)
                    os.symlink(software,f'{BIN_DIR}/{name}')
                    print(f'{Fore.YELLOW}{name}{Style.RESET_ALL} {Fore.BLUE}Update Successed.{Style.RESET_ALL}')
                    os.unlink(os.path.join(DOWNLOAD_TEMP,f'dpm_{name}.tgz'))
                else:
                    print(f'{Fore.YELLOW}{name}{Style.RESET_ALL} {Fore.GREEN}No need to update{Style.RESET_ALL}')
            # raise Error(f'{Fore.RED}Not package can update!{Style.RESET_ALL}')
        else:
            for name in kwargs['My']:
                new = download.read_package_info(name,remote=True)["version"]
                old = download.read_package_info(name,path=INSTALL_DIR)["version"]
                if compare_software_version(old,new):
                    print(f'{Fore.GREEN}{name}{Style.RESET_ALL}\t{Fore.RED}{old}{Style.RESET_ALL}\t->\t{Fore.YELLOW}{new}{Style.RESET_ALL}')
                    [download.download_file(url) for name,url in download.read_package_list(**kwargs).items()]
                    package_location:str = os.path.join(INSTALL_DIR,name)
                    if not os.path.exists(os.path.join(INSTALL_DIR,name)):
                        raise Error(f'{Fore.YELLOW}{name}{Style.RESET_ALL} {Fore.RED}Not installed!{Style.RESET_ALL}')
                    shutil.rmtree(os.path.join(INSTALL_DIR,name))
                    os.unlink(f'{BIN_DIR}/{name}')
                    os.mkdir(package_location)
                    self.extract_all_files(os.path.join(DOWNLOAD_TEMP,f'dpm_{name}.tgz'),package_location)
                    software = os.path.join(package_location,download.read_package_info(name,path=INSTALL_DIR)['main_file'])
                    os.chmod(software,0o755)
                    os.symlink(software,f'{BIN_DIR}/{name}')
                    print(f'{Fore.YELLOW}{name}{Style.RESET_ALL} {Fore.BLUE}Update Successed.{Style.RESET_ALL}')
                    os.unlink(os.path.join(DOWNLOAD_TEMP,f'dpm_{name}.tgz'))
        if len(kwargs['NotMy'])==0:
            # 進入系統管理包程序
            callback = check_system()
            syscall = callback(kwargs['NotMy'],**kwargs)
            syscall.update()
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
            callback = check_system()
            syscall = callback(kwargs['NotMy'],**kwargs)
            syscall.install()
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
            callback = check_system()
            syscall = callback(kwargs['NotMy'],**kwargs)
            syscall.uninstall()
    def update(self, **kwargs):
        old_version = Shell().runcmd(f'sudo dpm version',verbose=True,ret=True)
        response = requests.get("https://raw.githubusercontent.com/derrick921213/DPM-remake/main/VERSION.txt")
        if response.status_code == 200:
            new_version =  response.text
        if compare_versions(old_version,new_version) == 1:
            repo_url = 'https://github.com/derrick921213/DPM-remake.git'
            os.mkdir(GIT_PATH) if not os.path.exists(GIT_PATH) else os.system(f'rm -rf {DOWNLOAD_TEMP}/*')
            git.Repo.clone_from(repo_url, GIT_PATH, branch='main', progress=CloneProgress())
            if not Shell().runcmd(f"sudo make upgrade",verbose=True,cwd=GIT_PATH):
                raise Error(f'{Fore.RED}Something Wrong!{Style.RESET_ALL}')
            pattern = r'^dpm\..*'
            files = os.listdir(INSTALL_DIR)
            matching_files = [file for file in files if re.match(pattern, file)]
            if not matching_files:
                raise Error(f'{Fore.RED}No found dpm version!{Style.RESET_ALL}')
            max_version = max(matching_files, key=lambda version: (version, compare_versions('dpm.V0',version)))
            if os.path.islink(os.path.join(BIN_DIR,'dpm')):
                os.unlink(os.path.join(BIN_DIR,'dpm'))
            os.symlink(os.path.join(INSTALL_DIR,max_version),os.path.join(BIN_DIR,'dpm'))
            shutil.rmtree(GIT_PATH)
            print("Success Upgrade!")
        else:
            raise Error(f'{Fore.GREEN}This is Newest!!{Style.RESET_ALL}')
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
        if not kwargs.get('remote',False):
            if package in Action().installed_package_list(verbose=False):
                with open(f'{os.path.join(kwargs.get("path",None),package)}/package.json','r') as f:
                    package_info = json.load(f)
                    return package_info
        else:
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
        process = subprocess.Popen(cmd,stdout = subprocess.PIPE,stderr = subprocess.PIPE,text = True,shell = True,cwd=kwargs.get('cwd',None))
        if kwargs.get('verbose',False):
            while True:
                return_code = process.poll()
                if return_code is not None:
                    break
                line = process.stdout.readline().strip()
                if line:
                    if kwargs.get('ret',False):
                        return line
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
                    msg = "Description"
                    print(f"{Fore.YELLOW}Name{Style.RESET_ALL}\t{Fore.GREEN}{msg:>25s}{Style.RESET_ALL}")
                    print(f'{Fore.GREEN}---------------{Style.RESET_ALL}')
                    for keys,vals in result.items():
                        print(f"{Fore.YELLOW}{keys}{Style.RESET_ALL}\t{Fore.GREEN}{vals['description']:>25s}{Style.RESET_ALL}")
                    print(f"{Fore.GREEN}----{Style.RESET_ALL}{Fore.LIGHTBLUE_EX}These package can install from repository{Style.RESET_ALL}{Fore.GREEN}----{Style.RESET_ALL}")
                else:
                    self.FUNC.get(args.commands)[1](**func_args)
            except IndexError:
                pass
        else:
            self.FUNC.get(args.commands)(**func_args)

if __name__ == '__main__':
    parser = _arg.ArgumentParser(prog="dpm", description="DPM is a package manager", formatter_class=RawTextHelpFormatter, epilog="Further help: \n  https://github.com/derrick921213/DPM-remake/")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-v", "--verbose", action="store_true", help="開啟囉唆模式")
    parser.add_argument("commands",  choices=('search', 'install', 'list','uninstall', 'update','upgrade','version'), help="Choose one command to execute!")
    parser.add_argument("package", nargs='*',help="Wants to use packages or command")
    _auto.autocomplete(parser)
    _auto_zsh.autocomplete(parser)
    args = parser.parse_args()
    try:
        check_system()
        if not check_sudo():
            raise Error(f"{Fore.RED}無法切換管理員身份{Style.RESET_ALL}")
        if not os.path.isdir(INSTALL_DIR):
            Shell().runcmd(f'mkdir -p {INSTALL_DIR}')
        if not os.path.isdir(DOWNLOAD_TEMP):
            Shell().runcmd(f'mkdir -p {DOWNLOAD_TEMP}')
        Main(args)
    except Error as e:
        print(e.message)
