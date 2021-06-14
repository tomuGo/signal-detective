from signal_detective import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import QtCore, QtWidgets
import asyncio
import asyncqt
import os
import openpyxl
import json
from filter_json import FilterJson
import matplotlib
from scipy import signal

import matplotlib.cm as cm
from matplotlib.colors import LogNorm
matplotlib.use("Qt5Agg")  # 声明使用QT5
from matplotlib.figure import Figure
from sig import Plot
import numpy as np

_sheet_ecg_name = 'ECG_DATA'

ss = "[{\"bandpass\":{\"filter_min_frequency\":11,\"filter_max_frequency\":30}},{\"notch\":{\"filter_frequency\":2}}]"


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self._init_ui()
        self._ecg_data = []

    def _init_ui(self):
        self.importButton.clicked.connect(self._import_excel)
        self.runButton.clicked.connect(self._show_filter)
        self.filterCommandText.setText(ss)
        self.figure = Plot(dpi=100)
        self.plotLayout.addWidget(self.figure)

    def _import_excel(self):
        file_path, file_type = QtWidgets.QFileDialog.getOpenFileName(self, "选取文件", os.getcwd())
        self._load_signal(file_path)

    def _load_signal(self, file_path):
        print("file_path:{0}".format(file_path))
        if file_path.endswith('.xlsx'):
            workbook = openpyxl.load_workbook(file_path)
            ecg_sheet = workbook[_sheet_ecg_name]
            ecg_row_data = []
            for cell in ecg_sheet['B']:
                if cell.row > 1:
                    ecg_row_data.append(json.loads(cell.value))
            self._ecg_data = [i for j in ecg_row_data for i in j]
        else:
            print("error file type")

    def _show_filter(self):
        text = self.filterCommandText.toPlainText()
        print(self.frequency.text())
        temp_data = self._ecg_data[self.startPosition.value():self.endPosition.value()]
        json_filter = FilterJson(temp_data, text, self.frequency.value())
        filter_data = json_filter.run()
        self.figure.origin.cla()
        self.figure.origin.plot(temp_data)
        self.figure.origin.plot(filter_data)
        f, t, Zxx = signal.stft(filter_data, self.frequency.value(), nperseg=50)
        temperature = [[9, 2, 3, 9], [2, 3, 4, 5], [3, 4, 5, 6], [9, 7, 8, 9]]
        aa = np.random.randint(0, 10, size=(60, 1250))

        self.figure.timeFrequency.imshow(aa, cmap=cm.hot, norm=LogNorm())
        #self.figure.timeFrequency.plot(t, f, np.abs(Zxx))
        self.figure.draw()
        self.figure.flush_events()

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    loop = asyncqt.QEventLoop(app)
    asyncio.set_event_loop(loop)
    win.loop = loop
    with loop:
        sys.exit(loop.run_forever())
