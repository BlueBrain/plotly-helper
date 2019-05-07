'''
Define the public 'plot' function to be used to draw
morphology using plotly
'''
import os
from collections import defaultdict
from itertools import chain, repeat

import numpy as np
import plotly.graph_objs as go
from plotly.offline import init_notebook_mode, iplot, plot as plot_

from neurom import COLS, iter_neurites, iter_sections, iter_segments
from neurom.view.view import TREE_COLOR

from plotly_helper.helper import PlotlyHelperPlane
from plotly_helper.shapes import circle

NEURON_NAME = 'neuron'
SOMA_NAME = 'soma'


def _neurite_name(neurite, prefix, names):
    '''The neurite name used for the legend'''
    name = str(neurite.type).replace('NeuriteType.', '').replace('_', ' ')
    return '{} {} {}'.format(prefix, name, names[neurite.type])


# pylint: disable=too-many-locals
def _make_trace2d(neuron, plane, prefix='', opacity=1., visible=True, style=None, line_width=2):
    '''Create the trace to be plotted'''
    names = defaultdict(int)
    lines = list()
    for neurite in iter_neurites(neuron):
        names[neurite.type] += 1

        try:
            neurite_color = style[neurite]['color']
        except KeyError:
            neurite_color = TREE_COLOR.get(neurite.root_node.type, 'black')

        name = _neurite_name(neurite, prefix, names)

        for section in iter_sections(neurite):
            segs = [(s[0][COLS.XYZ], s[1][COLS.XYZ]) for s in iter_segments(section)]

            try:
                colors = style[section]['color']
            except KeyError:
                colors = neurite_color

            coords = dict()
            for i, coord in enumerate('xyz'):
                coords[coord] = list(chain.from_iterable((p1[i], p2[i], None) for p1, p2 in segs))

            coords = dict(x=coords[plane[0]], y=coords[plane[1]])
            lines.append(go.Scattergl(name=name, visible=visible, opacity=opacity,
                                      showlegend=False,
                                      line=dict(color=colors, width=line_width),
                                      mode='lines',
                                      **coords))
    return lines


# pylint: disable=too-many-locals
def _make_trace(neuron, plane, prefix='', opacity=1., visible=True, style=None, line_width=2):
    '''Create the trace to be plotted'''
    names = defaultdict(int)
    lines = list()
    for neurite in iter_neurites(neuron):
        names[neurite.type] += 1

        coords = dict(x=list(), y=list(), z=list())
        colors = list()

        try:
            default_color = style[neurite]['color']
        except KeyError:
            default_color = TREE_COLOR.get(neurite.root_node.type, 'black')

        for section in iter_sections(neurite):
            segs = [(s[0][COLS.XYZ], s[1][COLS.XYZ]) for s in iter_segments(section)]

            section_style = style.get(
                section, {'range': slice(0, len(segs)), 'color': default_color})
            range_ = section_style['range']
            colors += list(repeat(default_color, 3 * range_.start))
            colors += list(repeat(section_style['color'], 3 * (range_.stop - range_.start)))
            colors += list(repeat(default_color, 3 * (len(segs) - range_.stop)))

            for i, coord in enumerate('xyz'):
                coords[coord] += list(chain.from_iterable((p1[i], p2[i], None) for p1, p2 in segs)
                                      if coord in plane else
                                      chain.from_iterable((0, 0, None) for _ in segs))

        lines.append(go.Scatter3d(name=_neurite_name(neurite, prefix, names),
                                  showlegend=False,
                                  visible=visible, opacity=opacity,
                                  line=dict(color=colors, width=line_width),
                                  mode='lines',
                                  **coords))
    return lines


def _make_soma(neuron):
    ''' Create a 3d surface representing the soma '''
    theta = np.linspace(0, 2 * np.pi, 100)
    phi = np.linspace(0, np.pi, 100)
    soma_r = neuron.soma.radius
    soma_z = np.outer(np.ones(100), np.cos(phi)) * soma_r + neuron.soma.center[2]
    return go.Surface(
        name=SOMA_NAME,
        x=(np.outer(np.cos(theta), np.sin(phi)) * soma_r + neuron.soma.center[0]),
        y=(np.outer(np.sin(theta), np.sin(phi)) * soma_r + neuron.soma.center[1]),
        z=soma_z,
        cauto=False, surfacecolor=['black'] * len(soma_z), showscale=False,
    )


def _make_soma2d(neuron, plane):
    idx = {'x': 0, 'y': 1, 'z': 2}
    return circle(neuron.soma.center[idx[plane[0]]],
                  neuron.soma.center[idx[plane[1]]],
                  neuron.soma.radius,
                  color='rgba(50, 171, 96, 1)')


class NeuronBuilder:
    '''A helper class to plot neuron and colorize specific sections'''
    def __init__(self, neuron, plane, title='neuron', inline=False, line_width=2):
        self.neuron = neuron
        self.inline = inline
        self.line_width = line_width

        self.properties = defaultdict(dict)
        self.helper = PlotlyHelperPlane(title, plane)

    def color_section(self, section, color='green', recursive=False, start_point=0, end_point=None):
        '''Colors points of the section between start_point and end_point

        Args:
            section (neurom.core._neuron.Section): a NeuroM section
            color (str): A color supported by plotly
            recursive (bool): whether or not to color descendant sections as well
            start_point (int): point to start coloring from
            end_point (int): point to stop coloring at (None colors until the last section point)
        '''
        self.properties[section]['color'] = color
        end_point = end_point if end_point is not None else len(section.points) - 1
        self.properties[section]['range'] = slice(start_point, end_point)
        if recursive:
            for child in section.children:
                self.color_section(child, color, recursive=True)

    def get_figure(self):
        '''Build the figure and returns it'''
        is_3d = (self.helper.plane == 'xyz')
        if is_3d:
            self.helper.add_data({NEURON_NAME: _make_trace(
                self.neuron, self.helper.plane, style=self.properties, line_width=self.line_width)})
            self.helper.add_data({SOMA_NAME: _make_soma(self.neuron)})
            # self.helper.add_plane_buttons()
        else:
            self.helper.add_data({NEURON_NAME: _make_trace2d(
                self.neuron, self.helper.plane, style=self.properties, line_width=self.line_width)})
            self.helper.add_shapes([_make_soma2d(self.neuron, self.helper.plane)])
        return self.helper.get_fig()

    # pylint: disable=keyword-arg-before-vararg
    def plot(self, filename=None, *args, **kwargs):
        '''Plot

        Args:
            filename (str): the output html filename

        All other args are passed to plotly plot
        '''
        fig = self.get_figure()
        plot_fun = iplot if self.inline else plot_
        self.helper.layout['height'] = 1000

        if self.inline:
            init_notebook_mode(connected=True)  # pragma: no cover
        filename = filename or os.path.join('/tmp', self.helper.title + '.html')
        plot_fun(fig, filename=filename, *args, **kwargs)

        return fig


def plot(neuron, plane, title='neuron', inline=False, **kwargs):
    '''Draw the morphology within the given plane

    plane (str): a string representing the 2D plane (example: 'xy')
                 or '3d', '3D' for a 3D view

    inline (bool): must be set to True for interactive ipython notebook plotting
    '''
    return NeuronBuilder(neuron, plane, title, inline, **kwargs).plot()
