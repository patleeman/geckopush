import urllib.request
import json


class Dashboard(object):
    '''
    Dashboard object.  Used to hold the dashboard's API key and a collection
    of all the widgets that have been created from this instance.
    push_all() function allows a user to push to all associated dashboards.
    '''
    def __init__(self, api_key):
        self.api_key = api_key
        self.widgets = []

    def __repr__(self):
        return "<DASHBOARD OBJECT, API KEY: {api_key}>".format(
            api_key=self.api_key)

    def push_all(self):
        for widget in self.widgets:
            widget.push()


class Widget(object):
    '''
    Main widget object for all other custom widgets to inherit from.  This
    class houses the main push function as well as the final payload
    assembly steps.
    '''
    def __init__(self, dashboard):
        self.dashboard = dashboard
        self.api_key = dashboard.api_key
        self.widget_key = None
        self.payload = {
            "api_key": self.api_key,
            "data": {
                "item": [

                ]
            }
        }
        dashboard.widgets.append(self)


    def _assemble_item(self):
        pass

    def _assemble_payload(self, _data_module):
        self.payload["data"] = _data_module

    def push(self):
        self._assemble_item()
        _api_endpoint = 'https://push.geckoboard.com/v1/send/'\
                        '{widget_key}'.format(widget_key=self.widget_key)
        _payload_json = json.dumps(self.payload).encode('utf-8')
        _request = urllib.request.Request(url=_api_endpoint,
                                          data=_payload_json
                                          )
        _request.add_header('Content-Type', 'application/json')
        try:
            _response = urllib.request.urlopen(_request)
            _api_status = _response.read()
            print(_api_status)
        except urllib.request.HTTPError as e:
            print(e)


        # Todo: add error handling for non 200 codes to _response


class GeckoboardException(Exception):
    pass


class BarChart(Widget):
    # BarChart widget.  User must supply widget_key, data, and dashboard object.
    def __init__(self, widget_key, data, *args, **kwargs):
        super(BarChart, self).__init__(*args, **kwargs)
        self.widget_key = widget_key
        self.data = data
        self.x_axis_labels = None
        self.x_axis_type = None
        self.y_axis_format = None
        self.y_axis_unit = None

    def _assemble_item(self):
        _item = {
            "x_axis": {},
            "y_axis": {},
            "series": [
                {
                    "data": self.data
                }
            ]
        }

        if self.x_axis_labels is not None:
            _item["x_axis"]["labels"] = self.x_axis_labels

        if self.x_axis_type is not None:
            _item["x_axis"]["type"] = self.x_axis_type

        if self.y_axis_format is not None:
            _item["y_axis"]["format"] = self.y_axis_format

        if self.y_axis_unit is not None:
            _item["y_axis"]["unit"] = self.y_axis_unit

        self._assemble_payload(_item)


class BulletGraph(Widget):
    def __init__(self, widget_key, orientation, label, axis, red_start,
                 red_end, amber_start, amber_end, green_start, green_end,
                 measure_start, measure_end, projected_start, projected_end,
                 comparative, sublabel=None, *args, **kwargs):

        super(BulletGraph, self).__init__(*args, **kwargs)
        self.widget_key = widget_key
        self.orientation = [orientation]
        self.label = [label]
        self.axis = [axis]
        self.red_start = [red_start]
        self.red_end = [red_end]
        self.amber_start = [amber_start]
        self.amber_end = [amber_end]
        self.green_start = [green_start]
        self.green_end = [green_end]
        self.measure_start = [measure_start]
        self.measure_end = [measure_end]
        self.projected_start = [projected_start]
        self.projected_end = [projected_end]
        self.comparative = [comparative]
        self.sublabel = [sublabel]
        self.counter = 1

    def add(self, orientation, label, axis, red_start, red_end, amber_start,
            amber_end, green_start, green_end, measure_start, measure_end,
            projected_start, projected_end, comparative, sublabel=None):

        if self.counter >= 4:
            raise GeckoboardException("BarCharts support a maximum of 4 multiples.")

        self.orientation.append(orientation)
        self.label.append(label)
        self.axis.append(axis)
        self.red_start.append(red_start)
        self.red_end.append(red_end)
        self.amber_start.append(amber_start)
        self.amber_end.append(amber_end)
        self.green_start.append(green_start)
        self.green_end.append(green_end)
        self.measure_start.append(measure_start)
        self.measure_end.append(measure_end)
        self.projected_start.append(projected_start)
        self.projected_end.append(projected_end)
        self.comparative.append(comparative)
        self.sublabel.append(sublabel)
        self.counter += 1


    def _assemble_item(self):
        _item = []
        for x in range(self.counter):
            _data = {
                "orientation": self.orientation[x],
                "item": {
                    "label": self.label[x],
                    "axis": self.axis[x],
                    "range": {
                        "red": {
                            "start": self.red_start[x],
                            "end": self.red_end[x]
                        },
                        "amber": {
                            "start": self.amber_start[x],
                            "end": self.amber_end[x]

                        },
                        "green": {
                            "start": self.green_start[x],
                            "end": self.green_end[x]
                        }
                    }
                },
                "measure": {
                    "current": {
                        "start": self.measure_start[x],
                        "end": self.measure_end[x]
                    },
                    "projected": {
                        "start": self.projected_start[x],
                        "end": self.projected_end[x]
                    }
                },
                "comparative": {
                    "point": self.comparative[x]
                }
            }

            if self.sublabel is not None:
                _data["item"]["sublabel"] = self.sublabel

            _item.append(_data)

        self._assemble_payload(_item)


class Funnel(Widget):
    def __init__(self, widget_key, type=None, percentage=None, *args, **kwargs):
        super(Funnel, self).__init__(*args, **kwargs)
        self.widget_key = widget_key
        self.type=type
        self.percentage=percentage
        self.funnel_steps = []
        self.counter = 0

    def add(self, value, label):
        if self.counter >= 8:
            raise GeckoboardException("Funnel widgets support a max of 8 steps.")

        _step = {
            "value": value,
            "label": label,
        }
        self.funnel_steps.append(_step)
        self.counter += 1

    def _assemble_item(self):
        _item = {
            "item": self.funnel_steps
        }
        if self.type is not None:
            _item["type"] = self.type

        if self.percentage is not None:
            _item["percentage"] = self.percentage

        self._assemble_payload(_item)