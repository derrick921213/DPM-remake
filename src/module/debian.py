from .interface import SysAPI
class ubuntu(SysAPI):
    def __init__(self,packages:list,**kwargs):
        super().__init__(packages,**kwargs)
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