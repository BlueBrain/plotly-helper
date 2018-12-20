""" Pre defined function to create plotly object easily """
import numpy as np
import plotly.graph_objs as go


def create_scatter_line(points, name='', color='red', visible=True, showlegend=True, opacity=1.):
    """ Create a line scatter plot from an array of points

    Args :
        points: points used to create the scatter (np.array([[x1,y1,z1], ..., [x2,y2,z2]]))
        color: a css color name or rgb (string)
        visible: switch for visibility (bool)
        showlegend: boolean to add object to the legend
        opacity: set the opacity value (float)

    Returns :
        A scatter plot representing points
    """
    obj = go.Scatter3d(visible=visible, marker=dict(size=3, color=color),
                       line=dict(width=5, color=color),
                       x=points[:, 0], y=points[:, 1], z=points[:, 2], showlegend=showlegend,
                       opacity=opacity)
    if name:
        obj.name = name
    return obj


def create_scatter(points, name='', color='red', visible=True, showlegend=True, opacity=1.):
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
    scatter = create_scatter_line(points, name=name, color=color, visible=visible,
                                  showlegend=showlegend, opacity=opacity)
    scatter.mode = 'markers'
    return scatter


def create_point(p, name='', color='red', visible=True, showlegend=True, opacity=1.):
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
    return create_scatter(np.array([p, ]), name=name, color=color, visible=visible,
                          showlegend=showlegend, opacity=opacity)


def create_vector(p1, p2, name='', color='red', visible=True, showlegend=True, opacity=1.):
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
    return create_scatter_line(np.vstack((p1, p2)), name=name, color=color, visible=visible,
                               showlegend=showlegend, opacity=opacity)
