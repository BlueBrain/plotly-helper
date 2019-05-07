import nose.tools as nt
import numpy as np
import numpy.testing as npt

import plotly_helper.object_creator as object_creator


def test_create_scatter_line():
    points = np.array([[0, 0, 0], [1, 1, 1], [2, 2, 2]])
    obj = object_creator.scatter_line(points, name='plot1', visible=False).to_plotly_json()
    good_obj = {'line': {'width': 5},
                'marker': {'size': 3},
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


def test_scatter_line_2():
    points = np.array([[0, 0, 0], [1, 1, 1], [2, 2, 2]])
    obj = object_creator.scatter_line(points).to_plotly_json()
    good_obj = {'line': {'width': 5},
                'marker': {'size': 3},
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

def test_scatter():
    points = np.array([[0, 0, 0], [1, 1, 1], [2, 2, 2]])
    obj = object_creator.scatter(points).to_plotly_json()
    good_obj = {'mode': 'markers',
                'line': {'width': 5},
                'marker': {'line': {'width': 5}, 'size': 5},
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


def test_point():
    point = np.array([1, 1, 1])
    obj = object_creator.point(point).to_plotly_json()
    good_obj = {'mode': 'markers',
                'line': {'width': 5},
                'marker': {'line': {'width': 5}, 'size': 5},
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


def test_vector():
    point1 = np.array([1, 1, 1])
    point2 = np.array([2, 2, 2])

    obj = object_creator.vector(point1, point2).to_plotly_json()
    good_obj = {'line': {'width': 5},
                'marker': {'size': 3},
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
