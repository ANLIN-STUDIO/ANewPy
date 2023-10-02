# import typing
import shutil
from win32api import GetMonitorInfo, MonitorFromPoint
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QPushButton, QApplication, QWidget, QLabel
from PyQt5.QtGui import QPixmap


# Left = 0
# Right = 1
# Top = 2
# Bottom = 3


def connect(signal: any,
            function: any
            ):
    """
    :param signal: pyqtSignal
    :param function: function
    :return: None
    """
    signal.connect(function)


def BConnect(PushButton: QPushButton,
             function: any
             ):
    connect(PushButton.clicked, function)


def CTimer(self: QWidget,
           msec: int,
           function: any):
    from PyQt5.QtCore import QTimer
    timer = QTimer(self)
    timer.start(msec)
    connect(timer.timeout, function)
    return timer


def KTimer(self):
    self.timer.killTimer(self.timer.timerId())


def screensize():
    desktop = QApplication.desktop()
    return desktop.width(), desktop.height()


INACTION = 0
FILL = 1
FIT = 2

END = 0
RESTART = 1


def showImage(self: QWidget,
              image_path: str,
              label_size: [list[int] | tuple[int]],
              label_pos: [list[int] | tuple[int]],
              scaledContents: bool = True,
              ifAlignCenter: bool = True):
    __image_label = QLabel(self)
    __image_label.resize(label_size[0], label_size[1])
    __image_label.move(label_pos[0], label_pos[1])
    if ifAlignCenter:
        __image_label.setAlignment(Qt.AlignCenter)
    __image_label.setScaledContents(scaledContents)
    __image_label.setPixmap(QPixmap(image_path))


class playVideo(QWidget):
    import ANewPy

    @ANewPy.paras_checker(fps=[ANewPy.Rule.value_range, '(i, 0)'])
    def __init__(self,
                 self_,
                 video_path: str | ANewPy.Path,
                 label_pos: list | tuple,
                 label_size: list | tuple,
                 resize_mode: int = None,
                 fps: int = 60,
                 play_sounds: bool = True,
                 over_mode: int = None,
                 over_do: any = None,
                 ):
        """
        INACTION = 0;
        FILL = 1;
        FIT = 2;

        END = 0;
        RESTART = 1;
        """
        import cv2
        import os
        from moviepy.editor import AudioFileClip
        super().__init__()
        self.print_real_fps_flag = -1
        self.print_real_fps_s_time = None
        self.real_fps = -1
        self.ran_time = 0
        self.ms_time = 1000 // fps
        self.timer = None
        self.video_path = video_path
        self.label_pos = label_pos
        self.label_size = label_size
        self.resize_mode = resize_mode
        self.playsound = None
        self.if_pause = False
        self.over_mode = over_mode
        self.over_do = over_do

        self.__video_label = QLabel(self_)
        self.__video_label.resize(self.label_size[0], self.label_size[1])
        self.__video_label.move(self.label_pos[0], self.label_pos[1])

        if not os.path.exists('bin\\'):
            os.makedirs('bin\\')

        self.play_sounds = play_sounds
        if play_sounds:
            self.audio_path = f"bin\\{os.path.split(os.path.splitext(self.video_path)[0])[-1]}.wav"
            self.audio_copy_path = f"bin\\{os.path.split(os.path.splitext(self.video_path)[0])[-1]}~.wav"
            if os.path.exists(self.audio_copy_path):
                shutil.copy(self.audio_copy_path, self.audio_path)
            else:
                shutil.rmtree('bin\\')
                os.makedirs('bin\\')
                audio_clip = AudioFileClip(self.video_path)
                audio_clip.write_audiofile(self.audio_path)
                shutil.copy(self.audio_path, self.audio_copy_path)

        self.video_cap = cv2.VideoCapture(self.video_path)
        self.total_time = self.video_cap.get(7) / self.video_cap.get(5) * 1000
        self.frame = f'bin\\{os.path.split(os.path.splitext(self.video_path)[0])[-1]}.jpg'
        self.__from_mp4_get_img()
        if self.resize_mode == FIT or self.resize_mode is None:
            self.__FITResize()

    def check_running(self):
        return self.ran_time != -1 and not self.if_pause

    def __FITResize(self):
        from PIL import Image
        img = Image.open(self.frame)
        if img.size[0] - self.label_size[0] > img.size[1] - self.label_size[1]:
            k = self.label_size[0] / img.size[0]
        else:
            k = self.label_size[1] / img.size[1]
        self.label_size = int(img.size[0] * k), int(img.size[1] * k)
        self.__video_label.resize(self.label_size[0], self.label_size[1])

    def __from_mp4_get_img(self):
        import cv2
        self.video_cap.set(cv2.CAP_PROP_POS_MSEC, self.ran_time)
        image = self.video_cap.read()[1]
        try:
            cv2.imencode('.jpg', image)[1].tofile(self.frame)
        except cv2.error:
            return False

    def Relabel(self, label_pos, label_size):
        self.label_pos = label_pos
        self.__video_label.move(self.label_pos[0], self.label_pos[1])
        self.label_size = label_size
        if self.resize_mode == FIT or self.resize_mode is None:
            self.__FITResize()
        else:
            self.__video_label.resize(self.label_size[0], self.label_size[1])

    def run(self):
        import datetime
        import threading
        import time
        import winsound

        def ran_time_count():
            while self.ran_time < self.total_time and self.ran_time != -1:
                s_time = datetime.datetime.now()
                time.sleep(0.01)
                e_time = datetime.datetime.now()
                if not self.if_pause:
                    self.ran_time += (e_time - s_time).microseconds / 1000
            if self.ran_time != -1:
                KTimer(self)
                self.over()

        self.ran_time = 0
        threading.Thread(target=ran_time_count).start()
        if self.play_sounds:
            winsound.PlaySound(self.audio_path, winsound.SND_ASYNC)
        self.timer = CTimer(self, self.ms_time, self.__ms_run)

    def over(self):
        print('over')
        if self.over_do is not None:
            self.over_do()
        if self.over_mode == RESTART:
            self.restart()
        else:
            self.__video_label.close()
            self.__video_label.deleteLater()

    def pause(self):
        import winsound
        from pydub import AudioSegment
        self.if_pause = True
        winsound.PlaySound(self.playsound, winsound.SND_PURGE)
        shutil.copy(self.audio_copy_path, self.audio_path)
        wav = AudioSegment.from_wav(self.audio_path)
        wav[self.ran_time:].export(self.audio_path, format="wav")

    def recovery(self):
        import winsound
        self.if_pause = False
        winsound.PlaySound(self.audio_path, winsound.SND_ASYNC)

    def stop(self):
        self.over_mode = None
        self.if_pause = True

    def restart(self):
        KTimer(self)
        self.ran_time = -1
        shutil.copy(self.audio_copy_path, self.audio_path)
        self.run()

    def __ms_run(self):
        import datetime
        from PyQt5.QtCore import Qt
        if not self.if_pause and self.ran_time < self.total_time:
            if self.print_real_fps_flag >= 0:
                self.print_real_fps_flag += 1
                if datetime.datetime.now() - self.print_real_fps_s_time >= datetime.timedelta(seconds=1):
                    self.real_fps = int(self.print_real_fps_flag)
                    self.print_real_fps_flag = -1
                    self.print_real_fps_s_time = None
            self.__from_mp4_get_img()
            if self.resize_mode == INACTION:
                self.__video_label.setScaledContents(False)
                self.__video_label.setAlignment(Qt.AlignCenter)
            else:
                self.__video_label.setScaledContents(True)
            self.__video_label.setPixmap(QPixmap(self.frame))

    def flip_real_fps(self):
        import datetime
        self.print_real_fps_flag = 0
        self.print_real_fps_s_time = datetime.datetime.now()

    def print_real_fps(self):
        if self.real_fps == -1:
            print('You should use \"flip_real_fps()\" before using \"print_real_fps()\"')
            return None
        print(f"FPS: {self.real_fps}f/s")

    def get_real_fps(self):
        if self.real_fps == -1:
            print('You should use \"get_real_fps()\" before using \"print_real_fps()\"')
            return None
        return self.real_fps

# class intoScreen:
#
#     @typing.overload
#     def __init__(self: QWidget,
#                  size,
#                  origin_pos,
#                  direction,
#                  acceleration: 'float > 0',
#                  flip_millisecond: 'float > 0',
#                  positive_point: '1 >= float > 0' = 0.5
#                  ):
#         if direction == Right:
#             start_pos = (screensize()[0], origin_pos[1])
#         elif direction == Top:
#             start_pos = (origin_pos[0], -size[1])
#         elif direction == Bottom:
#             start_pos = (origin_pos[0], screensize()[1])
#         else:
#             start_pos = (-size[0], origin_pos[1])
#         intoScreen(self, start_pos, origin_pos, acceleration, flip_millisecond, positive_point)
#
#     @typing.overload
#     def __init__(self: QWidget,
#                  start_pos: list | tuple,
#                  end_pos: list | tuple,
#                  acceleration: 'float > 0',
#                  flip_millisecond: 'float > 0',
#                  positive_point: '1 >= float > 0' = 0.5
#                  ):
#         positive_line = []
#         negative_line = []
#         for difference in (start_pos[0] - end_pos[0], start_pos[1] - end_pos[1]):
#             positive_line.append(difference * positive_point)
#             negative_line.append(difference * (1 - positive_point))
#
#         def second_do():
#             for each_line in positive_line:
#                 pass
#             self.delta_v += acceleration * flip_millisecond / 1000
#
#         self.delta_v = 0
#         self.delta_v_flag = False
#         self.enter_or_out_flag = False
#         self.x, self.y = start_pos
#         self.move(self.x, self.y)
#         Ctimer(self, flip_millisecond, second_do)
#
#     def __init__(*args):
#         pass
