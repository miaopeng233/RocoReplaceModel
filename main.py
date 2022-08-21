import os
import atexit
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


if __name__ == '__main__':
    # 启动时开启系统代理
    system_proxy(True, "127.0.0.1", 8080)
    print("""服务已启动
默认修改方式 
    有前置宠物 使用前置宠物的模型
    没有前置宠物的 使用相同系别模型
有觉醒默认使用 金牛宫的觉醒 (后续再改)""")
    os.system(
        r"mitmdump -q -s {}".format(
            os.path.join(BASE_DIR, "replace_model.py")
        )
    )
