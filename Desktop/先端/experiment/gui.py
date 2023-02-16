import sys
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import QSound
from PyQt5.QtCore import *
from pedalboard import *
from pedalboard.io import AudioFile
import sounddevice as sd
import librosa
from threading import *
import threading
import soundfile as sf


class PyAudioPylerGUI(QWidget):
    value = pyqtSignal(int)
    value2 = pyqtSignal(int)
    number = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.dial = QDial()
        self.dial2 = QDial()
        self.worker = EffectThread()
        self.thread = QThread()
        self.init_ui()
        self.show()

    def init_ui(self):

        self.setGeometry(100, 100, 250, 250)
        grid = QGridLayout()
        self.setWindowTitle('Audio Player')

        button_dialog = QPushButton("環境音1")
        button_dialog2 = QPushButton("環境音2")
        button_dialog3 = QPushButton("環境音3")
        button_music = QPushButton("Play")
        button_music2 = QPushButton("Play")
        button_music3 = QPushButton("Play")
        button_test = QPushButton("Stop")

        grid.addWidget(button_dialog, 0, 0)
        grid.addWidget(button_dialog2, 1, 0)
        grid.addWidget(button_dialog3, 2, 0)
        grid.addWidget(button_music, 0, 3)
        grid.addWidget(button_music2, 1, 3)
        grid.addWidget(button_music3, 2, 3)
        grid.addWidget(button_test, 3, 0, 1, 2)

        grid.addWidget(self.dial,   4, 0, 1, 2)
        grid.addWidget(self.dial2,   4, 2, 1, 2)

        button_dialog.clicked.connect(self.button_play)
        button_dialog2.clicked.connect(self.button_play2)
        button_dialog3.clicked.connect(self.button_play3)
        button_music.clicked.connect(self.music)
        button_music2.clicked.connect(self.music2)
        button_music3.clicked.connect(self.music3)

        button_test.clicked.connect(self.button_stop)

        self.dial.setMinimum(0)
        self.dial.setMaximum(400)
        self.dial.setValue(0)

        self.dial.valueChanged.connect(self.progress)

        self.dial2.setMinimum(0)
        self.dial2.setMaximum(400)
        self.dial2.setValue(0)

        self.dial2.valueChanged.connect(self.progress2)

        self.setLayout(grid)

    def button_play(self):
        self.audio, self.sr = librosa.load(
            'sound/washing_machine1.wav', sr=44100)
        sd.play(self.audio, loop=True)

    def button_play2(self):
        self.audio, self.sr = librosa.load(
            'sound/site_of_construction1.wav', sr=44100)
        sd.play(self.audio, loop=True)

    def button_play3(self):
        self.audio, self.sr = librosa.load('sound/car_streets1.wav', sr=44100)
        sd.play(self.audio, loop=True)

    def music(self):
        self.worker = EffectThread()
        self.number.connect(self.worker.set_num)
        self.number.emit(0)
        self.button_play()
        self.start()

    def music2(self):
        self.worker = EffectThread()
        self.number.connect(self.worker.set_num)
        self.number.emit(1)
        self.button_play2()
        self.start()

    def music3(self):
        self.worker = EffectThread()
        self.number.connect(self.worker.set_num)
        self.number.emit(2)
        self.button_play3()
        self.start()

    def button_stop(self):
        self.worker.stop_stream()
        sd.stop()

    def start(self):

        self.value.connect(self.worker.para)
        self.value2.connect(self.worker.para2)

        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.play)
        self.worker.progress.connect(self.progress)
        self.worker.progress2.connect(self.progress2)

        self.thread.start()
        self.thread.quit()

    def progress(self, dum):
        dum = self.dial.value()
        self.value.emit(self.dial.value())

    def progress2(self, dum2):
        dum2 = self.dial2.value()
        self.value2.emit(self.dial2.value())


num = 0


class EffectThread(QObject):
    progress = pyqtSignal(int)
    progress2 = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.threaddeactive = False
        self.test = 0
        self.test2 = 0

    def para(self, value):
        self.test = value

    def para2(self, value2):
        self.test2 = value2

    def set_num(self, nums):
        global num
        num = nums

    @pyqtSlot()
    def play(self):

        event = threading.Event()

        file_list = [
            'sound/wash_melody.wav',
            'sound/site_melody.wav',
            'sound/car_melody.wav'
        ]

        data, fs = sf.read(file_list[num], always_2d=True)

        current_frame = 0

        with AudioFile(file_list[num], 'r') as f:
            data1 = f.read(f.frames)

        def callback(outdata, frames, time, status):
            nonlocal current_frame
            if status:
                print(status)
            if self.threaddeactive:
                self.threaddeactive = False
                return sd.CallbackStop

            board = Pedalboard([
                Phaser(centre_frequency_hz=self.test*10),
                Chorus(rate_hz=self.test2/10)
            ])

            chunksize = 4048
            if len(data) - current_frame < 4048:
                outdata[chunksize:] = 0
                current_frame = 0  # 追加
                stream.start()  # 追加
                return  # 追加
            outdata[:chunksize] = board(
                data[current_frame:current_frame + chunksize], sample_rate=44100)
            current_frame += chunksize
        stream = sd.OutputStream(
            samplerate=fs, blocksize=4048, channels=data.shape[1],
            callback=callback, finished_callback=event.set)
        with stream:
            event.wait()

    def stop_stream(self):
        self.threaddeactive = True
        print(self.threaddeactive)


def ui_main():
    app = QApplication(sys.argv)
    w = PyAudioPylerGUI()
    app.exit(app.exec_())


if __name__ == '__main__':
    ui_main()
