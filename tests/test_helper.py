import os
import tempfile
from contextlib import contextmanager
import shutil
import numpy as np
import nose.tools as nt
import plotly.graph_objs as go

from plotly_helper.helper import PlotlyHelper, PlotlyHelperPlane
from plotly_helper.helper import plot_fig, iplot_fig

@contextmanager
def setup_tempdir(prefix):
    temp_dir = tempfile.mkdtemp(prefix=prefix)
    try:
        yield temp_dir
    finally:
        shutil.rmtree(temp_dir)

def get_scatter():
    points = np.array([[0, 0, 0], [1, 1, 1], [2, 2, 2]])
    return go.Scatter3d(x=points[:, 0], y=points[:, 1], z=points[:, 2])


def test_empty_init():
    title = 'name'
    helper = PlotlyHelper(title)
    ok_dict = {'data': [],
               'layout': {'autosize': True,
                          'legend': {'bgcolor': '#FFFFFF',
                                     'bordercolor': '#FFFFFF',
                                     'borderwidth': 2,
                                     'font': {'color': '#000',
                                              'family': 'sans-serif',
                                              'size': 12},
                                     'traceorder': 'normal',
                                     'x': 0.8,
                                     'y': 1},
                          'shapes': [],
                          'title': 'name',
                          'updatemenus': []}}
    nt.assert_dict_equal(helper.get_fig(), ok_dict)
    nt.assert_equal(helper.title, title)
    nt.assert_equal(helper.nb_objects, 0)


def test__group_validator1():
    data = get_scatter()
    data2 = get_scatter()
    obj = {'name': [data, data2], 'name2': [data], 'name3': data}
    PlotlyHelper._group_validator(obj)


@nt.raises(TypeError)
def test__group_validator2():
    obj = 'dummy'
    PlotlyHelper._group_validator(obj)


@nt.raises(ValueError)
def test__group_validator3():
    obj = {'name': []}
    PlotlyHelper._group_validator(obj)


@nt.raises(TypeError)
def test__group_validator4():
    obj = {'name': [1]}
    PlotlyHelper._group_validator(obj)


@nt.raises(TypeError)
def test__group_validator5():
    data = get_scatter()
    obj = {1: [data]}
    PlotlyHelper._group_validator(obj)


@nt.raises(TypeError)
def test__group_validator6():
    obj = {'name': 1}
    PlotlyHelper._group_validator(obj)


def test__add_visibility1():
    helper = PlotlyHelper('name')
    helper._add_visibility('name1', [get_scatter()])
    nt.assert_equal(helper.visibility_map['name1'], range(0, 1))
    helper._add_visibility('name2', [get_scatter(), get_scatter(), get_scatter()])
    nt.assert_equal(helper.visibility_map['name2'], range(0, 3))


@nt.raises(ValueError)
def test__add_visibility2():
    helper = PlotlyHelper('name')
    helper._add_visibility('name', [get_scatter()])
    helper._add_visibility('name', [get_scatter()])


def test_add_data():
    helper = PlotlyHelper('name')
    data = get_scatter()
    helper.add_data({'name1': data})
    nt.assert_equal(helper.nb_objects, 1)
    helper.add_data({'name2': [data, data]})
    nt.assert_equal(helper.nb_objects, 3)
    nt.assert_equal(helper.visibility_map['name1'], range(0, 1))
    nt.assert_equal(helper.visibility_map['name2'], range(1, 3))


def test_get_visibility_list():
    helper = PlotlyHelper('name')
    data = get_scatter()
    helper.add_data({'name1': data})
    helper.add_data({'name2': [data, data]})
    nt.assert_list_equal(helper.get_visibility_list('name1'), [True, False, False])
    nt.assert_list_equal(helper.get_visibility_list('name2'), [False, True, True])


@nt.raises(KeyError)
def test_get_visibility_list_2():
    helper = PlotlyHelper('name')
    data = get_scatter()
    helper.add_data({'name1': data})
    helper.get_visibility_list('name2')


def test_remove_data():
    helper = PlotlyHelper('name')
    data = get_scatter()
    helper.add_data({'name1': data})
    helper.add_data({'name2': [data, data]})
    nt.assert_equal(helper.visibility_map['name2'], range(1, 3))
    nt.assert_list_equal(helper.get_visibility_list('name2'), [False, True, True])
    helper.remove_data('name1')
    nt.assert_equal(helper.nb_objects, 2)
    nt.assert_equal(helper.visibility_map['name2'], range(0, 2))
    nt.assert_list_equal(helper.get_visibility_list('name2'), [True, True])
    nt.assert_equal(len(helper.data), 2)
    helper.add_data({'name1': data})
    nt.assert_equal(len(helper.data), 3)
    nt.assert_equal(helper.visibility_map['name1'], range(2, 3))


@nt.raises(ValueError)
def test_remove_data_2():
    helper = PlotlyHelper('name')
    helper.remove_data('name1')


def test_add_shape():
    shape = {'type': 'rect', 'x0': .02, 'x1': 1.02, 'y0': 0, 'y1': 6}
    helper = PlotlyHelper('name')
    helper.add_shapes([shape, shape])
    nt.assert_equal(len(helper.shapes), 2)
    nt.assert_list_equal(helper.shapes, [{'type': 'rect', 'x0': .02, 'x1': 1.02, 'y0': 0, 'y1': 6},
                                         {'type': 'rect', 'x0': .02, 'x1': 1.02, 'y0': 0, 'y1': 6}])


def test_add_button():
    helper = PlotlyHelper('name')
    data = get_scatter()
    helper.add_data({'name1': data})
    helper.add_data({'name2': [data, data]})
    helper.add_button('button', 'update', [{'visible': helper.get_visibility_list('name1')}])
    ok_update = [{'type': 'dropdown', 'direction': 'down', 'xanchor': 'left',
                  'active': 0, 'buttons': [
            {'label': 'button', 'method': 'update', 'args': [{'visible': [True, False, False]}]}]}]
    nt.assert_list_equal(ok_update, helper.updatemenus)
    helper.add_button('button2', 'update', [{'visible': helper.get_visibility_list('name2')}])
    ok_update = [{'type': 'dropdown', 'direction': 'down', 'xanchor': 'left',
                  'active': 0, 'buttons': [
            {'label': 'button', 'method': 'update', 'args': [{'visible': [True, False, False]}]},
            {'label': 'button2', 'method': 'update', 'args': [{'visible': [False, True, True]}]}]}]
    nt.assert_list_equal(ok_update, helper.updatemenus)
    helper._place_buttons()
    ok_update = [{'type': 'dropdown', 'direction': 'down', 'xanchor': 'left',
                  'active': 0, 'buttons': [
            {'label': 'button', 'method': 'update', 'args': [{'visible': [True, False, False]}]},
            {'label': 'button2', 'method': 'update', 'args': [{'visible': [False, True, True]}]}],
                  'y': 1}]
    nt.assert_list_equal(ok_update, helper.updatemenus)


def test_default_plotly_helper_plane_init():
    helper = PlotlyHelperPlane('test', 'xy')
    nt.assert_equal(helper.plane, 'xy')
    nt.assert_equal(helper.title, 'test-xy')


def test_get_scene():
    scene = PlotlyHelperPlane._get_scene('xy')
    nt.assert_equal(scene['aspectmode'], 'data')
    nt.assert_equal(scene['dragmode'], 'zoom')
    camera_dict = {'up': {'x': 0, 'y': 1, 'z': 0}, 'center': {'x': 0, 'y': 0, 'z': 0},
                   'eye': {'x': 0, 'y': 0, 'z': 2.0}}
    nt.assert_dict_equal(scene['camera'], camera_dict)

    scene = PlotlyHelperPlane._get_scene('yx')
    nt.assert_equal(scene['aspectmode'], 'data')
    nt.assert_equal(scene['dragmode'], 'zoom')
    camera_dict = {'up': {'x': 1, 'y': 0, 'z': 0}, 'center': {'x': 0, 'y': 0, 'z': 0},
                   'eye': {'x': 0, 'y': 0, 'z': -2.0}}
    nt.assert_dict_equal(scene['camera'], camera_dict)

    scene = PlotlyHelperPlane._get_scene('xyz')
    nt.assert_equal(scene['aspectmode'], 'data')
    nt.assert_equal(scene['dragmode'], 'turntable')
    camera_dict = {'up': {'x': 0, 'y': 0, 'z': 1}, 'center': {'x': 0, 'y': 0, 'z': 0},
                   'eye': {'x': -1.7428, 'y': 1.0707, 'z': 0.71}}
    nt.assert_dict_equal(scene['camera'], camera_dict)


def test_sanitize_plane():
    nt.assert_equal(PlotlyHelperPlane._sanitize_plane('xy'), 'xy')
    nt.assert_equal(PlotlyHelperPlane._sanitize_plane('3d'), 'xyz')


@nt.raises(TypeError)
def test_sanitize_plane_2():
    PlotlyHelperPlane._sanitize_plane(1)


@nt.raises(ValueError)
def test_sanitize_plane_3():
    PlotlyHelperPlane._sanitize_plane('xyz')


@nt.raises(ValueError)
def test_sanitize_plane_4():
    PlotlyHelperPlane._sanitize_plane('x2')


def test_add_plane_buttons():
    helper = PlotlyHelperPlane('test', 'xy')
    helper.add_plane_buttons()
    updatemenus = helper.get_fig()['layout']['updatemenus']
    nt.assert_list_equal(updatemenus, [])


def test_add_plane_buttons_2():
    helper = PlotlyHelperPlane('test', '3d')
    helper.add_plane_buttons()
    fig = helper.get_fig()
    nt.assert_equal(fig['layout']['updatemenus'][0]['type'], 'dropdown')
    nt.assert_equal(fig['layout']['updatemenus'][0]['direction'], 'right')
    names = ('3D view', 'XY view', 'XZ view', 'YZ view')
    cameras = [{'up': {'x': 0, 'y': 0, 'z': 1}, 'center': {'x': 0, 'y': 0, 'z': 0},
                'eye': {'x': -1.7428, 'y': 1.0707, 'z': 0.71}},
               {'up': {'x': 0, 'y': 1, 'z': 0}, 'center': {'x': 0, 'y': 0, 'z': 0},
                'eye': {'x': 0, 'y': 0, 'z': 2.0}},
               {'up': {'x': 0, 'y': 0, 'z': 1}, 'center': {'x': 0, 'y': 0, 'z': 0},
                'eye': {'x': 0, 'y': -2.0, 'z': 0}},
               {'up': {'x': 0, 'y': 0, 'z': 1}, 'center': {'x': 0, 'y': 0, 'z': 0},
                'eye': {'x': 2.0, 'y': 0, 'z': 0}}]
    for i, button in enumerate(fig['layout']['updatemenus'][0]['buttons']):
        nt.assert_equal(button['label'], names[i])
        nt.assert_equal(button['method'], 'relayout')
        args = button['args']
        for key, item in args[1].items():
            if 'axis' in key:
                nt.assert_dict_equal(item, {'gridcolor': 'rgb(255, 255, 255)',
                                            'zerolinecolor': 'rgb(255, 255, 255)',
                                            'showbackground': True,
                                            'backgroundcolor': 'rgb(238, 238,238)',
                                            'visible': True})
            elif key == 'camera':
                nt.assert_dict_equal(item, cameras[i])


def test_plot():
    with setup_tempdir('plots') as plot_dir:
        output_file = os.path.join(plot_dir, 'test')
        helper = PlotlyHelper('name')
        data = get_scatter()
        helper.add_data({'name1': data})
        plot_fig(helper.get_fig(), output_file, auto_open=False)
        nt.ok_(os.path.exists(output_file + '.html'))
        output_file_2 = os.path.join(plot_dir, 'test2.html')
        plot_fig(helper.get_fig(), output_file_2, auto_open=False)
        nt.ok_(os.path.exists(output_file + '.html'))
