import os
from neurom import load_morphology
from plotly_helper.neuron_viewer import NeuronBuilder

PATH = os.path.dirname(__file__)

def plot():
    neuron = load_morphology(os.path.join(PATH, '..', 'tests', 'data', 'neuron.h5'))
    builder = NeuronBuilder(neuron, '3d', line_width=4)

    # Colorize first section of the neurite
    builder.color_section(neuron.neurites[1].root_node)

    # Colorize alls sections of the neurite
    builder.color_section(neuron.neurites[2].root_node, color='gray', recursive=True)

    # Colorize only a fraction of the section
    builder.color_section(neuron.sections[159], color='black', start_point=20, end_point=120)

    builder.plot()

if __name__=='__main__':
    plot()
