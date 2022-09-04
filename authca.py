import ctypes
import os
import subprocess
import sys
import time

import requests

BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))


def is_admin():
    """
        获取权限
    :return: 
    """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def download_ca():
    """
        下载 CA 证书
    :return:
    """
    with open(os.path.join(BASE_DIR, "mitmproxy.cer"), 'wb') as f:
        f.write(
            requests.get(
                "http://mitm.it/cert/cer"
            ).content
        )


def insert_ca():
    """
        安装 CA 证书
    :return:
    """
    if is_admin():
        # 将要运行的代码加到这里
        output = subprocess.Popen(
            ("certutil.exe", "-addstore", "root", os.path.join(BASE_DIR, "mitmproxy.cer")),
            stdout=subprocess.PIPE).stdout
        for line in output:
            print(line.decode(encoding='gbk', errors="ignore"))
        print("证书安装完成，关闭页面即可，10秒后自动关闭")
        os.remove(os.path.join(BASE_DIR, "mitmproxy.cer"))
        output.close()
        time.sleep(10)
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)


if __name__ == '__main__':
    download_ca()
    insert_ca()
