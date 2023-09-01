# PYTHON_ARGCOMPLETE_OK
# PYZSHCOMPLETE_OK
import argparse as _arg
from argparse import RawTextHelpFormatter
import argcomplete as _auto
import pyzshcomplete as _auto_zsh
from methods import Action,Download

class main:
    def __init__(self, args, package, verbose=False):
        self.__commands(args, package, verbose)

    def __commands(self, args, package, verbose):
        act = Action()
        if package:
            _package = " ".join(package)
        else:
            _package = None
        if args == "install":
            act.install(_package, verbose)
        elif args == "uninstall":
            act.uninstall(_package, verbose)
        elif args == "list":
            Download().installed_package_list(verbose=True)
        elif args == "search":
            if 'list' in package[0] or 'ls' in package[0]:
                download = Download()
                packages = download.package_list()
                print('---------------')
                for keys in packages.keys():
                    print(keys)
                print("----These package can install from repository----")
            else:
                # Download().read_package_list(_package, verbose=True)
                Download().read_package_info(_package)
        elif args == "update":
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
    if args.verbose:
        main(args.commands, args.package, verbose=True)
    else:
        main(args.commands, args.package)
