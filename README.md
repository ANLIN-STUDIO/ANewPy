# ANewPy 新的Python体验感 —— 一个帮助您更好使用 Python 的模块包)

# ANewPy
一个帮助您更好使用 Python 的模块包。 
提供 Pyqt 的便捷函数。
模块包作者 Anlin.Studio。


## ABO 原版加强
ANewPy 会尝试利用重写或调用原版 Python 内置函数的方式使其利用起来更加便捷

### Input
***· 利用 pyautogui 库控制键盘写入以达到以下效果***
 - **__prompt: Any = ''** : 提示信息
 - **default: Any = ''** : 默认输入
 - **wait_time: float | int = 0.1** : 输入默认输入的延迟时间
 - **PromptWriteable: bool = False** : 提示信息是否可编辑

```python
__input = input

def input(__prompt: Any = '', 
          default: Any = '', 
          wait_time: float | int = 0.1, 
          PromptWriteable: bool = False):
    if default != '' or PromptWriteable:
        import threading
        import pyautogui
        import time

        if default != '':
            def __AutoInput(__prompt_2, wait_time_2):
                time.sleep(wait_time_2)
                if PromptWriteable:
                    pyautogui.write(__prompt)
                pyautogui.write(__prompt_2)

            threading.Thread(target=__AutoInput, args=(str(default), wait_time)).start()
    if PromptWriteable:
        raw_input = __input()
    else:
        raw_input = __input(__prompt=__prompt)
    return raw_input
```
### Quit

 - **ForcedClose: bool = False** : 是否强制退出

```python
def quit(ForcedClose: bool = False):
    if ForcedClose:
        # noinspection PyProtectedMember
        os._exit(0)
    else:
        sys.exit()
```
### Open

  - \_\_init__() : **file_path: str** : 文件路径
  - ***def exists(self) -> bool***
	  - 判断文件是否存在
  - ***def read(self, isByte: bool = False, typeLimit: type | None = None, cur_encoding: str | None = None) -> str***
	  - 读取文件
	  - **isByte: bool = False** : 是否以二进制形式打开文件
	  - **typeLimit: type = None** : 文件类型限制
	  - **cur_encoding: str = None** : 锁定文件读取编码
  - ***def create(self) -> None***
	  - 创建文件
  - ***def write(self, content: str, isByte: bool = False, create: bool = True) -> None***
	  - 写入文件
	  - **content: str** : 写入内容
	  - **isByte: bool = False** : 是否以二进制形式打开文件
	  - **create: bool = True** : 若文件不存在是否创建
  - ***def append(self, content: str, position: int = -1, isByte: bool = False, create: bool = False) -> None***
	  - 追加文件
	  - **content: str** : 写入内容
	  - **position: int = -1** : 写入位置
	  -  **isByte: bool = False** : 是否以二进制形式打开文件
	  - **create: bool = False** : 若文件不存在是否创建
  - ***def clear(self) -> None***
 	 - 清空文件

```python
raw_open = open


class TypeWrong(Exception):
    def __str__(self):
        return "You may want to eval a string and you limited it type, but the real type is wrong."


class FileNotExists(Exception):
    def __str__(self):
        return "You may want to open a file, but the path is wrong."


class FileAlreadyExist(Exception):
    def __str__(self):
        return "You may want to create a file, but the file already exist."


class open:
    def __init__(self, file_path: str):
        self.fp = file_path

        self.r = self.read
        self.w = self.write
        self.a = self.append
        self.c = self.clear

    def exists(self):
        return os.path.exists(self.fp)

    def read(self, isByte: bool = False, typeLimit: type = None, cur_encoding: str = None):
        if self.exists():
            if isByte:
                with raw_open(self.fp, 'rb') as reader:
                    _ = reader.read()
                    return _
            else:
                if cur_encoding is None:
                    import chardet
                    with raw_open(self.fp, 'rb') as frb:
                        cur_encoding = chardet.detect(frb.read())['encoding']
                with raw_open(self.fp, 'r', encoding=cur_encoding) as reader:
                    _ = reader.read()
                if typeLimit:
                    _ = eval(_)
                    if isinstance(_, typeLimit):
                        return _
                    else:
                        raise TypeWrong
                else:
                    return _
        else:
            raise FileNotExists

    def create(self):
        if self.exists():
            raise FileAlreadyExist
        else:
            raw_open(self.fp, "w").close()

    def write(self, content: str, isByte: bool = False, create: bool = True):
        if not self.exists():
            if create:
                self.create()
            else:
                raise FileNotExists
            if isByte:
                mode = "wb"
            else:
                mode = "w"
            with raw_open(self.fp, mode) as writer:
                writer.write(content)

    def append(self, content: str, position: int = -1, isByte: bool = False, create: bool = False):
        if not self.exists():
            if create:
                self.create()
            else:
                raise FileNotExists
            _ = self.read(isByte)
            _ = _[:position] + content + _[position:]
            self.write(_, isByte, False)

    def clear(self):
        self.write("")
```


## MORE 更多加强
ANewPy 新增了一些日常可能用到的函数与一些复杂但实用的函数

### Set Input Method 更改输入法
 - **signal: int = en** : 需要切换输入法的[语言十六进制标识符](https://www.cnblogs.com/JCL1101/p/8036771.html)

```python
en = 0x0409
cn = 0x0804

def set_input_method(LanguageHexadecimalIdentifier: int = en):
    from win32con import WM_INPUTLANGCHANGEREQUEST
    hwnd = win32gui.GetForegroundWindow()
    win32gui.GetWindowText(hwnd)
    im_list = win32api.GetKeyboardLayoutList()
    list(map(hex, im_list))
    win32api.SendMessage(hwnd, WM_INPUTLANGCHANGEREQUEST, 0, LanguageHexadecimalIdentifier)
```
### RGB To Hex 颜色三维列表转十六进制
***! paras_checker() 为 ANewPy 的参数限制装饰器, 若没有导入 ANewPy.paras_checker ，可以将其删除***
 - **rgb: list[int] | tuple[int]** : 颜色三维列表（如 [255, 255, 255] 或 (0, 0, 0) 等）

```python
@paras_checker(rgb=[Rule.list_structure, [int, int, int]])
def RGB2Hex(rgb: list[int] | tuple[int]):
    strs = '#'
    for i in rgb:
        num = int(i)
        strs += str(hex(num))[-2:].replace('x', '0').upper()
    return strs
```
### Command 无终端弹窗运行系统指令并获取输出（代替 os.system() ）
 - **cmd: str** : 系统cmd指令（如 shutdown 等）
 - **getReturn: bool = False** : 是否需要收到返回值
 - **encoding: str = "gbk"** : 用于解码返回值的编码

```python
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
```
### Select File 打开文件资源管理器并选中指定的文件
***! 需要 ANewPy.more.command(...)***
 - **file_path: str** : 指定的文件

```python
def SelectFile(file_path: str):
    file_path = file_path.replace('/', '\\')
    command(f'explorer /select, {file_path}')
```
### Check Process 检查进程名是否存在
 - **process_name: str** : 进程名

```python
def check_process(process_name: str):
    import psutil
    for pid in psutil.pids():
        if psutil.Process(pid).name() == process_name:
            if isinstance(pid, int):
                return True
            else:
                return False
    return False
```
### Check Self Running 检查自身进程是否存在，防止多开
***! 无法作用于未编译的源码，因为运行源码的程序是 python(w).exe 而并非自身 .py(w) 文件***
 - **process_name: str** : 进程名

```python
def check_self_running():
    import psutil
    import os
    for pid in psutil.pids():
        if psutil.Process(pid).name() == os.path.split(sys.argv[0])[-1] and pid != os.getpid():
            return True
    return False
```
### Browse 弹出交互窗口，选择文件打开、保存、另存为
 - **mode: bool | int** : 操作文件模式 True为打开，False为保存
 - **file_type_dict: dict[str | list[str] | tuple[str]] = True** : 文件类型 可用字典表达（如 {"图像文件": ["png", "jpg"]} 或 {"图像文件": (".png", ".jpg")} 等） 或 为 True 则为所有文件，为 False 则仅为文件夹
 - **default_name: str = ""** : 文件名称输入框的默认内容，即默认选中的文件
 - **title: str = "选择您的文件"** : 弹出窗口的标题
 - **path: str = "::{20D04FE0-3AEA-1069-A2D8-08002B30309D}"** : 默认的目录（文件夹位置）（需要绝对路径）（默认为此电脑）
 - **->** : ( 是否选择成功, 选择的文件路径, 文件后缀名 ) 或 ( 是否选择成功, 选择的文件夹路径, None )，当弹出的窗口被关闭后 *是否选择成功* 将为 False

```python
def browse(mode: bool | int,
           file_type_dict: dict[str | list[str] | tuple[str]] = True,
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
```
### If Each Item In 判定列表内任意一个元素是否被text包含
***· 只要 items 内的元素之一在 text 中存在即为 True***
 - **text: str** : 需要判定的字符串
 - **items: [list[str] | tuple[str] | dict[str]]** : 用判定的字符串列表、元组、字典键

```python
def if_each_item_in(text: str,
                    items: [list[str] | tuple[str] | dict[str]]):
    for item in items:
        if item in text:
            return True
    return False
```
### Get Desktop Path 获取桌面文件夹路径

```python
def get_desktop_path() -> str:
    import winreg
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                         r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    return winreg.QueryValueEx(key, "Desktop")[0]
```
### Change Registry Right Click Menu 添加右键文件弹出的菜单交互按钮
 - **subkey: str** : 此注册表的键（建议设为按钮作用的英文）
 - **DisplayValue: str** : 菜单交互按钮的文本
 - **hotkey: str = None** : 可以选中此按钮的热键
 - **icon: [str | bool] = True** : 此按钮前的图标（给入 icon 路径字符串 或 为 True 则为本应用程序的图标，或为False则没有图标）

```python
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
```
### Work Area Size 获取桌面工作（非任务栏）区域的大小

```python
def work_area_size():
    monitor_info = win32api.GetMonitorInfo(win32api.MonitorFromPoint((0, 0)))
    work_area = monitor_info.get("Work")
    return work_area[2], work_area[3]
```
### Monitor Area Size 获取桌面任务栏（非工作）区域的大小

```python
def monitor_area_height():
    monitor_info = win32api.GetMonitorInfo(win32api.MonitorFromPoint((0, 0)))
    monitor_area = monitor_info.get("Monitor")
    work_area = monitor_info.get("Work")
    return monitor_area[3] - work_area[3]
```
### Send Msg To Clip 发送数据到剪贴板
***· 操作剪贴板分四步：
    1. 打开剪贴板：OpenClipboard()
    2. 清空剪贴板，新的数据才好写进去：EmptyClipboard()
    3. 往剪贴板写入数据：SetClipboardData()
    4. 关闭剪贴板：CloseClipboard()***
 - **type_data** : 数据的格式，unicode字符通常是传 win32con.CF_UNICODETEXT
 - **msg** : 要写入剪贴板的数据

```python
def send_msg_to_clip(type_data, msg):
    """
    :param type_data: 数据的格式，
    unicode字符通常是传 win32con.CF_UNICODETEXT
    :param msg: 要写入剪贴板的数据
    """
    import win32clipboard
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(type_data, msg)
    win32clipboard.CloseClipboard()
```
### Paste Img 将图片数据粘贴到剪贴板
***! 需要 ANewPy.more.send_msg_to_clip(...)***
***· 图片转换成二进制字符串，然后以位图的格式写入剪贴板，主要思路是用Image模块打开图片，用BytesIO存储图片转换之后的二进制字符串***
 - **file_img: PIL.Image.Image** : 图片的路径

```python
def paste_img(file_img: any):
    """
    :param file_img: PIL.Image.Image | 图片的路径
    """
    from PIL import Image
    from io import BytesIO
    import win32clipboard
    if type(file_img) == Image.Image:
        image = file_img
    else:
        image = Image.open(file_img)
    output = BytesIO()
    image.save(output, 'BMP')
    data = output.getvalue()[14:]
    output.close()
    send_msg_to_clip(win32clipboard.CF_DIB, data)
```
### If Pressed 全局判断标识是否发送信号
 - **wconKey** : window con 按键标识（如 1 为鼠标左键，2为鼠标右键等）

```python
def IfPressed(wconKey):
    import ctypes
    return bool(ctypes.windll.user32.GetAsyncKeyState(wconKey) & 0x8000)
```
### Mouse Pressed 全局判断鼠标是否按下
***! 需要 ANewPy.more.IfPressed(...)***
***· 除了鼠标的上下滚轮，鼠标的按键都能返回 True***

```python
def MousePressed():
    for i in [1, 2, 4, 5, 6]:
        if IfPressed(i):
            return True
    else:
        return False
```
## Control Volume 控制系统声音大小
ANewPy 新增了一些可以操作window系统声音的函数

### 前提
```python
import ctypes
import comtypes
from ctypes import wintypes

MMDeviceApiLib = comtypes.GUID(
    '{2FDAAFA3-7523-4F66-9957-9D5E7FE698F6}')
IID_IMMDevice = comtypes.GUID(
    '{D666063F-1587-4E43-81F1-B948E807363F}')
IID_IMMDeviceCollection = comtypes.GUID(
    '{0BD7A1BE-7A1A-44DB-8397-CC5392387B5E}')
IID_IMMDeviceEnumerator = comtypes.GUID(
    '{A95664D2-9614-4F35-A746-DE8DB63617E6}')
IID_IAudioEndpointVolume = comtypes.GUID(
    '{5CDF2C82-841E-4546-9722-0CF74078229A}')
CLSID_MMDeviceEnumerator = comtypes.GUID(
    '{BCDE0395-E52F-467C-8E3D-C4579291692E}')

# EDataFlow
eRender = 0  # audio rendering stream
eCapture = 1  # audio capture stream
eAll = 2  # audio rendering or capture stream

# ERole
eConsole = 0  # games, system sounds, and voice commands
eMultimedia = 1  # music, movies, narration
eCommunications = 2  # voice communications

LPCGUID = REFIID = ctypes.POINTER(comtypes.GUID)
LPFLOAT = ctypes.POINTER(ctypes.c_float)
LPDWORD = ctypes.POINTER(wintypes.DWORD)
LPUINT = ctypes.POINTER(wintypes.UINT)
LPBOOL = ctypes.POINTER(wintypes.BOOL)
PIUnknown = ctypes.POINTER(comtypes.IUnknown)


class IMMDevice(comtypes.IUnknown):
    _iid_ = IID_IMMDevice
    _methods_ = (
        comtypes.COMMETHOD([], ctypes.HRESULT, 'Activate',
                           (['in'], REFIID, 'iid'),
                           (['in'], wintypes.DWORD, 'dwClsCtx'),
                           (['in'], LPDWORD, 'pActivationParams', None),
                           (['out', 'retval'], ctypes.POINTER(PIUnknown), 'ppInterface')),
        comtypes.STDMETHOD(ctypes.HRESULT, 'OpenPropertyStore', []),
        comtypes.STDMETHOD(ctypes.HRESULT, 'GetId', []),
        comtypes.STDMETHOD(ctypes.HRESULT, 'GetState', []))


PIMMDevice = ctypes.POINTER(IMMDevice)


class IMMDeviceCollection(comtypes.IUnknown):
    _iid_ = IID_IMMDeviceCollection


PIMMDeviceCollection = ctypes.POINTER(IMMDeviceCollection)


class IMMDeviceEnumerator(comtypes.IUnknown):
    _iid_ = IID_IMMDeviceEnumerator
    _methods_ = (
        comtypes.COMMETHOD([], ctypes.HRESULT, 'EnumAudioEndpoints',
                           (['in'], wintypes.DWORD, 'dataFlow'),
                           (['in'], wintypes.DWORD, 'dwStateMask'),
                           (['out', 'retval'], ctypes.POINTER(PIMMDeviceCollection),
                            'ppDevices')),
        comtypes.COMMETHOD([], ctypes.HRESULT, 'GetDefaultAudioEndpoint',
                           (['in'], wintypes.DWORD, 'dataFlow'),
                           (['in'], wintypes.DWORD, 'role'),
                           (['out', 'retval'], ctypes.POINTER(PIMMDevice), 'ppDevices')))

    @classmethod
    def get_default(cls, dataFlow, role):
        enumerator = comtypes.CoCreateInstance(
            CLSID_MMDeviceEnumerator, cls, comtypes.CLSCTX_INPROC_SERVER)
        return enumerator.GetDefaultAudioEndpoint(dataFlow, role)


class IAudioEndpointVolume(comtypes.IUnknown):
    _iid_ = IID_IAudioEndpointVolume
    _methods_ = (
        comtypes.STDMETHOD(ctypes.HRESULT, 'RegisterControlChangeNotify', []),
        comtypes.STDMETHOD(ctypes.HRESULT, 'UnregisterControlChangeNotify', []),
        comtypes.COMMETHOD([], ctypes.HRESULT, 'GetChannelCount',
                           (['out', 'retval'], LPUINT, 'pnChannelCount')),
        comtypes.COMMETHOD([], ctypes.HRESULT, 'SetMasterVolumeLevel',
                           (['in'], ctypes.c_float, 'fLevelDB'),
                           (['in'], LPCGUID, 'pguidEventContext', None)),
        comtypes.COMMETHOD([], ctypes.HRESULT, 'SetMasterVolumeLevelScalar',
                           (['in'], ctypes.c_float, 'fLevel'),
                           (['in'], LPCGUID, 'pguidEventContext', None)),
        comtypes.COMMETHOD([], ctypes.HRESULT, 'GetMasterVolumeLevel',
                           (['out', 'retval'], LPFLOAT, 'pfLevelDB')),
        comtypes.COMMETHOD([], ctypes.HRESULT, 'GetMasterVolumeLevelScalar',
                           (['out', 'retval'], LPFLOAT, 'pfLevel')),
        comtypes.COMMETHOD([], ctypes.HRESULT, 'SetChannelVolumeLevel',
                           (['in'], wintypes.UINT, 'nChannel'),
                           (['in'], ctypes.c_float, 'fLevelDB'),
                           (['in'], LPCGUID, 'pguidEventContext', None)),
        comtypes.COMMETHOD([], ctypes.HRESULT, 'SetChannelVolumeLevelScalar',
                           (['in'], wintypes.UINT, 'nChannel'),
                           (['in'], ctypes.c_float, 'fLevel'),
                           (['in'], LPCGUID, 'pguidEventContext', None)),
        comtypes.COMMETHOD([], ctypes.HRESULT, 'GetChannelVolumeLevel',
                           (['in'], wintypes.UINT, 'nChannel'),
                           (['out', 'retval'], LPFLOAT, 'pfLevelDB')),
        comtypes.COMMETHOD([], ctypes.HRESULT, 'GetChannelVolumeLevelScalar',
                           (['in'], wintypes.UINT, 'nChannel'),
                           (['out', 'retval'], LPFLOAT, 'pfLevel')),
        comtypes.COMMETHOD([], ctypes.HRESULT, 'SetMute',
                           (['in'], wintypes.BOOL, 'bMute'),
                           (['in'], LPCGUID, 'pguidEventContext', None)),
        comtypes.COMMETHOD([], ctypes.HRESULT, 'GetMute',
                           (['out', 'retval'], LPBOOL, 'pbMute')),
        comtypes.COMMETHOD([], ctypes.HRESULT, 'GetVolumeStepInfo',
                           (['out', 'retval'], LPUINT, 'pnStep'),
                           (['out', 'retval'], LPUINT, 'pnStepCount')),
        comtypes.COMMETHOD([], ctypes.HRESULT, 'VolumeStepUp',
                           (['in'], LPCGUID, 'pguidEventContext', None)),
        comtypes.COMMETHOD([], ctypes.HRESULT, 'VolumeStepDown',
                           (['in'], LPCGUID, 'pguidEventContext', None)),
        comtypes.COMMETHOD([], ctypes.HRESULT, 'QueryHardwareSupport',
                           (['out', 'retval'], LPDWORD, 'pdwHardwareSupportMask')),
        comtypes.COMMETHOD([], ctypes.HRESULT, 'GetVolumeRange',
                           (['out', 'retval'], LPFLOAT, 'pfLevelMinDB'),
                           (['out', 'retval'], LPFLOAT, 'pfLevelMaxDB'),
                           (['out', 'retval'], LPFLOAT, 'pfVolumeIncrementDB')))

    @classmethod
    def get_default(cls):
        endpoint = IMMDeviceEnumerator.get_default(eRender, eMultimedia)
        interface = endpoint.Activate(cls._iid_, comtypes.CLSCTX_INPROC_SERVER)
        return ctypes.cast(interface, ctypes.POINTER(cls))


ev = IAudioEndpointVolume.get_default()


def getMasterVolumeLevel():
    return ev.GetMasterVolumeLevel()


def getMasterVolumeLevelScalar():
    return ev.GetMasterVolumeLevelScalar()


def getVolume():
    return ev.GetMasterVolumeLevelScalar()


def getVolumeStepInfo():
    return ev.GetVolumeStepInfo()


def volumeStepUp():
    ev.VolumeStepUp()


def volumeStepDown():
    ev.VolumeStepDown()


def setMasterVolumeLevelScalar(k):
    ev.SetMasterVolumeLevelScalar(k)


def setVolume(k):
    ev.SetMasterVolumeLevelScalar(k)
```
### getVolume() 获取系统音量
***return 0 <= k <= 1***

```python
def getVolume() -> float:
    return ev.GetMasterVolumeLevelScalar()
```
### volumeStepUp() 增加系统音量
***· 等效于 Fn 调节音量***

```python
def volumeStepUp():
    ev.VolumeStepUp()
```
### volumeStepDown() 减少系统音量
***· 等效于 Fn 调节音量***

```python
def volumeStepDown():
    ev.VolumeStepDown()
```
### setVolume() 设置系统音量
***0 <= k <= 1***
 - **k: int** : 于 0 到 1 之间的音量系数

```python
def setVolume(k: int):
    ev.SetMasterVolumeLevelScalar(k)
```
## Para Checker 检测给入函数的参数是否符合规则
ANewPy 新增了一些可以检测给入函数的参数是否符合规则的修饰器和函数

### 前提

```python
def para_checker(para_single_rule: any, paras: list[str], *args_rule_paras):
    def wrapper(func):
        def __(*args, **kwargs):
            for i in paras:
                func_para = func.__code__.co_varnames[:func.__code__.co_argcount]
                if i in func_para:
                    idx = func_para.index(i)
                    # kwargs check
                    if i in kwargs.keys():
                        if args_rule_paras:
                            para_single_rule(kwargs[i], i, args_rule_paras)
                        else:
                            para_single_rule(kwargs[i], i)
                            # positional check
                    elif args.__len__() - 1 >= idx:
                        if args_rule_paras:
                            para_single_rule(args[idx], i, args_rule_paras)
                        else:
                            para_single_rule(args[idx], i)
                    # default para check
                    else:
                        pos = idx - func_para.__len__()
                        if func.__defaults__.__len__() >= pos:
                            if args_rule_paras:
                                para_single_rule(func.__defaults__[pos], i, args_rule_paras)
                            else:
                                para_single_rule(func.__defaults__[pos], i)
            return func(*args, **kwargs)

        return __

    return wrapper


def paras_checker(**kwparas):
    def wrapper(func):
        def __(*args, **kwargs):
            paras = kwparas.keys()
            for para in paras:
                value = kwparas[para]
                if isinstance(value, list | tuple):
                    value: list | tuple
                    para_single_rule = value.pop(0)
                    args_rule_paras = value
                else:
                    para_single_rule = value
                    args_rule_paras = False
                func_para = func.__code__.co_varnames[:func.__code__.co_argcount]
                if para in func_para:
                    idx = func_para.index(para)
                    # kwargs check
                    if para in kwargs.keys():
                        if args_rule_paras:
                            para_single_rule(kwargs[para], para, args_rule_paras)
                        else:
                            para_single_rule(kwargs[para], para)
                            # positional check
                    elif args.__len__() - 1 >= idx:
                        if args_rule_paras:
                            para_single_rule(args[idx], para, args_rule_paras)
                        else:
                            para_single_rule(args[idx], para)
                    # default para check
                    else:
                        pos = idx - func_para.__len__()
                        if func.__defaults__.__len__() >= pos:
                            if args_rule_paras:
                                para_single_rule(func.__defaults__[pos], para, args_rule_paras)
                            else:
                                para_single_rule(func.__defaults__[pos], para)
            return func(*args, **kwargs)

        return __

    return wrapper


def if_value_in_range(test_int: int, range_: str):
    """"∞", "infinity" or "i" all indicate positive infinity.
    Add "-" before them to indicate negative infinity.
    "(" and ")" means not to take this value; "[" and "]" means to take this value.
    Closed loop formed between brackets.
    Separate two values with ", "(comma+space) or ","(comma).

    "∞"、"infinity"或"i"都表示正无穷大。
    在它们前面加上"-"表示负无穷大。
    "("和")"表示不取此值；"["和"]"表示取此值。
    括号之间形成闭环。
    用", "（逗号+空格）或","（逗号）分隔两个值。

    · For example:
    > @para_checker(Rule.value_range, ['a'], '(i, 0]')
    > def test(a: int):
    >   print(a)
    · 当 a 大于等于 0 时不报错
    """
    range_ = range_.replace('infinity', '∞').replace('i', '∞').replace(', ', ',')
    try:
        if '(' in range_:
            the_max = (False, range_[1:].split(',')[0])
        elif '[' in range_:
            the_max = (True, range_[1:].split(',')[0])
        else:
            assert False
        if ')' in range_:
            the_min = (False, range_[:-1].split(',')[1])
        elif ']' in range_:
            the_min = (True, range_[:-1].split(',')[1])
        else:
            assert False
        if the_max[1] != '∞':
            int(the_max[1])
        if the_min[1] == '∞':
            the_min = (the_min[0], '-∞')
        if the_min[1] != '-∞':
            int(the_min[1])
        assert isinstance(test_int, int)
    except Exception as e:
        assert False, \
            f'Incorrect parameter structure passed in ({e})'
    if not (the_max[1] == '∞' or the_min[1] == '-∞'):
        assert (the_max[1] == the_min[1] and the_max[0] and the_min[0]) or (the_max[1] > the_min[1]), \
            'The maximum value should be greater than the minimum value'
    if the_max[1] == '∞':
        if the_min[1] != '-∞':
            if the_min[0]:
                if not test_int >= int(the_min[1]):
                    return False
            else:
                if not test_int > int(the_min[1]):
                    return False
    elif the_min[1] == '-∞':
        if the_max[1] != '∞':
            if the_max[0]:
                if not int(the_max[1]) >= test_int:
                    return False
            else:
                if not int(the_max[1]) > test_int:
                    return False
    else:
        if the_max[0]:
            if the_min[0]:
                if not int(the_max[1]) >= test_int >= int(the_min[1]):
                    return False
            else:
                if not int(the_max[1]) >= test_int > int(the_min[1]):
                    return False
        else:
            if the_min[0]:
                if not int(the_max[1]) > test_int >= int(the_min[1]):
                    return False
            else:
                if not int(the_max[1]) > test_int > int(the_min[1]):
                    return False
    return True


class Rule(object):
    @staticmethod
    def __positional_arguments(name: str, args: tuple, expected_quantity: int):
        assert len(args) == expected_quantity, \
            f'Rule.{name}() takes {expected_quantity} positional arguments but {len(args)} were given'
        if len(args) == 0:
            return None
        elif len(args) == 1:
            return args[0]
        elif len(args) > 1:
            return args

    @staticmethod
    def __notNone(x, i, *args):
        Rule.__positional_arguments('notNone', args, 0)
        assert x is not None, \
            f'\"{i}\" should not take None'

    notNone = __notNone

    @staticmethod
    def __notTure(x, i, RelativeAndAbsolute):
        """:RelativeAndAbsolute:
        "True" is absolute True
        "False" is relative True"""
        Rule.__positional_arguments('notTure', RelativeAndAbsolute, 1)
        if bool(RelativeAndAbsolute[0]):
            assert x is not True, \
                f'\"{i}\" should not take Ture'
        else:
            assert not x, \
                f'\"{i}\" should not take Ture'

    notTrue = __notTure

    @staticmethod
    def __notFalse(x, i, RelativeAndAbsolute):
        """:RelativeAndAbsolute:
        "True" is absolute False
        "False" is relative False"""
        Rule.__positional_arguments('notTure', RelativeAndAbsolute, 1)
        if bool(RelativeAndAbsolute[0]):
            assert x is not False, \
                f'\"{i}\" should not take False'
        else:
            assert x, \
                f'\"{i}\" should not take False'

    notFalse = __notFalse

    @staticmethod
    def __value_range(x, i, range_: tuple[str]):
        """"∞", "infinity" or "i" all indicate positive infinity.
        Add "-" before them to indicate negative infinity.
        "(" and ")" means not to take this value; "[" and "]" means to take this value.
        Closed loop formed between brackets.
        Separate two values with ", "(comma+space) or ","(comma).

        "∞"、"infinity"或"i"都表示正无穷大。
        在它们前面加上"-"表示负无穷大。
        "("和")"表示不取此值；"["和"]"表示取此值。
        括号之间形成闭环。
        用", "（逗号+空格）或","（逗号）分隔两个值。

        · For example:
        > @para_checker(Rule.value_range, ['a'], '(i, 0]')
        > def test(a: int):
        >     print(a)
        · 当 a 大于等于 0 时不报错
        """
        range_ = Rule.__positional_arguments('value_range', range_, 1) \
            .replace('infinity', '∞') \
            .replace('i', '∞') \
            .replace(', ', ',')
        try:
            if '(' in range_:
                the_max = (False, range_[1:].split(',')[0])
            elif '[' in range_:
                the_max = (True, range_[1:].split(',')[0])
            else:
                assert False
            if ')' in range_:
                the_min = (False, range_[:-1].split(',')[1])
            elif ']' in range_:
                the_min = (True, range_[:-1].split(',')[1])
            else:
                assert False
            if the_max[1] != '∞':
                int(the_max[1])
            if the_min[1] == '∞':
                the_min = (the_min[0], '-∞')
                range_ = f"{range_[:-1].split(',')[0]},-∞)"
            if the_min[1] != '-∞':
                int(the_min[1])
            assert isinstance(x, int)
        except Exception as e:
            assert False, \
                f'Incorrect parameter structure passed in ({e})'
        if not (the_max[1] == '∞' or the_min[1] == '-∞'):
            assert (the_max[1] == the_min[1] and the_max[0] and the_min[0]) or (the_max[1] > the_min[1]), \
                'The maximum value should be greater than the minimum value'
        if the_max[1] == '∞':
            range_ = range_.replace('[', '(')
        if the_min[1] == '-∞':
            range_ = range_.replace(']', ')')
        error = f'\"{i}\" should be in the range {range_}'
        if the_max[1] == '∞':
            if the_min[1] != '-∞':
                if the_min[0]:
                    assert x >= int(the_min[1]), \
                        error
                else:
                    assert x > int(the_min[1]), \
                        error
        elif the_min[1] == '-∞':
            if the_max[1] != '∞':
                if the_max[0]:
                    assert int(the_max[1]) >= x, \
                        error
                else:
                    assert int(the_max[1]) > x, \
                        error
        else:
            if the_max[0]:
                if the_min[0]:
                    assert int(the_max[1]) >= x >= int(the_min[1]), \
                        error
                else:
                    assert int(the_max[1]) >= x > int(the_min[1]), \
                        error
            else:
                if the_min[0]:
                    assert int(the_max[1]) > x >= int(the_min[1]), \
                        error
                else:
                    assert int(the_max[1]) > x > int(the_min[1]), \
                        error

    value_range = __value_range

    @staticmethod
    def __list_structure(x, i, structure: tuple[list[type] | tuple[type]]):
        """
        not only "list", but also "tuple"
        The passed in parameters must be in the format you specify.
        One more element, one less element and change a kind of element all cannot pass.
        """
        structure = Rule.__positional_arguments('list_structure', structure, 1)
        assert isinstance(x, list | tuple), \
            f'\"{i}\" must be a list or tuple'
        assert len(x) == len(structure), \
            f'The length of \"{i}\" must be the same as that of \"structure\"({structure})'
        for each_type in range(len(structure)):
            assert isinstance(x[each_type], structure[each_type]), \
                f"The {each_type + 1}-th element, \"{i}\"({x[each_type]}: {type(x[each_type])}) is different from \"structure\"{structure[each_type]}"

    list_structure = __list_structure

```
## Pyqtpro 提供 Pyqt 的便捷函数
ANewPy 新增了一些关于 Pyqt 使用中的便捷函数

### Pyqtpro
Pyqtpro 的主代码
#### Connect 为信号槽绑定函数
 - **signal: pyqtSignal** : Pyqt 信号槽（如 button.clicked 等）
 - **function: function** : 运行的函数

```python
def connect(signal: any,
            function: any):
    """
    :param signal: pyqtSignal
    :param function: function
    :return: None
    """
    signal.connect(function)
```
#### Button Connect 为按钮信号槽绑定函数
 - **PushButton: QPushButton** : Pyqt 按钮控件
 - **function: function** : 运行的函数

```python
def BConnect(PushButton: QPushButton,
             function: any
             ):
    connect(PushButton.clicked, function)
```
#### Create Timer 快速创建计时器并绑定函数
 - **self: QWidget** : Pyqt 窗口控件（一般为代码中的 self）
 - **msec: int** : 每次运行的毫秒间隔
 - **function: any** : 运行的函数

```python
def CTimer(self: QWidget,
           msec: int,
           function: any):
    from PyQt5.QtCore import QTimer
    timer = QTimer(self)
    timer.start(msec)
    connect(timer.timeout, function)
    return timer
```
#### Kill Timer 快速击杀计时器
 - **self: QWidget** : Pyqt 窗口控件（一般为代码中的 self）

```python
def KTimer(self: QWidget):
    self.timer.killTimer(self.timer.timerId())
```
#### Screensize 获取屏幕分辨率

```python
def screensize():
    desktop = QApplication.desktop()
    return desktop.width(), desktop.height()
```
### Window Effect 窗口效果
为您的窗口添加毛玻璃、亚克力等效果
#### 前提

```python
from ctypes import POINTER, c_bool, sizeof, windll, pointer, c_int, Structure
from ctypes.wintypes import DWORD, ULONG
import ANewPy
import win32api
import win32gui
from win32.lib import win32con
from enum import Enum


class WINDOWCOMPOSITIONATTRIB(Enum):
    WCA_UNDEFINED = 0,
    WCA_NCRENDERING_ENABLED = 1,
    WCA_NCRENDERING_POLICY = 2,
    WCA_TRANSITIONS_FORCEDISABLED = 3,
    WCA_ALLOW_NCPAINT = 4,
    WCA_CAPTION_BUTTON_BOUNDS = 5,
    WCA_NONCLIENT_RTL_LAYOUT = 6,
    WCA_FORCE_ICONIC_REPRESENTATION = 7,
    WCA_EXTENDED_FRAME_BOUNDS = 8,
    WCA_HAS_ICONIC_BITMAP = 9,
    WCA_THEME_ATTRIBUTES = 10,
    WCA_NCRENDERING_EXILED = 11,
    WCA_NCADORNMENTINFO = 12,
    WCA_EXCLUDED_FROM_LIVEPREVIEW = 13,
    WCA_VIDEO_OVERLAY_ACTIVE = 14,
    WCA_FORCE_ACTIVEWINDOW_APPEARANCE = 15,
    WCA_DISALLOW_PEEK = 16,
    WCA_CLOAK = 17,
    WCA_CLOAKED = 18,
    WCA_ACCENT_POLICY = 19,
    WCA_FREEZE_REPRESENTATION = 20,
    WCA_EVER_UNCLOAKED = 21,
    WCA_VISUAL_OWNER = 22,
    WCA_LAST = 23


class ACCENT_STATE(Enum):
    """ 客户区状态枚举类 """
    ACCENT_DISABLED = 0,
    ACCENT_ENABLE_GRADIENT = 1,
    ACCENT_ENABLE_TRANSPARENTGRADIENT = 2,
    ACCENT_ENABLE_BLURBEHIND = 3,  # Aero效果
    ACCENT_ENABLE_ACRYLICBLURBEHIND = 4,  # 亚克力效果
    ACCENT_INVALID_STATE = 5


class ACCENT_POLICY(Structure):
    """ 设置客户区的具体属性 """
    _fields_ = [
        ('AccentState', DWORD),
        ('AccentFlags', DWORD),
        ('GradientColor', DWORD),
        ('AnimationId', DWORD),
    ]


class WINDOWCOMPOSITIONATTRIBDATA(Structure):
    _fields_ = [
        ('Attribute', DWORD),
        ('Data', POINTER(ACCENT_POLICY)),  # POINTER()接收任何ctypes类型，并返回一个指针类型
        ('SizeOfData', ULONG),
    ]


class WindowEffect:
    """ 调用windows api实现窗口效果 """

    def __init__(self):
        # 调用api
        self.SetWindowCompositionAttribute = windll.user32.SetWindowCompositionAttribute
        self.SetWindowCompositionAttribute.restype = c_bool
        self.SetWindowCompositionAttribute.argtypes = [
            c_int, POINTER(WINDOWCOMPOSITIONATTRIBDATA)]
        # 初始化结构体
        self.accentPolicy = ACCENT_POLICY()
        self.winCompAttrData = WINDOWCOMPOSITIONATTRIBDATA()
        self.winCompAttrData.Attribute = WINDOWCOMPOSITIONATTRIB.WCA_ACCENT_POLICY.value[0]
        self.winCompAttrData.SizeOfData = sizeof(self.accentPolicy)
        self.winCompAttrData.Data = pointer(self.accentPolicy)

    @ANewPy.paras_checker(gradientColor=[ANewPy.Rule.list_structure, [int, int, int, int]])
    def setAcrylicEffect(self, hWnd: int, gradientColor: list | tuple = (0, 0, 0, 155),
                         isEnableShadow: bool = True, animationId: int = 0):
        """ 开启亚克力效果

        Parameters
        ----------
        hWnd: int
            窗口句柄

        gradientColor: str
             十六进制亚克力混合色，对应 RGBA 四个分量

        isEnableShadow: bool
            是否启用窗口阴影

        animationId: int
            控制磨砂动画
        """
        # 亚克力混合色
        gradientColor = ANewPy.RGB_to_Hex(gradientColor[:-1])[1:] + str(gradientColor[-1])
        gradientColor = gradientColor[6:] + gradientColor[4:6] + gradientColor[2:4] + gradientColor[:2]
        gradientColor = DWORD(int(gradientColor, base=16))
        # 磨砂动画
        animationId = DWORD(animationId)
        # 窗口阴影
        accentFlags = DWORD(0x20 | 0x40 | 0x80 |
                            0x100) if isEnableShadow else DWORD(0)
        self.accentPolicy.AccentState = ACCENT_STATE.ACCENT_ENABLE_ACRYLICBLURBEHIND.value[0]
        self.accentPolicy.GradientColor = gradientColor
        self.accentPolicy.AccentFlags = accentFlags
        self.accentPolicy.AnimationId = animationId
        # 开启亚克力
        self.SetWindowCompositionAttribute(hWnd, pointer(self.winCompAttrData))

    def setAeroEffect(self, hWnd: int):
        """ 开启 Aero 效果

        Parameter
        ----------
        hWnd: int
            窗口句柄
        """
        self.accentPolicy.AccentState = ACCENT_STATE.ACCENT_ENABLE_BLURBEHIND.value[0]
        # 开启Aero
        self.SetWindowCompositionAttribute(hWnd, pointer(self.winCompAttrData))
```
#### Get Window Id 获取窗口ID
 - **self: QWidget** : Pyqt 窗口控件（一般为代码中的 self）
```python
def getWinId(self: QWidget):
    return int(self.winId())
```
#### Acrylic Effect Preposition 开启亚克力效果
***! paras_checker() 为 ANewPy 的参数限制装饰器, 若没有导入 ANewPy.paras_checker ，可以将其删除***
***! 需要 ANewPy.pyqtpro.windowEffect.getWinId(...)***
 - **self: QWidget** : Pyqt 窗口控件（一般为代码中的 self）
 - **self, gradientColor: list | tuple = (0, 0, 0, 155)** : 亚克力效果的混合色颜色与透明度
 - **isEnableShadow: bool = True** : 是否启用窗口阴影
 - **animationId: int = 0** : 控制磨砂动画

```python
@ANewPy.paras_checker(gradientColor=[ANewPy.Rule.list_structure, (int, int, int, int)])
def AcrylicEffectPreposition(self: QWidget, gradientColor: list | tuple = (0, 0, 0, 155),
                             isEnableShadow: bool = True, animationId: int = 0):
    self.setStyleSheet(f"{self.styleSheet()} background:transparent")
    WindowEffect().setAcrylicEffect(getWinId(self), gradientColor, isEnableShadow, animationId)
```
#### Aero Effect Preposition 开启毛玻璃效果
***! 需要 ANewPy.pyqtpro.windowEffect.getWinId(...)***
 - **self: QWidget** : Pyqt 窗口控件（一般为代码中的 self）

```python
def AeroEffectPreposition(self):
    self.setStyleSheet(f"{self.styleSheet()} background:transparent")
    WindowEffect().setAeroEffect(getWinId(self))
```
# 最后
ANewPy正在不断扩大、修复与添加，争取越做越好。
若您在代码中发现错误，或在我的描述中发现漏洞，或您对某处有某些见解，欢迎在评论区下方留言讨论。
制作不易，望点赞、收藏。
