""" Pre defined function to create plotly object easily """
import numpy as np
import plotly.graph_objs as go


def scatter_line(points, name=None, color=None, width=5, visible=True,
                 showlegend=True, opacity=1.0, marker_size=3):
    """ Create a line scatter plot from an array of points

    Args :
        points: points used to create the scatter (np.array([[x1,y1,z1], ..., [x2,y2,z2]]))
        color: a css color name or rgb (string)
        visible: switch for visibility (bool)
        showlegend: boolean to add object to the legend
        opacity: set the opacity value (float)
        marker_size: size of marker (set to small value to get lines)

    Returns :
        A scatter plot representing points
    """
    args = dict(visible=visible, marker=dict(size=marker_size, color=color),
                line=dict(width=width, color=color),
                x=points[:, 0], y=points[:, 1],
                showlegend=showlegend, opacity=opacity)

    if points.shape[1] == 3:
        scatter_fun = go.Scatter3d
        args['z'] = points[:, 2]
    else:
        scatter_fun = go.Scattergl

    obj = scatter_fun(**args)
    if name:
        obj.name = name
    return obj


def scatter(points, name=None, color=None, width=5, visible=True, showlegend=True, opacity=1.0):
    """ Create a scatter plot from a numpy array of points

    Args :
        points: points used to create the scatter (np.array([[x1,y1,z1], ..., [x2,y2,z2]]))
        color: a css color name or rgb (string)
        visible: switch for visibility (bool)
        showlegend: boolean to add object to the legend
        opacity: set the opacity value (float)

    Returns :
        A scatter plot representing points
    """
    obj = scatter_line(points, name, color, width, visible, showlegend, opacity)
    marker = dict(
        line=dict(width=width, color=color),
        color=color,
        size=width,
    )
    obj['marker'] = marker
    obj.mode = 'markers'
    return obj


# pylint: disable=redefined-outer-name
def point(point, name=None, color=None, width=5, visible=True, showlegend=True, opacity=1.0):
    """ Create a single point

    Args :
        p: a point to represent (array([x,y,z]))
        color: a css color name or rgb (string)
        visible: switch for visibility (bool)
        showlegend: boolean to add object to the legend
        opacity: set the opacity value (float)

    Returns :
        A scatter plot representing one point
    """
    return scatter(np.array([point, ]), name, color, width, visible, showlegend, opacity)


def vector(point1, point2, name=None, color=None, width=5, visible=True, showlegend=True,
           opacity=1.0):
    """ Create a 3d vector using 2 numpy arrays

    Args :
        p1: a point coordinates (array([x1,y1,z1]))
        p2: a point coordinates (array([x2,y2,z2]))
        color: a css color name or rgb (string)
        visible: switch for visibility (bool)
        showlegend: boolean to add object to the legend
        opacity: set the opacity value (float)

    Returns :
        a scatter plot representing vector for plotly
    """
    return scatter_line(np.vstack((point1, point2)), name, color, width, visible, showlegend,
                        opacity)
