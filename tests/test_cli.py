import os

from click.testing import CliRunner
from nose.tools import assert_equal

from mock import patch
from plotly_helper.cli import cli

PATH = os.path.dirname(__file__)


# patching plotly.offline.plot to avoid the call
@patch('plotly_helper.neuron_viewer.plot_')
def test_cli(_):
    runner = CliRunner()
    result = runner.invoke(cli, ['view', os.path.join(PATH, 'data', 'neuron.h5')])
    assert_equal(result.exit_code, 0)
