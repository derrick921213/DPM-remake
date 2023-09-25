from dpm_module.interface import SysAPI
from typing import NoReturn
import subprocess,os
import pwd
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
class mac(SysAPI):
    def __init__(self,packages:list,**kwargs):
        self.original_user = os.environ.get("SUDO_USER")
        super().__init__(packages,**kwargs)
    def install(self)->NoReturn:
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
    def uninstall(self)->NoReturn: 
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
    def update(self)->NoReturn: 
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