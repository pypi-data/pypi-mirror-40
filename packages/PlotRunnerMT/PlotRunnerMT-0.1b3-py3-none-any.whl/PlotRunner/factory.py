from PlotRunner.runner import *
import threading as ti
import numpy as np

def oneAxesSimpleRunner(legend=True, **kwargs):
    runner = GraphRunner(name="__simpleRunner__{}".format(0), legend=legend, **kwargs)

    def update(xdata=None, ydata=None, **kwargs):
        runner.draw(xdata, ydata, axesIndex=0, **kwargs)

    runner.updateLine = update
    return runner


if __name__ == '__main__':
    # mlb.use('GTK')
    runner = oneAxesSimpleRunner(suptitle="TEST", xlabel="lunshu", ylabel="score", interactive=True)


    def run():
        runner.addLine(label="A", color="r")
        runner.addLine(label="B")
        runner.updateLine(0, .2, lineLabel="A")
        runner.updateLine(2, 0.3, lineIndex=1)
        runner.updateLine([], [], lineIndex=0, color="y")
        runner.updateLine(4, 11, lineIndex=0)
        runner.updateLine(lineIndex=0)
        runner.updateOneLineLabel([1, 2], [3, 4], lineLabel="A")
        runner.updateOneAxes([1, 2], np.array([[-5, -6], [-7, -6]]))
        # runner.stopDraw()


    T = ti.Thread(target=run)
    T.start()
    runner.run()

    # plt.show(clear = True)
