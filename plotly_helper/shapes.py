'''An API to get primitive shapes'''
# pylint: disable=invalid-name


def line(x0, y0, x1, y1, color=None, width=None):
    '''Return a line shape

    args:
        x0, y0, x1, y1: beginning and end of line
        color (str): a plotly color string
        width (int): line width
    '''
    data = {
        'type': 'line',
        'x0': x0, 'y0': y0, 'x1': x1, 'y1': y1,
        'line': {}
    }
    if color:
        data['line']['color'] = color

    if width:
        data['line']['width'] = width

    return data


def circle(x, y, radius, color=None, width=None):
    '''Return a circle shape

    args:
        x, y (float): center coordinates
        radius (float): circle radius
        color (str): a plotly color string
        width (int): line width
    '''
    data = {
        'type': 'circle',
        'xref': 'x',
        'yref': 'y',
        'fillcolor': 'rgba(50, 171, 96, 0.7)',
        'x0': x - radius,
        'y0': y - radius,
        'x1': x + radius,
        'y1': y + radius,
        'line': {
        },
    }
    if color:
        data['line']['color'] = color

    if width:
        data['line']['width'] = width

    return data
