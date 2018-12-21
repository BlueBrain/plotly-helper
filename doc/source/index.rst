.. include:: _common.rst

Welcome to |name| documentation!
==========================================

Introduction
============

|name| is a Python library to facilitate the display of 3d objects and graphs using
the python package Plotly (https://plot.ly/python/).


Plotly is an open source visualization package for R, Python and JavaScript. It is
relatively user-friendly, complete and gives access to simple "out of the box"
3D visualisations with basic interactions. This makes plotly a good alternative
to matplotlib for a lot of usecases. This library has been successfully used for displaying
3D neurons from neuroM or sub set of orientation fields in BBP.


Content
=========

The main interface classes exposed in |name| are ``PlotlyHelper`` and his
sub-class ``PlotlyHelperPlane``.

``PlotlyHelper`` contains few methods which facilitate the use of plotly:

  - a single class to regroup all your displayable objects
  - adding/removing data to/from your plot
  - adding shapes
  - adding buttons
  - create your final figure dictionary

``PlotlyHelperPlane`` contains the same methods but adds some specifics for 2/3d
representations using a (x, y, z) axis:

  - correct setup of the camera for 2/3D representation
  - adding buttons to switch from 3D to 2D projections

Two free functions are available to display your graphs in ``plotly_helper.helper``:

  - ``plot`` to create an `html` file.
  - ``iplot`` that you can use in a jupyter notebook

Free functions to create scatter plots in a concise way are also available in the
``object_creator`` module:

  - ``create_scatter_line`` to create 3D lines
  - ``create_scatter`` to create 3D scatter plots
  - ``create_vector`` to create 3D vectors
  - ``create_point`` to create 3D points


Examples
=========

3D plots
~~~~~~~~~

We will create a simple example with two populations of randomly placed points in 3D.

.. code-block:: python

    >>> import numpy as np
    >>> from plotly_helper.helper import PlotlyHelperPlane, plot_fig
    >>> from plotly_helper.object_creator import create_scatter
    >>> helper = PlotlyHelperPlane('my_plot', '3d')
    >>> population1 = np.random.random((50, 3))
    >>> population2 = np.random.random((50, 3))
    >>> prop1 = PlotlyObjectProperties(name='pop1', color='red')
    >>> graph_pop1 = create_scatter(population1, prop1)
    >>> prop2 = PlotlyObjectProperties(name='pop2', color='blue')
    >>> graph_pop2 = create_scatter(population2, name='pop2', color='blue')
    >>> helper.add_data({'pop1': graph_pop1, 'pop2': graph_pop2})
    >>> helper.add_button('all', 'update',
                         [{'visible': helper.get_visibility_list(['pop1', 'pop2'])}],
                         'viz')
    >>> helper.add_button('pop1 only', 'update',
                          [{'visible': helper.get_visibility_list('pop1')}], 'viz')
    >>> helper.add_button('pop2 only', 'update',
                          [{'visible': helper.get_visibility_list('pop2')}], 'viz')

    >>> plot_fig(helper.get_fig(), 'ouput.html', auto_open=True)


Your web browser will pop off and the figure will be displayed. You can now do the
following actions :

  - mouse left click + drag to rotate the scene
  - mouse left click + drag to translate the scene
  - mouse wheel click + drag or wheel roll to zoom in/out
  - click on the left button to choose to display only one population or both
  - click on the legend to remove a population, click again to show it again
  - double click on the legend to only display this population

2D plots
~~~~~~~~~

We will create a simple example with two traces of points in 2D.

.. code-block:: python

    >>> import numpy as np
    >>> from plotly_helper.helper import PlotlyHelper, plot_fig
    >>> from plotly_helper.object_creator import create_scatter
    >>> import plotly.graph_objs as go

    >>> N = 500
    >>> random1_x = np.linspace(0, 1, N)
    >>> random1_y = np.random.randn(N)
    >>> random2_x = np.linspace(0, 1, N)
    >>> random2_y = np.random.randn(N)

    >>> helper = PlotlyHelper('my_plot')
    >>> trace1 = go.Scatter(x = random1_x, y = random1_y, name='random1')
    >>> trace2 = go.Scatter(x = random2_x, y = random2_y, name='random2')
    >>> helper.add_data({'trace1': trace1, 'trace2': trace2})
    >>> helper.add_button('all', 'update', [{'visible': helper.get_visibility_list(['trace1', 'trace2'])}], 'viz')
    >>> helper.add_button('trace1', 'update', [{'visible': helper.get_visibility_list('trace1')}], 'viz')
    >>> helper.add_button('trace2', 'update', [{'visible': helper.get_visibility_list('trace2')}], 'viz')
    >>> plot_fig(helper.get_fig(), 'ouput.html', auto_open=True)

