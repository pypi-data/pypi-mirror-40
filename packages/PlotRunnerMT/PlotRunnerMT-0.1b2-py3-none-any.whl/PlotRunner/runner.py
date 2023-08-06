from threading import Thread
import matplotlib
from matplotlib import pyplot as plt
import PlotRunner.builder as PlotBuilder
from IPython import display
from collections import Iterable
from queue import Queue


class GraphRunner(Thread):
    def __init__(self, interactive=False, group=None, name=None, daemon=None, legend=False, timeout=0.01,
                 plotPause=0.02, windowActive=True, **kwargs):
        """
        GraphRunner 是一个支持多种交互方式的Graph。
        :param interactive: 是否采用交互式绘图
        :param group: 线程group，见threading.Thread
        :param name: 线程name，见threading.Thread
        :param daemon: 线程daemon，见threading.Thread
        :param legend: 是否绘制legend
        :param timeout: 小于0则使用阻塞模式，大于0则是设置阻塞超时时间，来避免长时间阻塞
        :param plotPause: 图刷新时间间隔
        :param windowActive: 是否展示图
        :param kwargs: figure和axes的参数，详见matplotlib的plt.figure和plt.axes所支持的参数
        """
        Thread.__init__(self, group=group, name=name, daemon=daemon)
        figure = kwargs.pop("figure", None)
        axes_size = kwargs.pop("axes_size", 1)
        axes_names = kwargs.pop("axes_names", None)
        axes = kwargs.pop("axes", None)
        suptitle = kwargs.pop("suptitle", "Test 1")

        def cycle():
            cyc = matplotlib.rcParams['axes.prop_cycle']
            while True:
                for v in cyc:
                    yield v

        self.color_cycle = cycle()

        def newQueue():
            return Queue(maxsize=kwargs.pop("jobMaxSize", 30))

        self.newQueue = newQueue

        if not figure:
            self.figure = PlotBuilder.simpleFigure(**kwargs)
            self.figure.suptitle(suptitle)
        if axes:
            self.axes = axes
            if isinstance(axes, Iterable):
                axes = list(axes)
            else:
                axes = [axes, ]
            self.axes = axes
        else:
            self.axes = PlotBuilder.simpleAxes(axes_size, axes_names, **kwargs)
        self.axesIndex = list(self.axes)
        self.axesIndex.sort(key=lambda x: x.name)

        self.figure.add_axes(*self.axesIndex)
        self.axesNames = {axes.name: axes for axes in self.axesIndex}
        self.curAxesIndex = -1
        self.__initFlag = False
        self.legend = legend
        self.interactive = interactive
        self.timeout = timeout
        self.plotPause = plotPause
        self.windowActive = windowActive

        if self.interactive:
            self.jobQueue = self.newQueue()  # 这里需要一个堵塞式的

    def __addLine(self, axes, line=None, **kwargs):
        for ax in axes:
            if 'color' not in kwargs:
                kwargs.update(next(self.color_cycle))
            if not line:
                line = PlotBuilder.simpleLine(**kwargs)
                ax.add_line(line)
            if self.legend:
                ax.legend()

    def addLine(self, line=None, axes=None, axesIndex=0, axesName=None, **kwargs):
        """
        新增线段
        :param line: Line2D对象
        【定位axes】
        :param axes: axes对象
        :param axesIndex:
        :param axesName:
        :param kwargs:
        :return:
        """
        axes = self.getAxes(axes, axesIndex, axesName)
        self.addDrawJob(lambda: self.__addLine(axes, line, **kwargs))

    def __draw(self, xdata, ydata, line=None, lineIndex=0, lineLabel=None, axes=None, axesName=None, axesIndex=None,
               **lineParam):
        if axes is None and axesName is None and axesIndex is None:
            if not hasattr(self, "lineIter"):
                def iter():
                    lineAxesList = [(line, ax) for ax in self.axesIndex for line in ax.lines]
                    index = -1
                    while True:
                        index += 1
                        if index >= len(lineAxesList):
                            index = 0
                        yield lineAxesList[index]

                self.lineIter = iter()
            if lineLabel is not None:
                line, axes = next(self.lineIter)
                while line.get_label() != lineLabel:
                    line, axes = next(self.lineIter)
            else:
                line, axes = next(self.lineIter)

            # draw
        elif axes:
            lineList = axes.lines
            if not line:
                if lineLabel is not None:
                    lineList = list(filter(lambda x: x.get_label() == lineLabel, lineList))
                line = lineList[lineIndex]
        elif axesName is not None:
            axes = self.axesNames[axesName]
            lineList = axes.lines
            if not line:
                if lineLabel is not None:
                    lineList = list(filter(lambda x: x.get_label() == lineLabel, lineList))
                line = lineList[lineIndex]
        elif axesIndex is not None:
            axes = self.axesIndex[axesIndex]
            if not line:
                lineList = axes.lines
                if lineLabel is not None:
                    lineList = list(filter(lambda x: x.get_label() == lineLabel, lineList))
                line = lineList[lineIndex]
        else:
            raise Exception("wrong params:can't match axes")

        xline = line.get_xdata()
        yline = line.get_ydata()
        if xdata is not None:
            if isinstance(xdata,Iterable):
                xline.extend(xdata)
            else:
                xline.append(xdata)
        if ydata is not None:
            if isinstance(ydata,Iterable):
                yline.extend(ydata)
            else:
                yline.append(ydata)
        line.set_xdata(xline)
        line.set_ydata(yline)

        xmin = xdata
        xmax = xdata
        if isinstance(xdata,Iterable) and len(xdata) > 0:
            xmin = min(xdata)
            xmax = max(xdata)

        ymin = ydata
        ymax = ydata
        if isinstance(ydata,Iterable) and len(ydata) > 0:
            ymin = min(ydata)
            ymax = max(ydata)

        if axes:
            self.__updateLim(axes, xmin, xmax, ymin, ymax)
            self.__setLineParam(axes, line, **lineParam)
        self.figure.stale = True

    def draw(self, xdata=None, ydata=None, line=None, lineIndex=0, lineLabel=None, axes=None, axesName=None, axesIndex=None,
             **lineParam):
        """
        绘图函数，所有的绘图最终基于这个函数进行绘图，对于确定的line和确定的axes进行绘图。
        :param xdata: x轴数据
        :param ydata: y轴数据
        【用于定位line】
        :param line: line对象，不建议使用这个参数
        :param lineIndex: axes中line的顺序号
        :param lineLabel: axes中line的label
        【用于定位axes】
        :param axes: axes对象，不建议使用这个参数
        :param axesName: axes名
        :param axesIndex: axes的Index【默认按照前到后的顺序，如果有指定axes.name，则按照axes.name进行排序】
        【line参数】
        :param lineParam: 线段参数，详见matplotlib的Line2D支持的参数
        :return:
        """
        self.addDrawJob(
            lambda: self.__draw(xdata, ydata, line, lineIndex, lineLabel, axes, axesName, axesIndex, **lineParam))

    def __init_lines(self):
        # 如果没有被初始化过，那么对每条线段分配初始颜色
        # 如果
        pass

    def init_lines(self):
        self.addDrawJob(self.__init_lines)

    def updateLegend(self, axes=None, axesIndex=0, axesName=None):
        """
        更新Legend
        【定位axes】
        :param axes:
        :param axesIndex:
        :param axesName:
        :return:
        """
        self.addDrawJob(lambda: self.__updateLegend(axes, axesIndex, axesName))

    def __updateLegend(self, axes=None, axesIndex=0, axesName=None):
        axes = self.getAxes(axes, axesIndex, axesName)
        for ax in axes:
            ax.legend()

    def updateLegendAll(self):
        """
        更新所有axes的legend
        :return:
        """
        self.updateLegend(self.axesIndex)

    def __removeLegend(self, axes=None, axesIndex=0, axesName=None):
        axes = self.getAxes(axes, axesIndex, axesName)
        for ax in axes:
            legends = ax.get_legend()
            if legends:
                legends.remove()

    def removeLegend(self, axes=None, axesIndex=0, axesName=None):
        """
        删除Legend
        【定位axes】
        :param axes:
        :param axesIndex:
        :param axesName:
        :return:
        """
        self.addDrawJob(lambda: self.__removeLegend(axes, axesIndex, axesName))

    def removeLegendAll(self):
        """
        删除所有Legend
        :return:
        """
        self.removeLegend(self.axes)

    def __updateLim(self, axes, xmin, xmax, ymin, ymax):
        xlim = axes.get_xlim()
        ylim = axes.get_ylim()
        if xmin is not None and xmax is not None:
            if xlim[0] > xmin or xlim[1] < xmax:
                if xlim[0] < xmin:
                    xmin = xlim[0]
                if xlim[1] > xmax:
                    xmax = xlim[1]
                axes.set_xlim(xmin, xmax)
        if ymin is not None and ymax is not None:
            if ylim[0] > ymin or ylim[1] < ymax:
                if ylim[0] < ymin:
                    ymin = ylim[0]
                if ylim[1] > ymax:
                    ymax = ylim[1]
                axes.set_ylim(ymin, ymax)

    def updateLim(self, axes, xmin, xmax, ymin, ymax):
        """
        更新axes的xlim和ylim
        :param axes:
        :param xmin:
        :param xmax:
        :param ymin:
        :param ymax:
        :return:
        """
        self.addDrawJob(lambda: self.__updateLim(axes, xmin, xmax, ymin, ymax))

    def getAxes(self, axes=None, axesIndex=0, axesName=None):
        """
        定位Axes
        :param axes: Axes对象或者Axes列表
        :param axesIndex:
        :param axesName:
        :return:
        """
        if axes:
            if isinstance(axes, Iterable):
                return list(axes)
            else:
                return [axes, ]
        elif axesName is not None:
            if isinstance(axesName, Iterable):
                return [self.axesNames[axName] for axName in axesName]
            else:
                return [self.axesNames[axesName], ]
        else:
            if isinstance(axesIndex, Iterable):
                return [self.axesIndex[axIndex] for axIndex in axesIndex]
            else:
                return [self.axesIndex[axesIndex], ]

    def __updateOneAxes(self, xdata, ydatas, axes=None, axesIndex=0, axesName=None, **kwargs):
        axes = self.getAxes(axes, axesIndex, axesName)
        assert axes, "error:can't find axes!"
        assert not isinstance(axes, Iterable) or (
                isinstance(axes, Iterable) and len(axes) <= 1), "wrong:many axes found,choose the first update!"
        axes = axes[0]
        for ydata,line in zip(ydatas,axes.get_lines()):
            self.__draw(xdata, ydata, axes=axes,line = line,**kwargs)

    def updateOneAxes(self, xdata, ydatas, axes=None, axesIndex=0, axesName=None, **kwargs):
        """
        更新一个Axes的所有线段，更新ydatas和axes的line数量的最小数量
        :param xdata: 1维数组
        :param ydatas: 2维数组
        【定位axes】
        :param axes:
        :param axesIndex:
        :param axesName:
        【线段参数】
        :param kwargs:
        :return:
        """
        self.addDrawJob(lambda: self.__updateOneAxes(xdata, ydatas, axes, axesIndex, axesName, **kwargs))

    def __updateOneLineLabel(self, xdata, ydata, axes=None, axesIndex=-1, axesName=None, lineLabel=None, **kwargs):
        axes = self.getAxes(axes, axesIndex, axesName)
        if lineLabel:
            if type(xdata) == list and type(xdata[0]) == list:
                for xda, ax in zip(xdata, axes):
                    self.draw(xdata, ydata, axes=ax, lineLabel=lineLabel, **kwargs)
            else:
                for ax in axes:
                    self.draw(xdata, ydata, axes=ax, lineLabel=lineLabel, **kwargs)

    def updateOneLineLabel(self, xdata, ydata, axes=None, axesIndex=-1, axesName=None, lineLabel=None, **kwargs):
        """
        更新指定lineLabel的数据
        【数据】
        :param xdata:
        :param ydata:
        【定位Axes】
        :param axes:
        :param axesIndex:
        :param axesName:

        :param lineLabel:lineLabel
        :param kwargs: 线段参数
        :return:
        """
        self.addDrawJob(lambda: self.__updateOneLineLabel(xdata, ydata, axes, axesIndex, axesName, lineLabel, **kwargs))

    def __setLineParam(self, axes, line, **kwargs):
        if kwargs:
            line.set(**kwargs)
            self.updateLegend(axes)

    def setLineParam(self, axes, line, **kwargs):
        """
        设置线段参数，不推荐直接使用，建议使用draw，不传入xdata和ydata
        :param axes:
        :param line:
        :param kwargs:
        :return:
        """
        self.addDrawJob(lambda: self.__setLineParam(axes, line, **kwargs))

    def addDrawJob(self, func):
        if self.interactive:
            self.jobQueue.put(func)
        else:
            func()

    def __cleanJob(self):
        assert not self.__runFlag, "Error:can't clean job when runner is running!"
        del self.jobQueue
        self.jobQueue = self.newQueue()

    def stopDraw(self):
        """
        停止绘图
        :return:
        """
        def stop_draw():
            self.__runFlag = False

        self.addDrawJob(stop_draw)

    def __cleanAxes(self, axes=None, axesIndex=0, axesName=None):
        axes = self.getAxes(axes, axesIndex, axesName)
        for ax in axes:
            ax.cla()

    def cleanAxes(self, axes=None, axesIndex=0, axesName=None):
        """
        清空指定axes内容
        【定位axes】
        :param axes:
        :param axesIndex:
        :param axesName:
        :return:
        """
        self.addDrawJob(lambda: self.__cleanAxes(axes, axesIndex, axesName))

    def __deleteLine(self, axes, line=None, lineIndex=0, lineLabel=None):
        if not line:
            lineList = list(axes.lines)
            if lineLabel is not None:
                lineList = list(filter(lambda x: x.get_label() == lineLabel, lineList))
                for line in lineList:
                    self.__removeLineFromAxes(axes, line)
            elif lineIndex >= 0 and lineIndex < len(axes.lines):
                axes.lines.pop(lineIndex)
        else:
            self.__removeLineFromAxes(axes, line)
        if self.legend:
            axes.legend()

    def deleteLine(self, line=None, lineIndex=0, lineLabel=None, axes=None, axesName=None, axesIndex=0):
        """
        删除line
        【定位line】
        :param line:
        :param lineIndex:
        :param lineLabel:
        【定位axes】
        :param axes:
        :param axesName:
        :param axesIndex:
        :return:
        """
        axes = self.getAxes(axes, axesIndex, axesName)
        for ax in axes:
            self.addDrawJob(lambda: self.__deleteLine(ax, line, lineIndex, lineLabel))
        self.updateLegend()

    def __removeLineFromAxes(self, axes, line):
        try:
            axes.lines.remove(line)
        except Exception:
            pass

    def show(self):
        """
        window活跃
        :return:
        """
        def f():
            self.windowActive = True

        self.addDrawJob(f)

    def unshow(self):
        """
        window不活跃
        :return:
        """
        def f():
            self.windowActive = False

        self.addDrawJob(f)

    def restart(self):
        """
        重启runer
        :return:
        """
        for ax in self.figure.axes:
            for line in ax.lines:
                line.set_xdata([])
                line.set_ydata([])
        self.__cleanJob()
        if self.interactive:
            self.start()
        else:
            self.run()

    def run(self):
        """
        如果要使用 qt/tk 模式应调用start。如果是 inline 模式调动run
        :return:
        """
        if not self.__initFlag:
            self.init_lines()
        self.__runFlag = True
        plt.ion()

        while self.__runFlag:
            try:
                if self.timeout >= 0:
                    job = self.jobQueue.get(timeout=self.timeout)
                else:
                    job = self.jobQueue.get()
            except Exception:
                pass
            else:
                job()
            is_ipython = 'inline' in matplotlib.get_backend()
            if is_ipython:
                display.clear_output(wait=True)
                display.display(plt.gcf())
            else:
                if self.windowActive:
                    plt.pause(self.plotPause)
        self.__runFlag = False
        plt.close("all")
        plt.ioff()
