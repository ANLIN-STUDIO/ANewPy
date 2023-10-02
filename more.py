import os
import sys

from typing import Any
import win32api
import win32gui
from ANewPy.para_checker import *

en = 0x0409
cn = 0x0804


def set_input_method(LanguageHexadecimalIdentifier: int = en):
    from win32con import WM_INPUTLANGCHANGEREQUEST
    hwnd = win32gui.GetForegroundWindow()
    win32gui.GetWindowText(hwnd)
    im_list = win32api.GetKeyboardLayoutList()
    list(map(hex, im_list))
    win32api.SendMessage(hwnd, WM_INPUTLANGCHANGEREQUEST, 0, LanguageHexadecimalIdentifier)


@paras_checker(rgb=[Rule.list_structure, [int, int, int]])
def RGB2Hex(rgb: list[int] | tuple[int]):
    strs = '#'
    for i in rgb:
        num = int(i)
        strs += str(hex(num))[-2:].replace('x', '0').upper()
    return strs


def command(cmd: str, getReturn: bool = False, encoding: str = "gbk"):
    import subprocess
    if getReturn:
        return subprocess.Popen(cmd,
                                shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, encoding=encoding).communicate()[0]
    else:
        __si = subprocess.STARTUPINFO()
        __si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        subprocess.call(cmd, startupinfo=__si)


def SelectFile(file_path: str):
    import subprocess
    file_path = file_path.replace('/', '\\')
    subprocess.Popen(f'explorer /select ,\"{file_path}\"',
                     shell=True, stdout=subprocess.PIPE,
                     stderr=subprocess.STDOUT).communicate()[0]


def check_process(process_name: str):
    import psutil
    for pid in psutil.pids():
        if psutil.Process(pid).name() == process_name:
            if isinstance(pid, int):
                return True
            else:
                return False
    return False


def check_self_running():
    import psutil
    import os
    for pid in psutil.pids():
        if psutil.Process(pid).name() == os.path.split(sys.argv[0])[-1] and pid != os.getpid():
            return True
    return False


def browse(mode: bool | int,
           file_type_dict: dict[str | list[str] | tuple[str]] | bool = True,
           default_name: str = "",
           title: str = "选择您的文件",
           path: str = "::{20D04FE0-3AEA-1069-A2D8-08002B30309D}") -> tuple[bool, str, str]:
    """
    -> (if_pass, filename, fileExt) or (if_pass, dirname, None)
    :param mode:  True: open; False: save
    :param file_type_dict:
        1. {"图像文件": ["png", "jpg"]} or {"图像文件": (".png", ".jpg")};
        2. True: Selector supports all files;
        3. False: Selector only supports folders.
    """
    import os
    import win32con
    import win32ui
    if file_type_dict is None:
        file_type_dict = {"所有文件": "*"}
    file_type = ""
    if file_type_dict is True:
        file_type = "所有文件|*.*|"
    elif file_type_dict is False:
        file_type = "文件夹|*.|"
        if default_name == "":
            default_name = "选择一个文件夹"
    else:
        for each_file_type in file_type_dict:
            type_ = file_type_dict[each_file_type]
            if isinstance(type_, str):
                if type_.startswith("."):
                    type_ = type_[1:]
                file_type += f'{each_file_type}(*.{type_})|*.{type_}|'
            elif isinstance(type_, list | tuple):
                file_type += f'{each_file_type}('
                for each_type in type_:
                    if each_type.startswith("."):
                        each_type = each_type[1:]
                    file_type += f'*.{each_type};'
                file_type += ')|'
                for each_type in type_:
                    if each_type.startswith("."):
                        each_type = each_type[1:]
                    file_type += f'*.{each_type};'
                file_type += '|'
    API_flag = win32con.OFN_OVERWRITEPROMPT | win32con.OFN_FILEMUSTEXIST
    dlg = win32ui.CreateFileDialog(mode, None, default_name, API_flag, file_type)
    dlg.SetOFNTitle(title)
    dlg.SetOFNInitialDir(path)
    dlg.DoModal()
    if file_type_dict is False:
        filename = os.path.split(dlg.GetPathName())[0]
        fileExt = None
    else:
        filename = dlg.GetPathName()
        fileExt = dlg.GetFileExt()
    if os.path.exists(filename):
        if_pass = True
    elif not mode:
        if os.path.split(filename)[0] == '':
            if_pass = False
        else:
            if_pass = True
    else:
        if_pass = False
    return if_pass, filename, fileExt


def if_each_item_in(text: str,
                    items: [list[str] | tuple[str] | dict[str]]):
    for item in items:
        if item in text:
            return True
    return False


def get_desktop_path() -> str:
    import winreg
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                         r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    return winreg.QueryValueEx(key, "Desktop")[0]


def C_REG_RightClickMenu(subkey: str,
                         DisplayValue: str,
                         hotkey: str = None,
                         icon: [str | bool] = True):
    """
    icon
    |   str: icon_path;
    |   True: __file__(Icon of this file);
    |   False: No Icon.
    """
    import win32con
    import win32api
    from win32ctypes.pywin32 import pywintypes

    reg_path = fr"*\shell\{subkey}"
    try:
        win32api.RegOpenKey(win32con.HKEY_CLASSES_ROOT, reg_path, 0, win32con.KEY_READ)
        return False
    except pywintypes.error:
        key = win32api.RegCreateKey(win32con.HKEY_CLASSES_ROOT, reg_path)
        if hotkey is not None:
            DisplayValue += f" (&{hotkey})"
        win32api.RegSetValue(key, '', win32con.REG_SZ, DisplayValue)
        if icon is not False:
            if icon is True:
                icon = __file__
            win32api.RegSetValueEx(key, "Icon", 0, win32con.REG_SZ, icon)
        win32api.RegSetValue(key, 'command', win32con.REG_SZ, f"\"{__file__}\" \"%1\"")
        win32api.RegCloseKey(key)
        return True


def work_area_size():
    monitor_info = win32api.GetMonitorInfo(win32api.MonitorFromPoint((0, 0)))
    work_area = monitor_info.get("Work")
    return work_area[2], work_area[3]


def monitor_area_height():
    monitor_info = win32api.GetMonitorInfo(win32api.MonitorFromPoint((0, 0)))
    monitor_area = monitor_info.get("Monitor")
    work_area = monitor_info.get("Work")
    return monitor_area[3] - work_area[3]


def send_msg_to_clip(type_data, msg):
    """
    操作剪贴板分四步：
    1. 打开剪贴板：OpenClipboard()
    2. 清空剪贴板，新的数据才好写进去：EmptyClipboard()
    3. 往剪贴板写入数据：SetClipboardData()
    4. 关闭剪贴板：CloseClipboard()

    :param type_data: 数据的格式，
    unicode字符通常是传 win32con.CF_UNICODETEXT
    :param msg: 要写入剪贴板的数据
    """
    import win32clipboard
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(type_data, msg)
    win32clipboard.CloseClipboard()


def paste_img(file_img: any):
    """
    图片转换成二进制字符串，然后以位图的格式写入剪贴板

    主要思路是用Image模块打开图片，
    用BytesIO存储图片转换之后的二进制字符串

    :param file_img: PIL.Image.Image | 图片的路径
    """
    from PIL import Image
    from io import BytesIO
    import win32clipboard
    if type(file_img) == Image.Image:
        image = file_img
    else:
        # 把图片写入image变量中
        # 用open函数处理后，图像对象的模式都是 RGB
        image = Image.open(file_img)

    # 声明output字节对象
    output = BytesIO()

    # 用BMP (Bitmap) 格式存储
    # 这里是位图，然后用output字节对象来存储
    image.save(output, 'BMP')

    # BMP图片有14字节的header，需要额外去除
    data = output.getvalue()[14:]

    # 关闭
    output.close()

    # DIB: 设备无关位图(device-independent bitmap)，名如其意
    # BMP的图片有时也会以.DIB和.RLE作扩展名
    # 设置好剪贴板的数据格式，再传入对应格式的数据，才能正确向剪贴板写入数据
    send_msg_to_clip(win32clipboard.CF_DIB, data)


def MousePressed():
    for i in [1, 2, 4, 5, 6]:
        if IfPressed(i):
            return True
    else:
        return False


def IfPressed(wconKey):
    import ctypes
    return bool(ctypes.windll.user32.GetAsyncKeyState(wconKey) & 0x8000)
