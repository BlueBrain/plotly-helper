import numpy as np
import nose.tools as nt
import plotly.graph_objs as go

from plotly_helper.helper import PlotlyHelper


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
