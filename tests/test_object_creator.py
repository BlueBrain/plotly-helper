import nose.tools as nt
import numpy as np
import numpy.testing as npt

from plotly_helper.helper import PlotlyObjectProperties
import plotly_helper.object_creator as object_creator


def test_create_scatter_line():
    points = np.array([[0, 0, 0], [1, 1, 1], [2, 2, 2]])
    prop = PlotlyObjectProperties(name='plot1', visible=False)
    obj = object_creator.create_scatter_line(points, prop).to_plotly_json()
    good_obj = {'line': {'color': 'red', 'width': 5},
                'marker': {'color': 'red', 'size': 3},
                'name': 'plot1',
                'opacity': 1.0,
                'showlegend': True,
                'visible': False,
                'x': np.array([0, 1, 2]),
                'y': np.array([0, 1, 2]),
                'z': np.array([0, 1, 2]),
                'type': 'scatter3d'}

    # can't dict equal with numpy array. Remove and test them and then test the dict.
    npt.assert_array_equal(good_obj.pop('x'), obj.pop('x'))
    npt.assert_array_equal(good_obj.pop('y'), obj.pop('y'))
    npt.assert_array_equal(good_obj.pop('z'), obj.pop('z'))
    nt.assert_dict_equal(obj, good_obj)


def test_create_scatter_line_2():
    points = np.array([[0, 0, 0], [1, 1, 1], [2, 2, 2]])
    obj = object_creator.create_scatter_line(points).to_plotly_json()
    good_obj = {'line': {'color': 'red', 'width': 5},
                'marker': {'color': 'red', 'size': 3},
                'opacity': 1.0,
                'showlegend': True,
                'visible': True,
                'x': np.array([0, 1, 2]),
                'y': np.array([0, 1, 2]),
                'z': np.array([0, 1, 2]),
                'type': 'scatter3d'}

    # can't dict equal with numpy array. Remove and test them and then test the dict.
    npt.assert_array_equal(good_obj.pop('x'), obj.pop('x'))
    npt.assert_array_equal(good_obj.pop('y'), obj.pop('y'))
    npt.assert_array_equal(good_obj.pop('z'), obj.pop('z'))
    nt.assert_dict_equal(obj, good_obj)

def test_create_scatter():
    points = np.array([[0, 0, 0], [1, 1, 1], [2, 2, 2]])
    obj = object_creator.create_scatter(points).to_plotly_json()
    good_obj = {'mode': 'markers',
                'line': {'color': 'red', 'width': 5},
                'marker': {'color': 'red', 'size': 3},
                'opacity': 1.0,
                'showlegend': True,
                'visible': True,
                'x': np.array([0, 1, 2]),
                'y': np.array([0, 1, 2]),
                'z': np.array([0, 1, 2]),
                'type': 'scatter3d'}

    # can't dict equal with numpy array. Remove and test them and then test the dict.
    npt.assert_array_equal(good_obj.pop('x'), obj.pop('x'))
    npt.assert_array_equal(good_obj.pop('y'), obj.pop('y'))
    npt.assert_array_equal(good_obj.pop('z'), obj.pop('z'))
    nt.assert_dict_equal(obj, good_obj)


def test_create_point():
    point = np.array([1, 1, 1])
    obj = object_creator.create_point(point).to_plotly_json()
    good_obj = {'mode': 'markers',
                'line': {'color': 'red', 'width': 5},
                'marker': {'color': 'red', 'size': 3},
                'opacity': 1.0,
                'showlegend': True,
                'visible': True,
                'x': np.array([1]),
                'y': np.array([1]),
                'z': np.array([1]),
                'type': 'scatter3d'}

    # can't dict equal with numpy array. Remove and test them and then test the dict.
    npt.assert_array_equal(good_obj.pop('x'), obj.pop('x'))
    npt.assert_array_equal(good_obj.pop('y'), obj.pop('y'))
    npt.assert_array_equal(good_obj.pop('z'), obj.pop('z'))
    nt.assert_dict_equal(obj, good_obj)


def test_create_vector():
    point1 = np.array([1, 1, 1])
    point2 = np.array([2, 2, 2])

    obj = object_creator.create_vector(point1, point2).to_plotly_json()
    good_obj = {'line': {'color': 'red', 'width': 5},
                'marker': {'color': 'red', 'size': 3},
                'opacity': 1.0,
                'showlegend': True,
                'visible': True,
                'x': np.array([1, 2]),
                'y': np.array([1, 2]),
                'z': np.array([1, 2]),
                'type': 'scatter3d'}

    # can't dict equal with numpy array. Remove and test them and then test the dict.
    npt.assert_array_equal(good_obj.pop('x'), obj.pop('x'))
    npt.assert_array_equal(good_obj.pop('y'), obj.pop('y'))
    npt.assert_array_equal(good_obj.pop('z'), obj.pop('z'))
    nt.assert_dict_equal(obj, good_obj)
