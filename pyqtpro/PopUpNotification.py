import sys
import ANewPy.pyqtpro.pyqtpro
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget, QLabel


class PopUpNotification(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool | Qt.WindowDoesNotAcceptFocus)
        self.size = [300, 200]
        self.resize(self.size[0], self.size[1])

        y = 10

        self.L_1 = QLabel(self)
        self.L_1.move(10, y)
        font_size = 13
        self.L_1.setFont(QFont("微软雅黑", font_size, QFont.Bold))
        self.L_1.setText('This is a POP-UP NOTIFICATION')
        y += font_size + 10

        self.L_2 = QLabel(self)
        self.L_2.move(10, y)
        font_size = 10
        self.L_2.setFont(QFont("微软雅黑", font_size))
        self.L_2.setText('ANewPy was made by ANLIN.STUDIO :-)')
        y += font_size + 10

        y += 10
        self.L_3 = QLabel(self)
        self.L_3.move(10, y)
        font_size = 10
        self.L_3.setFont(QFont("微软雅黑", font_size))
        self.L_3.setText('| This is a example for you.')
        y += font_size + 10

        y -= 6
        self.L_4 = QLabel(self)
        self.L_4.move(10, y)
        font_size = 10
        self.L_4.setFont(QFont("微软雅黑", font_size))
        self.L_4.setText('| To show you how to use \"pyqtpro\".')
        y += font_size + 10

        y -= 6
        self.L_5 = QLabel(self)
        self.L_5.move(10, y)
        font_size = 10
        self.L_5.setFont(QFont("微软雅黑", font_size))
        self.L_5.setText('| It\'s like Lego, You just need to put them in')
        y += font_size + 10

        y -= 6
        self.L_6 = QLabel(self)
        self.L_6.move(10, y)
        font_size = 10
        self.L_6.setFont(QFont("微软雅黑", font_size))
        self.L_6.setText('|   the code.')
        y += font_size + 10

        self.L_quit = QLabel(self)
        font_size = 10
        self.L_quit.move(10, self.size[1] - 20 - font_size)
        self.L_quit.setFont(QFont("微软雅黑", font_size, QFont.Bold))
        self.L_quit.setText('(Click me to quit)')

        ANewPy.pyqtpro.windowEffect.AcrylicEffectPreposition(self, [255, 255, 255, 150])
        ANewPy.pyqtpro.pyqtpro.CTimer(self, 10, self.timer_do)
        self.x = -self.size[0] - 10
        self.delta_v = 0
        self.delta_v_flag = False
        self.enter_or_out_flag = False

    def timer_do(self):
        if self.x < 10 and not self.enter_or_out_flag:
            self.x += self.delta_v
            if self.delta_v_flag:
                if self.delta_v > 1:
                    self.delta_v -= 0.3
            else:
                self.delta_v += 0.3
            if self.x + self.size[0]/2 + 5 >= 0:
                self.delta_v_flag = True
            self.move(int(self.x), ANewPy.screensize()[1] - self.size[1] - 60)
        if self.enter_or_out_flag:
            if self.x > -self.size[0] - 10:
                self.x -= self.delta_v
                if self.delta_v_flag:
                    if self.delta_v > 1:
                        self.delta_v -= 0.3
                else:
                    self.delta_v += 0.3
                if 10-self.x >= (self.size[0]+10)/2:
                    self.delta_v_flag = True
                self.move(int(self.x), ANewPy.screensize()[1] - self.size[1] - 60)
            else:
                self.quit()

    def quit(self):
        self.close()
        quit()

    def re_delta_v(self):
        self.delta_v = 0
        self.delta_v_flag = False

    def out(self):
        self.re_delta_v()
        self.enter_or_out_flag = True

    def mousePressEvent(self, _):
        self.out()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    PopUpNotificationWindow = PopUpNotification()
    PopUpNotificationWindow.show()
    sys.exit(app.exec_())
