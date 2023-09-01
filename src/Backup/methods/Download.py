import json,os,sys
from urllib.request import urlopen
import tarfile
class package_download:
    def read_package_list(self, package, verbose=False):
        data_json = self.package_list()
        if package in data_json:
            if verbose:
                print(f'[{package}] Found!!')
            return data_json[package]["url"]
        else:
            print(f'[{package}] not found!!')

    def read_package_info(self, package):
        # import subprocess
        # cmd = f"temp=/tmp;a=`ls $temp | grep '^dpm_{package}'`;tar -xf $temp/$a -C $temp package.json;cat $temp/package.json;rm -rf $temp/package.json"
        # output = subprocess.Popen(
        #     cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        # data = output.stdout.read()
        # data_json = json.loads(data.decode("utf-8"))
        # return data_json
        import requests
        import tarfile
        import json
        from io import BytesIO

        url = self.read_package_list(package)
        package_json_path = 'package.json'
        # Fetch the tgz file from the URL
        response = requests.get(url)
        if response.status_code == 200:
            tgz_bytes = BytesIO(response.content)
            with tarfile.open(fileobj=tgz_bytes, mode='r:gz') as tgz:
                package_json_file = tgz.extractfile(package_json_path)
                if package_json_file:
                    package_json_content = package_json_file.read().decode('utf-8')
                    package_data = json.loads(package_json_content)
                    # print(package_data)
                    return package_data
        else:
            print('Failed to fetch the tgz file.')

    def package_list(self):
        import ssl
        ssl._create_default_https_context = ssl._create_unverified_context
        url = "https://raw.githubusercontent.com/derrick921213/package_manager_server/main/package.json"
        response = urlopen(url)
        data = json.loads(response.read())
        response.close()
        return data

    def installed_package_list(self, verbose=False):
        installed_package = os.listdir('/usr/local/DPM')
        packages = len(installed_package)
        if packages > 0:
            if verbose:
                for i in installed_package:
                    print(f"{i}")
            return installed_package
        else:
            print("Try install some package")
            sys.exit(1)

    def download_file(self, url):
        import requests as req
        filename = url.split('/')[-1]
        r = req.get(url, stream=True)
        with open("/tmp/"+filename, 'wb') as f:
            f.write(r.content)
        return filename