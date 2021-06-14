from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QSizePolicy


class Plot(FigureCanvas):

    def __init__(self, parent=None, dpi=100):
        plt.rcParams['font.family'] = ['SimHei']  # 更换字体使中文显示正常
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

        # 创建绘图对象，就像matlab里创建一个新的窗口那样

        self.fig = Figure( dpi=dpi)

        # 紧接着在这个新的窗口加上一个子图，也就是实际画图的地方
        # 看到subplot我想你也明白，可以在这里添加多个子图，并且规定子图的位置，
        # 方法和matlab的subplot一摸一样，为了演示我加了一个新的axes1

        self.origin = self.fig.add_subplot(3, 1, 1)
        # self.origin.set_title('origin')
        # self.filter = self.fig.add_subplot(3, 1, 2)
        #self.filter.set_title('filter')
        self.timeFrequency = self.fig.add_subplot(3, 1, 3)
        self.timeFrequency.set_title('time_frequency')

        #self.timeFrequency.setyLabel('Frequency [Hz]')

        # 下面这个是画新图后不保留上次的图形，但这个代码似乎有问题报错了，先注释掉
        # self.axes.hold(False)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        '''定义FigureCanvas的尺寸策略，这部分的意思是设置FigureCanvas，使之尽可能的向外填充空间。'''
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
