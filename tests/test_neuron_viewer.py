import os
import sys
from mock import patch

from neurom import load_neuron
from plotly_helper.neuron_viewer import NeuronBuilder

from nose.tools import assert_dict_equal, assert_equal
PATH = os.path.dirname(__file__)

# patching plotly.offline.plot to avoid the call
@patch('plotly_helper.neuron_viewer.plot_')
def test_color_section(_):
    neuron = load_neuron(os.path.join(PATH, '..', 'tests', 'data', 'neuron.h5'))

    # Colorize first section of the neurite
    builder = NeuronBuilder(neuron, '3d')
    builder.color_section(neuron.neurites[1].root_node)
    assert_equal(len(builder.properties.values()), 1)
    assert_dict_equal(next(iter(builder.properties.values())),
                      {'color': 'green', 'range': slice(0, 23, None)})
    builder.plot()

    # Colorize alls sections of the neurite
    builder = NeuronBuilder(neuron, '3d')
    section = neuron.neurites[2].root_node
    builder.color_section(section, color='gray', recursive=True)
    assert_equal(len(builder.properties.values()), 27)
    builder.plot()

    # Colorize only a fraction of the section
    builder = NeuronBuilder(neuron, '3d')
    builder.color_section(neuron.sections[159], color='black', start_point=20, end_point=120)
    assert_dict_equal(next(iter(builder.properties.values())),
                      {'color': 'black', 'range': slice(20, 120, None)})
    builder.plot()


    # 2d
    builder = NeuronBuilder(neuron, 'xy')
    builder.color_section(neuron.neurites[1].root_node)
    assert_equal(len(builder.properties.values()), 1)
    assert_dict_equal(next(iter(builder.properties.values())),
                      {'color': 'green', 'range': slice(0, 23, None)})
    builder.plot()
