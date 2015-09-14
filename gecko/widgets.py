

class Widget(object):
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.api_endpoint = 'https://push.geckoboard.com/v1/send/'


    def push(self):
        pass


class BarChart(Widget):
    def __init__(self, widget_key=None,
                 x_axis_labels=None,
                 x_axis_type=None,
                 y_axis_format=None,
                 y_axis_unit=None):
        self.widget_key = widget_key
        self.x_axis_labels = x_axis_labels
        self.x_axis_type = x_axis_type
        self.y_axis_format = y_axis_format
        self.y_axis_unit = y_axis_format
