'''The morph-tool command line launcher'''
import click
from neurom import load_neuron

from plotly_helper.neuron_viewer import plot


@click.group()
def cli():
    '''The CLI entry point'''


@cli.command()
@click.argument('input_file')
@click.option('--plane', type=click.Choice(['3d', 'xy', 'yx', 'yz', 'zy', 'xz', 'zx']),
              default='3d')
def view(input_file, plane):
    '''A simple neuron viewer'''
    plot(load_neuron(input_file), plane=plane)
