from os.path import join
import wget
INSTALL_DIR = '/usr/local/DPM'
print(INSTALL_DIR)
print(join(INSTALL_DIR,'test'))
DOWNLOAD_TEMP = join(INSTALL_DIR,'TEMP')
def download_file(url):
        filename = url.split('/')[-1]
        # wget.download(url,join(DOWNLOAD_TEMP,filename))
        print(join(DOWNLOAD_TEMP,filename))
        return filename
download_file("https://github.com/derrick921213/package_manager_server/raw/main/software/dpm_test.tgz")

print(DOWNLOAD_TEMP)