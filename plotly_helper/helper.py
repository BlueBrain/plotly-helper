""" Helper function for plotly. Facilitate the 3d repr of objects with plotly.

You can find information on python plotly here : https://plot.ly/python/
"""
import os

import six
import numpy as np

from plotly.offline import plot, iplot
# unknown pylint problem with this import
# pylint: disable-msg=E0611,E0001
from plotly.basedatatypes import BaseTraceType


class PlotlyHelper(object):
    """Class to help creating plotly plots with shapes, buttons and data """

    def __init__(self, title, layout=None):
        self.title = title
        self.layout = layout if layout else self._get_standard_layout(title)
        self.data = list()
        self.visibility_map = dict()
        self.updatemenus = list()
        self.shapes = list()
        self.nb_objects = 0
        self.button_group_to_index = dict()
        self.button_group_index = -1

    @staticmethod
    def _get_standard_layout(title):
        """ Return a very simple layout with a title and legend's setup """
        return dict(autosize=True, title=title,
                    legend=PlotlyHelper._get_legend())

    @staticmethod
    def _get_legend():
        """ Returns the legend dict already setup for the plot """
        return dict(x=0.8, y=1, traceorder='normal',
                    font=dict(family='sans-serif', size=12, color='#000'),
                    bgcolor='#FFFFFF', bordercolor='#FFFFFF', borderwidth=2)

    @staticmethod
    def _get_button_skeleton(direction='down'):
        """ Returns the skeleton dict for buttons

        Args:
            direction: the direction for the button layout (default=down)
        """
        return dict(type='dropdown', direction=direction, xanchor='left', active=0, buttons=list())

    def _add_button_group(self, name, direction='down'):
        """ Add a button group to the plot

        Args:
            name: the button group name (str)
            direction: the direction for the button layout (default=down)
        """
        if name not in self.button_group_to_index:
            self.button_group_index += 1
            self.button_group_to_index[name] = self.button_group_index
            if self.button_group_index == 0:
                self.updatemenus = list([self._get_button_skeleton(direction)])
            else:
                self.updatemenus.append(self._get_button_skeleton(direction))

    def _add_visibility(self, name, objs):
        """ Update the position dictionary used to handle the visibility in plotly

        Args:
            name: the id used to name a group of plotly object (str)
            objs: a list containing the plotly objects included in the group 'name'

        Raises:
            ValueError: An error occurs if name shadows a previous entry name
        """
        if name in self.visibility_map:
            raise ValueError('{} already exists'.format(name))
        self.visibility_map[name] = range(len(self.data), len(self.data) + len(objs))

    def _place_buttons(self, offset=0.01):
        """ Place the buttons using the update menu from plotly """
        y_position = 1
        for group in self.updatemenus:
            group['y'] = y_position
            gap = 0.04 if group['direction'] == 'right' else len(group['buttons']) * 0.04
            y_position = y_position - (gap + offset)

    def get_visibility_list(self, names):
        """ Return the boolean list for the groups in names

        Args:
            names: a list of id corresponding to different groups of plotly objects
                list('str1, str2')

        Returns:
            the visibility list used in plotly with True for all groups in names and False
            elsewhere.

        Raises:
            KeyError: if a name is not found in the visibility map

        Notes:
             This function is a helper to facilitate the manipulation of plotly visibility. The
             visibility is natively poorly handled in plotly. To change the visibility of an
             object you need to keep track of the object's insertion number and to provide a boolean
             list.
             Ex: You inserted 4 objects in your figure and you want to display
             only the second one, you need to provide the list : [False, True, False, False].
             This function gives you easy access to this list using only the name of the inserted
             object.
             Ex:
             >>> helper = PlotlyHelper()
             >>> helper.add_data({"graph1" : [obj1], "graph2": [obj2]}).
             >>> helper.get_visibility_list(["graph1", "graph2"])
        """
        if isinstance(names, six.string_types):
            names = [names]
        try:
            true_indexes = set(item for name in names for item in self.visibility_map[name])
        except KeyError as error:
            raise KeyError('Can not find the object {}'.format(error))
        return [i in true_indexes for i in range(self.nb_objects)]

    @staticmethod
    def _group_validator(obj_groups):
        """ Type validator for a group of plotly objects

        Raises:
            TypeError: if obj_groups is not a dict
            TypeError: if an item in obj_groups is not a BaseTraceType
            TypeError: if a key in obj_groups is not a string_type
            ValueError: if an item is empty
        """
        if not isinstance(obj_groups, dict):
            raise TypeError('can t add {} to helper. Must be a dict'.format(obj_groups))

        def _obj_validator(current_obj):
            if not isinstance(current_obj, BaseTraceType):
                raise TypeError('can t add {} to helper'.format(current_obj))

        for name, obj_group in obj_groups.items():
            if not isinstance(name, six.string_types):
                raise TypeError('bad name {} for object'.format(name))

            if not isinstance(obj_group, (list, BaseTraceType)):
                raise TypeError('bad obj_group {} for name'.format(name))

            if isinstance(obj_group, list):
                if not obj_group:
                    raise ValueError('{} object is empty'.format(name))
                for obj in obj_group:
                    _obj_validator(obj)

    def add_data(self, obj_groups):
        """ Add plotly data to the plot and update its visibility map

        Args:
            obj_groups: a dict {name1: [list of plotly objs], name2: [list of plotly obj], ...}

        Note:
            This function is used to keep track of insertion numbers and to group different plotly
            objects altogether.
        """
        self._group_validator(obj_groups)
        for name, group in obj_groups.items():
            if not isinstance(group, list):
                group = [group]
            self._add_visibility(name, group)
            for obj in group:
                self.nb_objects += 1
                self.data.append(obj)

    def remove_data(self, names):
        """ Remove plotly data to the plot and update its visibility map

        Args:
            names: a list of name [name1, name2, ...] of object to remove

        Raises:
            ValueError: if one of the name has been referenced before

        Note:
            This function keeps recompute the number of object and visibility_map for all objects
        """

        def _remove_visibility(visibility_map, obj_name):
            if obj_name not in visibility_map:
                raise ValueError('{} must exists'.format(obj_name))
            to_removed_range = visibility_map.pop(obj_name)
            for c_name, obj_range in self.visibility_map.items():
                if obj_range[0] > to_removed_range[-1]:
                    c_range = list(visibility_map[c_name])
                    start = c_range[0] - len(to_removed_range)
                    stop = c_range[-1] - len(to_removed_range) + 1
                    visibility_map[c_name] = range(start, stop)
            return to_removed_range

        if isinstance(names, six.string_types):
            names = [names]

        for name in names:
            removed_range = list(_remove_visibility(self.visibility_map, name))
            self.nb_objects -= len(removed_range)
            del self.data[slice(removed_range[0], removed_range[-1] + 1)]

    def add_shapes(self, shapes):
        """ Add shape to the figure

        Args:
            shapes: a list of plotly shapes.

        Notes:
            A plotly shape is an object displayed on the plot background.
        """
        self.shapes.extend(shapes)

    def add_button(self, label, method, args, groupname='classic', direction='down'):
        """ Add button to the figure.

        Args:
            label: legend in the button (str)
            method: method used by plotly ('restyle', 'relayout', 'update', 'animate')
            args: arguments for the method see plotly documentation (str)
            groupname: name of the button group (str)
            direction: direction of the group of button ('down' or 'left')

        Notes:
            Buttons are grouped thanks to the groupname variable. If you add some update button
            you need to do it after including all your data.
        """
        self._add_button_group(groupname, direction)
        index = self.button_group_to_index[groupname]
        self.updatemenus[index]['buttons'].append(dict(label=label, method=method, args=args))

    def get_fig(self):
        """ Return the final figure

        Notes:
            you can use in the plotly.offline.(i)plot functions
        """
        self._place_buttons()
        self.layout['updatemenus'] = self.updatemenus
        self.layout['shapes'] = self.shapes
        return dict(data=self.data, layout=self.layout)


class PlotlyHelperPlane(PlotlyHelper):
    """ Helper to create plotly figure with plane helpers """

    def __init__(self, title, plane):
        self.plane = self._sanitize_plane(plane)
        title = self._get_title(title, plane)
        super(PlotlyHelperPlane, self).__init__(title, self._get_layout_skeleton(title, self.plane))

    @staticmethod
    def _get_title(title, plane):
        """ Return the title with the correct plane name

        Args:
            title: the title for the plot.
            plane: the sanitized plane used for this plot
        """
        return '{}-{}'.format(title, plane)

    @staticmethod
    def _sanitize_plane(plane):
        """ sanitizer for the plane input

        Args:
            plane: a string that should be a combination of 'x', 'y' or 'z'

        Returns :
            A sanitized plane such as xyz, xy, xz, zy

        Raises:
            TypeError: if the plane provided is not a string type
            ValueError: if the plane input is not composed of 2 characters or not a 2-combination
            of x, y and z or 3d

        Notes:
            Good values are : 3d, xy, xz, zy ...
        """
        if not isinstance(plane, six.string_types):
            raise TypeError('plane argument must be a string')
        plane = plane.lower()
        if len(plane) > 2:
            raise ValueError('plane argument must be "3d" or a 2-combination of x, y and z')
        if plane == '3d':
            plane = 'xyz'
        else:
            values = 'xyz'
            correct = sum(1 if v in plane else 0 for v in values) == 2
            if not correct or plane[0] == plane[1]:
                raise ValueError('plane argument is not formed of a 2-combination of x, y, and z')
        return plane

    @staticmethod
    def _get_camera(plane):
        """ Get the default camera for 3d scene or 2d scenes

        Args:
            plane: a string that should be a combination of 'x', 'y' or 'z'

        Notes:
            For 2d scene the camera is simply positioned in such a way that for xy plane, the
            x axis is from left to right and y for bottom to up.
        """
        camera = dict(up=dict(x=0, y=0, z=0), center=dict(x=0, y=0, z=0), eye=dict(x=0, y=0, z=0))
        if plane == 'xyz':
            camera['up'] = dict(x=0, y=0, z=1)
            camera['eye'] = dict(x=-1.7428, y=1.0707, z=0.7100, )
        else:
            unit = {v: np.eye(3)[i] for i, v in enumerate('xyz')}
            sign_cross = np.sum(np.sign(np.cross(unit[plane[0]], unit[plane[1]])))
            camera['eye'][list(set('xyz') - set(plane))[0]] = sign_cross * 2
            camera['up'][plane[1]] = 1
        return camera

    @staticmethod
    def _get_scene(plane):
        """ Get the default scene for a given plane

        Args:
            plane: a string that should be a combination of 'x', 'y' or 'z'

        Notes:
            For 2d scene the camera is simply positioned in such a way that for xy plane, the
            x axis is from left to right and y for bottom to up.
            The colors for the planes, background etc are set here.
        """
        dragmode = 'zoom' if plane != 'xyz' else 'turntable'
        scene = dict(xaxis=None, yaxis=None, zaxis=None, aspectmode='data',
                     dragmode=dragmode, camera=PlotlyHelperPlane._get_camera(plane))
        for axis in 'xyz':
            axis_name = axis + 'axis'
            scene[axis_name] = dict(
                gridcolor='rgb(255, 255, 255)',
                zerolinecolor='rgb(255, 255, 255)',
                showbackground=True,
                backgroundcolor='rgb(238, 238,238)',
                visible=True,
            )
        return scene

    @staticmethod
    def _get_layout_skeleton(title, plane):
        """ Returns a layout skeleton that is camera compliant """
        layout = dict(autosize=True, title=title,
                      scene=PlotlyHelperPlane._get_scene(plane),
                      legend=PlotlyHelperPlane._get_legend())
        return layout

    def add_plane_buttons(self):
        """ Add the plane buttons to the plot """
        if self.plane == 'xyz':
            self.add_button('3D view', 'relayout', ['scene', PlotlyHelperPlane._get_scene('xyz')],
                            'view', 'right')
            self.add_button('XY view', 'relayout', ['scene', PlotlyHelperPlane._get_scene('xy')],
                            'view')
            self.add_button('XZ view', 'relayout', ['scene', PlotlyHelperPlane._get_scene('xz')],
                            'view')
            self.add_button('YZ view', 'relayout', ['scene', PlotlyHelperPlane._get_scene('yz')],
                            'view')


def plot_fig(fig, filename, auto_open=True, show_link=False):
    """ Create the html file """
    if os.path.splitext(filename)[1] != '.html':
        filename += '.html'
    plot(fig, filename=filename, auto_open=auto_open, show_link=show_link)


def iplot_fig(fig, filename, show_link=False):  # pragma: no cover
    """ Plot the figure inside a jupyter notebook """
    if os.path.splitext(filename)[1] != '.html':
        filename += '.html'
    iplot(fig, filename=filename, show_link=show_link)
