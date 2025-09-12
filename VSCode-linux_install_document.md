# 安装说明

1. 下载visual studio code 源码：下载地址：https://code.visualstudio.com/Download#

2. 解压

3. 覆盖

4. ```bash
   # 进入VSCode安装目录
   cd /home/lirongyao0916/SoftWares/VSCode/
   
   # 设置chrome-sandbox的所有者为root
   sudo chown root:root chrome-sandbox
   
   # 设置正确的权限（4755）
   sudo chmod 4755 chrome-sandbox
   
   # 1. 更改文件所有者为 root
   sudo chown root:root /home/lirongyaoper/Softwares/VSCode-linux-x64/chrome-sandbox
   
   # 2. 设置正确的权限模式（4755 包含 setuid 位）
   sudo chmod 4755 /home/lirongyaoper/Softwares/VSCode-linux-x64/chrome-sandbox
   
   ```
   
   

