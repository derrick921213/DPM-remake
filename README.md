# DPM-remake
## 安裝腳本
```shell
curl -sSLf -H "Cache-Control: no-cache, no-store, must-revalidate" https://raw.githubusercontent.com/derrick921213/DPM-remake/main/src/script/install.sh | bash
```
## 刪除腳本
```shell
curl -sSLf -H "Cache-Control: no-cache, no-store, must-revalidate" https://raw.githubusercontent.com/derrick921213/DPM-remake/main/src/script/uninstall.sh | bash
```
## DPM使用方式
### 安裝軟體
```shell
sudo dpm install {package_name}
```
### 刪除軟體
```shell
sudo dpm uninstall {package_name}
```
### 搜尋軟體
```shell
sudo dpm search {package_name}
```
### 更新軟體
```shell
sudo dpm update {package_name}
```
### 列出已安裝軟體
```shell
sudo dpm list
```
### 更新DPM本身
```shell
sudo dpm upgrade
```