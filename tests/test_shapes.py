import os
import sys
from mock import patch

from neurom import load_neuron
from plotly_helper.shapes import line, circle

from nose.tools import assert_dict_equal, assert_equal
PATH = os.path.dirname(__file__)

def test_shapes():
    assert_dict_equal(line(0, 0, 1, 1, color=2, width=4),
                      {'line': {'color': 2, 'width': 4},
                       'type': 'line',
                       'x0': 0,
                       'x1': 1,
                       'y0': 0,
                       'y1': 1})

    assert_dict_equal(circle(0, 0, 10, color=2, width=4),
                      {'fillcolor': 'rgba(50, 171, 96, 0.7)',
                       'line': {'color': 2, 'width': 4},
                       'type': 'circle',
                       'x0': -10,
                       'x1': 10,
                       'xref': 'x',
                       'y0': -10,
                       'y1': 10,
                       'yref': 'y'}
)
