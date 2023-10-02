import sys
import os
from builtins import *
from typing import Any


__input = input
raw_open = open


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


def quit(ForcedClose: bool = False,
         todo: Any = None):
    if ForcedClose:
        # noinspection PyProtectedMember
        os._exit(0)
    else:
        sys.exit()


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


class Path:
    def __init__(self,
                 path: str):
        self.path = path
        self.test()

    def test(self):
        if os.path.exists(self.path):
            return True
        del self


