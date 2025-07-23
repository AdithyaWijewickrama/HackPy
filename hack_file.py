import ctypes
import os
import re
import shlex
import subprocess
import sys

enable_remote_desktop = (r'reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Terminal Server" /v '
                         r'fDenyTSConnections /t REG_DWORD /d 0 /f')
configure_firewall_for_remote_desktop = r'netsh advfirewall firewall set rule group="remote desktop" new enable=Yes'


def get_cmd_out_as_admin(cmd: str) -> str:
    temp_out = os.path.join("admin_cmd_output.txt")
    ps_command = f'{cmd} | Out-File -Encoding UTF8 -FilePath "{temp_out}"'
    try:
        subprocess.run(["powershell", "-Command", ps_command], shell=True)
        if os.path.exists(temp_out):
            with open(temp_out, "r", encoding="utf-8") as f:
                return f.read().strip()
        else:
            return "❌ Output file not found. Script may have failed or been denied admin permission."

    except Exception as e:
        return f"❌ Error running as admin: {e}"


def get_cmd_out(cmd: str) -> str:
    return subprocess.run(shlex.split(cmd), stdout=subprocess.PIPE).stdout.decode('utf-8')


def get_wifi_conf():
    out = get_cmd_out('netsh wlan show profile')
    p = re.findall(': .+', out)
    i = 0
    for v in p:
        p[i] = v.replace(': ', '').replace('\r', '')
        i += 1
    i = 0
    r = {}
    for v in p:
        p[i] = re.findall('Key Content.+:.+', get_cmd_out_as_admin('netsh wlan show profile \"' + v + '\" key=clear'))
        if len(p[i]) > 0:
            p[i] = re.sub('Key Content.+: ', '', p[i][0]).replace('\r', '')
            r[v] = p[i]
        i += 1
    return r


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception as e:
        return e


if __name__ == '__main__':
    if not is_admin():
        print("Relaunching as admin...")
        cmd = f'{__file__}'
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, cmd, None, 1)

    if is_admin():
        while True:
            i = input('''
What do you want?
    Show wifi passwords :p
    Exit    :e

Your answer : '''
                      )
            if i == 'p':
                print(get_wifi_conf())
            elif i == 'e':
                exit(1)
