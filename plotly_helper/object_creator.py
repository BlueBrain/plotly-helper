""" Pre defined function to create plotly object easily """
import numpy as np
import plotly.graph_objs as go

from plotly_helper.helper import PlotlyObjectProperties


def create_scatter_line(points, properties=None):
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
    if properties is None:
        properties = PlotlyObjectProperties()
    obj = go.Scatter3d(visible=properties.visible, marker=dict(size=3, color=properties.color),
                       line=dict(width=5, color=properties.color),
                       x=points[:, 0], y=points[:, 1], z=points[:, 2],
                       showlegend=properties.showlegend, opacity=properties.opacity)
    if properties.name:
        obj.name = properties.name
    return obj


def create_scatter(points, properties=None):
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
    if properties is None:
        properties = PlotlyObjectProperties()
    scatter = create_scatter_line(points, properties)
    scatter.mode = 'markers'
    return scatter


def create_point(point, properties=None):
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
    if properties is None:
        properties = PlotlyObjectProperties()
    return create_scatter(np.array([point, ]), properties)


def create_vector(point1, point2, properties=None):
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
    if properties is None:
        properties = PlotlyObjectProperties()
    return create_scatter_line(np.vstack((point1, point2)), properties)
