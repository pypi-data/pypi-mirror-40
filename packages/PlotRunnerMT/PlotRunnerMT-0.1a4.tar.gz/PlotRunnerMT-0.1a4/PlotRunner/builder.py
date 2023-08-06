from matplotlib import pyplot as plt
from matplotlib.lines import Line2D
import math
def simpleFigure(**kwargs):
    return plt.figure()

def simpleAxes(axes_size,axes_names,**kwargs):
    axes_pool = []
    if type(axes_size) == int:
        axes_count = axes_size
        x = int(axes_size**0.5)
        axes_size = (math.floor(axes_size//x),x)
    else:
        axes_count = axes_size[0]*axes_size[1]
    for axes_index in range(1,axes_count+1):
        axes_ = plt.subplot(axes_size[0], axes_size[1], axes_index, **kwargs)
        if type(axes_names) == list:
            axes_.name = axes_names[axes_index-1]
        elif axes_names is not None:
            axes_.name = axes_names
        axes_pool.append(axes_)
    return axes_pool

def simpleLine(**kwargs):
    return Line2D([],[],**kwargs)









