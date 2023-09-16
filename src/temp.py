# from os.path import join
# import wget
# INSTALL_DIR = '/usr/local/DPM'
# print(INSTALL_DIR)
# print(join(INSTALL_DIR,'test'))
# DOWNLOAD_TEMP = join(INSTALL_DIR,'TEMP')
# def download_file(url):
#         filename = url.split('/')[-1]
#         # wget.download(url,join(DOWNLOAD_TEMP,filename))
#         print(join(DOWNLOAD_TEMP,filename))
#         return filename
# download_file("https://github.com/derrick921213/package_manager_server/raw/main/software/dpm_test.tgz")

# print(DOWNLOAD_TEMP)
# from os import environ
# print(environ)
# import json,tarfile,requests
# from colorama import Fore, Style
# from urllib.request import urlopen
# from io import BytesIO
# import wget,os
# INSTALL_DIR = '/usr/local/DPM'
# DOWNLOAD_TEMP = os.path.join(INSTALL_DIR,'TEMP')
# class Error(Exception):
#     def __init__(self, msg: str) -> None:
#         self.message = msg
#     def __str__(self) -> str:
#         return self.message
# class Download:
#     def read_package_list(self, *args,**kwargs):
#         data_json = self.package_list()
#         if len(args)==0:
#             verbose = kwargs.get('verbose')
#             ret = {}
#             for name in kwargs.get('package'):
#                 if name in data_json:
#                     if verbose:
#                         print(f'{Fore.YELLOW}[{name}]{Style.RESET_ALL} {Fore.GREEN}Found!!{Style.RESET_ALL}')
#                     ret[name] = data_json[name]["url"]
#                 else:
#                     raise Error(f'{Fore.YELLOW}[{name}]{Style.RESET_ALL} {Fore.RED}not found!!{Style.RESET_ALL}')
#             return ret
#         else:
#             if args[0] in data_json:
#                 return data_json[args[0]]["url"]
#             else:
#                 raise Error(f'{Fore.YELLOW}[{args[0]}]{Style.RESET_ALL} {Fore.RED}not found!!{Style.RESET_ALL}')

#     def read_package_info(self, package,**kwargs):
#         url = self.read_package_list(package)
#         package_json_path = 'package.json'
#         response = requests.get(url)
#         if response.status_code == 200:
#             tgz_bytes = BytesIO(response.content)
#             with tarfile.open(fileobj=tgz_bytes, mode='r:gz') as tgz:
#                 package_json_file = tgz.extractfile(package_json_path)
#                 if package_json_file:
#                     package_json_content = package_json_file.read().decode('utf-8')
#                     package_data = json.loads(package_json_content)
#                     return package_data
#         else:
#             raise Error(f'{Fore.RED}Failed to fetch the tgz file.{Style.RESET_ALL}')

#     def package_list(self,**kwargs):
#         import ssl
#         ssl._create_default_https_context = ssl._create_unverified_context
#         url = "https://raw.githubusercontent.com/derrick921213/package_manager_server/main/package.json"
#         response = urlopen(url)
#         data = json.loads(response.read())
#         response.close()
#         return data

#     def installed_package_list(self, verbose=False):
#         try:
#             installed_package = os.listdir('/usr/local/DPM')
#         except FileNotFoundError:
#             raise Error(f'{Fore.RED}未安裝 DPM 無法顯示已安裝軟體!{Style.RESET_ALL}')
#         packages = len(installed_package)
#         if packages > 0:
#             if verbose:
#                 for i in installed_package:
#                     print(f"{i}")
#             return installed_package
#         else:
#             raise Error(f'{Fore.RED}嘗試安裝軟體後再試一次{Style.RESET_ALL}')

#     def download_file(self, url):
#         filename = url.split('/')[-1]
#         wget.download(url,os.path.join(DOWNLOAD_TEMP,filename))
#         return filename
# test = Download()
# print(test.read_package_info('test'))

# import os, subprocess

# def prompt_sudo():
#     ret:bool = True
#     if os.geteuid() != 0:
#         msg:str = "[sudo] password for %u:"
#         ret = (subprocess.check_call("sudo -v -p '%s'" % msg, shell=True)==0) if ret else False
#     return ret
# if not prompt_sudo():
#     print("無法切換管理員身份")
# else:
#     print("Now you're root")

# from os import getuid

# if (getuid() != 0):
#     print('Not root user')

# from os.path import join
# INSTALL_DIR = '/usr/local/DPM'
# DOWNLOAD_TEMP = join(INSTALL_DIR,'TEMP')
# BIN_DIR = join(INSTALL_DIR,'TEMP') 

# import os

# src = '/usr/bin/python3'
# dst = '/tmp/python'

# # This creates a symbolic link on python in tmp directory
# os.symlink(src, dst)

# print ("symlink created")


# from typing import overload,NoReturn

# @overload
# def hello(ret:str) -> str:
#     return ret

# @overload
# def hello(ret:int) -> int:
#     return ret

# def hello(ret:float)->float:
#     return ret

# print(type(hello(1)),type(hello('name')))
# import json
# class Book: 
#     title = None
#     author = None
#     pages = 0
#     @overload
#     def __init__(self, title: str, author: str)-> NoReturn:
#         self.title = title
#         self.author = author
#     @overload
#     def __init__(self, title: str, pages: int)-> NoReturn:
#         self.title = title
#         self.pages = pages
#     def __init__(self, title: str, author: str, pages: int) -> NoReturn:
#         self.title = title
#         self.author = author
#         self.pages = pages
#     def __call__(self, title: str, author: str, pages: int):
#         self.title = title
#         self.author = author
#         self.pages = pages
    
#     def __len__(self) -> int:
#         return self.pages
    
#     def __str__(self) -> str:
#         return f'name={self.title}, author={self.author}, pages={self.pages}'
    
#     @classmethod
#     def from_json(cls, book_as_json: str) -> 'Book':
#         book = json.loads(book_as_json)
#         return cls(title=book['title'], author=book['author'], pages=book['pages'])

# # print(Book.from_json(json.dumps({'title':'test','author':'derrick','pages':300})))
# # print(len(Book.from_json(json.dumps({'title':'test','author':'derrick','pages':300}))))
# test = Book('test','derrick')
# print(test)
# class Test:
#     result = None
#     @overload
#     def __init__(self,data:int) -> NoReturn:
#         self.result = data
#     @overload
#     def __init__(self,data:float) -> NoReturn:
#         self.result = data
#     def __init__(self,data) -> NoReturn:
#         self.result = data
#     def __str__(self):
#         return f'type={type(self.result)}, data={self.result}'
# print(Test(1))
# import subprocess

# def runcmd(cmd, **kwargs):
#     process = subprocess.Popen(
#         cmd,
#         stdout = subprocess.PIPE,
#         stderr = subprocess.PIPE,
#         text = True,
#         shell = True
#     )
#     std_out, std_err = process.communicate()
#     if kwargs.get('verbose',False):
#         print(std_out.strip(), std_err)
#     if kwargs.get('returncode',False):
#         return process.returncode
#     else:
#         return process.returncode==0 if True else False

# ret = runcmd('echo "Hello, World!"', verbose = True,returncode=True)
# import tarfile
# def extract_all_files(tar_file_path, extract_to):
#     with tarfile.open(tar_file_path, mode='r:gz') as tar:
#         tar.extractall(extract_to)

# tar_file_path = 'dpm_test.tgz'
# extract_to = 'test'
# extract_all_files(tar_file_path,extract_to)

# import os,stat
# os.rename(__file__,'test1.py')
# os.chmod('main.py',stat.S_IRWXU|stat.S_IRGRP|stat.S_IXGRP|stat.S_IROTH|stat.S_IXOTH)
# os.symlink('main.py','../test1.py')
# os.chmod('../test1.py',0o777)

# import git
# from git import RemoteProgress
# from tqdm import tqdm

# class CloneProgress(RemoteProgress):
#     def __init__(self):
#         super().__init__()
#         self.pbar = tqdm()

#     def update(self, op_code, cur_count, max_count=None, message=''):
#         self.pbar.total = max_count
#         self.pbar.n = cur_count
#         self.pbar.refresh()

# git.Repo.clone_from("https://github.com/derrick921213/DPM-remake.git", "DPM_SRC", branch='main', progress=CloneProgress())
# import os
# import shutil
# import git
# import subprocess
# import sys

# def update():
#     # 定义一些路径和参数
#     GIT_PATH = '/path/to/your/git/repo'
#     BACKUP_PATH = '/path/to/backup/directory'
#     repo_url = 'https://github.com/derrick921213/DPM-remake.git'

#     try:
#         # 备份旧版本代码
#         if os.path.exists(BACKUP_PATH):
#             shutil.rmtree(BACKUP_PATH)
#         shutil.copytree(GIT_PATH, BACKUP_PATH)

#         # 下载新版本代码
#         git.Repo.clone_from(repo_url, GIT_PATH, branch='main')

#         # 重启程序
#         subprocess.Popen([sys.executable] + sys.argv)

#         # 退出当前程序
#         sys.exit(0)
#     except Exception as e:
#         print(f"更新失败: {str(e)}")
#         # 在更新失败时，你可以回滚到备份的旧版本
#         if os.path.exists(BACKUP_PATH):
#             shutil.rmtree(GIT_PATH)
#             shutil.copytree(BACKUP_PATH, GIT_PATH)
#         sys.exit(1)

# if __name__ == "__main__":
#     update()

#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
Play with atexit
"""

import atexit
import sys

print('enter script')

# do something
print('do something')

def _leave_0():
    print('exit script 0')


def _leave_1(*args):
    print('args:', args)
    print('exit script 1')


atexit.register(_leave_0)
atexit.register(_leave_1, *sys.argv)

if len(sys.argv) < 2:
    atexit.unregister(_leave_1)