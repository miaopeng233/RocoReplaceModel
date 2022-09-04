import os
import atexit
import subprocess
import sys
import winreg

# 文件路径
BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))


@atexit.register
def clean():
    # 结束时强制关闭代理
    system_proxy(False, "127.0.0.1", 8080)


def system_proxy(open_or_close, host, port):
    """
        修改系统代理函数
        :param open_or_close: 是否开启 bool
        :param host: IP
        :param port: 端口
        :return:
    """
    proxy = f"{host}:{port}"
    root = winreg.HKEY_CURRENT_USER
    proxy_path = r"Software\Microsoft\Windows\CurrentVersion\Internet Settings"
    kv_Enable = [
        (proxy_path, "ProxyEnable", 1, winreg.REG_DWORD),
        (proxy_path, "ProxyServer", proxy, winreg.REG_SZ),
    ]

    kv_Disable = [
        (proxy_path, "ProxyEnable", 0, winreg.REG_DWORD),
        # (proxy_path, "ProxyServer", proxy, winreg.REG_SZ),
    ]
    if open_or_close:
        kv = kv_Enable
    else:
        kv = kv_Disable
    for keypath, value_name, value, value_type in kv:
        hKey = winreg.CreateKey(root, keypath)
        winreg.SetValueEx(hKey, value_name, 0, value_type, value)


def chink_mitmproxy():
    """
        检测是否安装了 mitmproxy
    :return:
    """
    output = subprocess.Popen(
        ("mitmproxy", "--version"),
        stdout=subprocess.PIPE).stdout
    if 'Mitmproxy' not in output.read().decode(encoding='gbk', errors="ignore"):
        print('检测到您没有安装代理 mitmproxy 将为您安装 mitmproxy')
        os.system(os.path.join(BASE_DIR, "mitmproxy-8.1.1-windows-x64-installer.exe"))


if __name__ == '__main__':
    # 启动时开启系统代理
    system_proxy(True, "127.0.0.1", 8080)
    print("服务已启动，将为您自动替换宠物资源")
    print('*' * 100)
    print("* 如果您是第一次启动，请启动 `证书安装.exe`，证书只需要安装一次 *")
    print('*' * 100)
    os.system(
        r"mitmdump -q -s {}".format(
            os.path.join(BASE_DIR, "script/replace_model.py")
        )
    )
