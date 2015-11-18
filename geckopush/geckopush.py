"""
Geckopush was built for Python 3.
Author: Patrick Lee (me@patricklee.nyc)
Git Repo: http://www.github.com/patleeman/geckopush
"""

import urllib.request
import json


class Dashboard(object):
    """
    Dashboard object.  Used to hold the dashboard's API key and a collection
    of all the widgets that have been created from this instance.
    push_all() function allows a user to push to all associated dashboards.
    """
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
    """
    Main widget object for all other custom widgets to inherit from.  This
    class houses the main push function as well as the final payload
    assembly steps.
    """
    def __init__(self, dashboard, widget_key):
        self.dashboard = dashboard
        self.api_key = dashboard.api_key
        self.widget_key = widget_key
        self.payload = {
            "api_key": self.api_key,
            "data": {
                "item": [

                ]
            }
        }
        dashboard.widgets.append(self)

    def __str__(self):
        print("Dashboard: {}, Widget_Key: {}".format(self.dashboard,
                                                     self.widget_key))

    def __repr__(self):
        print("<geckopush Object (Dasboard: {}; Widget Key: {}>".format(
            self.dashboard,
            self.widget_key
        ))

    def _assemble_payload(self, _data_module):
        self.payload["data"] = _data_module

    def _assemble_data(self, *args, **kwargs):
        pass

    def add(self, *args, **kwargs):
        raise GeckoboardException("Method has no effect in this widget")

    def add_data(self, *args, **kwargs):
        raise GeckoboardException("Method has no effect in this widget")

    def push(self):
        self._assemble_data()
        _api_endpoint = 'https://push.geckoboard.com/v1/send/'\
                        '{widget_key}'.format(widget_key=self.widget_key)
        _payload_json = json.dumps(self.payload).encode('utf-8')
        _request = urllib.request.Request(url=_api_endpoint,
                                          data=_payload_json
                                          )
        _request.add_header('Content-Type', 'application/json')

        try:
            _response = urllib.request.urlopen(_request)
            _api_status = json.loads(_response.read().decode('utf-8'))
            _name = str(self.__class__)
            _name_truncated = _name[8:len(_name)-2]
            print("API Success ({}): {}".format(_name_truncated,
                                                _api_status["success"]))
            return _api_status

        except urllib.request.HTTPError as e:
            print(e)
            return e

    def get_payload(self):
        self._assemble_data()
        return self.payload


class GeckoboardException(Exception):
    pass


# The following subclasses all inherit from the Widget superclass.
class BarChart(Widget):
    def __init__(self, data=None, x_axis_labels=None,
                 x_axis_type=None, y_axis_format=None, y_axis_unit=None,
                 *args, **kwargs):
        super(BarChart, self).__init__(*args, **kwargs)
        self.data = []
        self.x_axis_labels = x_axis_labels
        self.x_axis_type = x_axis_type
        self.y_axis_format = y_axis_format
        self.y_axis_unit = y_axis_unit

        if data is not None:
            self.add_data(data=data)

    def add_data(self, data, *args, **kwargs):
        self.data.append(
            {
                "data": data
            }
        )

    def add(self, x_axis_labels=None, x_axis_type=None, y_axis_format=None,
            y_axis_unit=None):
        if x_axis_labels is not None:
            self.x_axis_labels = x_axis_labels
        if x_axis_type is not None:
            self.x_axis_type = x_axis_type
        if y_axis_format is not None:
            self.y_axis_format = y_axis_format
        if y_axis_unit is not None:
            self.y_axis_unit = y_axis_unit

    def _assemble_data(self):
        if len(self.data) == 0:
            raise GeckoboardException("Widget missing required data.")

        _data = {
            "x_axis": {},
            "y_axis": {},
            "series": self.data
        }

        if self.x_axis_labels is not None:
            _data["x_axis"]["labels"] = self.x_axis_labels

        if self.x_axis_type is not None:
            _data["x_axis"]["type"] = self.x_axis_type

        if self.y_axis_format is not None:
            _data["y_axis"]["format"] = self.y_axis_format

        if self.y_axis_unit is not None:
            _data["y_axis"]["unit"] = self.y_axis_unit

        self._assemble_payload(_data)


class BulletGraph(Widget):
    def __init__(self, orientation=None, label=None, axis=None,
                 red_start=None, red_end=None, amber_start=None,
                 amber_end=None, green_start=None, green_end=None,
                 measure_start=None, measure_end=None, projected_start=None,
                 projected_end=None, comparative=None, sublabel=None,
                 *args, **kwargs):
        super(BulletGraph, self).__init__(*args, **kwargs)
        self.orientation = orientation
        self.data = []

        _necessary = [label, axis, red_start, red_end, amber_start, amber_end,
                      green_start, green_end, measure_start, measure_end,
                      projected_start, projected_end, comparative]

        # Check if any of the _necessary elements are None (not entered)
        _necessary_none = list(bool(item is None) for item in _necessary)

        # is True if all elements of _necessary_none are True.
        _is_all_none = all(_necessary_none)

        if not _is_all_none:
            self.add_data(label, axis, red_start, red_end, amber_start,
                          amber_end, green_start, green_end, measure_start,
                          measure_end, projected_start, projected_end,
                          comparative, sublabel)

    def add(self, orientation=None, *args, **kwargs):
        if orientation is not None:
            self.orientation = orientation

    def add_data(self, label, axis, red_start, red_end, amber_start,
                 amber_end, green_start, green_end, measure_start, measure_end,
                 projected_start, projected_end, comparative, sublabel=None):

        if len(self.data) >= 4:
            raise GeckoboardException(
                "Bullet Graphs support a maximum of 4 multiples."
            )

        self._all_or_none(label, axis, red_start, red_end, amber_start,
                          amber_end, green_start, green_end, measure_start,
                          measure_end, projected_start, projected_end,
                          comparative)

        _item_payload = {
                        "label": label,
                        "axis": {
                            "point": axis,
                        },
                        "range": {
                            "red": {
                                "start": red_start,
                                "end": red_end
                            },
                            "amber": {
                                "start": amber_start,
                                "end": amber_end

                            },
                            "green": {
                                "start": green_start,
                                "end": green_end
                            }
                        },
                        "measure": {
                            "current": {
                                "start": measure_start,
                                "end": measure_end
                            },
                            "projected": {
                                "start": projected_start,
                                "end": projected_end
                            }
                        },
                        "comparative": {
                            "point": comparative
                            }
                        }
        if sublabel is not None:
            _item_payload["sublabel"] = sublabel

        self.data.append(_item_payload)

    @staticmethod
    def _all_or_none(label, axis, red_start, red_end, amber_start,
                     amber_end, green_start, green_end, measure_start,
                     measure_end, projected_start, projected_end,
                     comparative):
        """
        Method to check if all the required elements are supplied, otherwise
        raise an exception.
        """
        # Check to make sure that all or none of the required fields are added
        _necessary = [label, axis, red_start, red_end, amber_start, amber_end,
                      green_start, green_end, measure_start, measure_end,
                      projected_start, projected_end, comparative]
        _necessary_none = list(bool(item is None) for item in _necessary)
        _is_all_none = all(_necessary_none)
        _is_all_not_none = all(not x for x in _necessary_none)
        if _is_all_none == _is_all_not_none:
            raise GeckoboardException("Missing required data point(s).")
        return True

    def _assemble_data(self):
        _data = {
            "orientation": self.orientation,
            "item": None
        }
        _item = self.data

        if len(_item) == 1:
            _data["item"] = _item[0]
        else:
            _data["item"] = _item

        self._assemble_payload(_data)


class Funnel(Widget):
    def __init__(self, value=None, label=None, funnel_type=None,
                 percentage=None, *args, **kwargs):
        super(Funnel, self).__init__(*args, **kwargs)
        self.funnel_type = funnel_type
        self.percentage = percentage
        self.data = []
        if value is not None and label is not None:
            self.data.append({"value": value, "label": label})

    def add_data(self, value, label):
        if len(self.data) >= 8:
            raise GeckoboardException(
                "Funnel widgets support a max of 8 steps."
            )

        _step = {
            "value": value,
            "label": label,
        }
        self.data.append(_step)

    def _assemble_data(self):
        if len(self.data) == 0:
            raise GeckoboardException("Must add at least one value.")

        _data = {
            "item": self.data
        }
        if self.funnel_type is not None:
            _data["type"] = self.funnel_type

        if self.percentage is not None:
            _data["percentage"] = self.percentage

        self._assemble_payload(_data)


class GeckoMeter(Widget):
    def __init__(self, item=None, min_value=None, max_value=None,
                 *args, **kwargs):
        super(GeckoMeter, self).__init__(*args, **kwargs)
        self.item = item
        self.min_value = min_value
        self.max_value = max_value

    def add_data(self, item, min_value, max_value):
        if self.item is not None \
                or self.min_value is not None \
                or self.max_value is not None:
            raise GeckoboardException("Widget already initialized")

        self.item = item
        self.min_value = min_value
        self.max_value = max_value

    def _assemble_data(self):
        if self.item is None \
                or self.min_value is None \
                or self.max_value is None:
            raise GeckoboardException("Widget missing required data.")

        _data = {
            "item": self.item,
            "min": {
                "value": self.min_value
            },
            "max": {
                "value": self.max_value
            }
        }
        self._assemble_payload(_data)


class HighCharts(Widget):
    def __init__(self, highchart=None, *args, **kwargs):
        super(HighCharts, self).__init__(*args, **kwargs)
        self.highchart = highchart

    def add_data(self, highchart):
        if self.highchart is not None:
            raise GeckoboardException("Widget already initialized.")

        self.highchart = highchart

    def _assemble_data(self):
        if not isinstance(self.highchart, str):
            raise TypeError("Highchart must be a string object")
        if self.highchart is None:
            raise GeckoboardException("Widget missing required data.")

        _data = {
            "highchart": self.highchart
        }
        self._assemble_payload(_data)


class Leaderboard(Widget):
    def __init__(self, label=None, value=None, previous_rank=None,
                 number_format=None, unit=None, *args, **kwargs):
        super(Leaderboard, self).__init__(*args, **kwargs)
        self.number_format = number_format
        self.unit = unit
        self.data = []

        if label is not None:
            self.add_data(label, value, previous_rank)

    def add_data(self, label, value=None, previous_rank=None):
        _item = {
            "label": label
        }

        if value is not None:
            _item["value"] = value

        if previous_rank is not None:
            _item["previous_rank"] = previous_rank

        self.data.append(_item)

    def _assemble_data(self):
        if len(self.data) > 22:
            raise GeckoboardException(
                "Leaderboard widget accepts a max of 22 labels"
            )
        elif len(self.data) == 0:
            raise GeckoboardException("Must add at least one value.")

        _data = {
            "items": self.data
        }
        if self.number_format is not None:
            _data["format"] = self.number_format

        if self.unit is not None:
            _data["unit"] = self.unit

        self._assemble_payload(_data)


class LineChart(Widget):
    def __init__(self, data=None, name=None, incomplete_from=None,
                 series_type=None, x_axis_labels=None, x_axis_type=None,
                 y_axis_format=None, y_axis_unit=None, *args, **kwargs):
        super(LineChart, self).__init__(*args, **kwargs)
        self.x_axis_labels = x_axis_labels
        self.x_axis_type = x_axis_type
        self.y_axis_format = y_axis_format
        self.y_axis_unit = y_axis_unit
        self.data = []

        if data is not None:
            self.add_data(data, name, incomplete_from, series_type)

    def add_data(self, data, name=None, incomplete_from=None, series_type=None,
                 *args, **kwargs):
        _series = {
            "data": data
        }

        if name is not None:
            _series["name"] = name
        if series_type is not None:
            _series["type"] = series_type
        if incomplete_from is not None:
            _series["incomplete_from"] = incomplete_from

        self.data.append(_series)

    def add(self, x_axis_labels=None, x_axis_type=None, y_axis_format=None,
            y_axis_unit=None):
        if x_axis_labels is not None:
            self.x_axis_labels = x_axis_labels
        if x_axis_type is not None:
            self.x_axis_type = x_axis_type
        if y_axis_format is not None:
            self.y_axis_format = y_axis_format
        if y_axis_unit is not None:
            self.y_axis_unit = y_axis_unit

    def _label_data_check(self):
        _is_pairs = [bool(self._data_check(x["data"])) for x in self.data]
        if all(_is_pairs) and self.x_axis_labels is not None:
            raise GeckoboardException("Two x-axis labels provided.")
        elif not all(not x for x in _is_pairs) and not all(_is_pairs):
            raise GeckoboardException("Can not mix pairs and lists.")

    @staticmethod
    def _data_check(data):
        """
        Check whether data is an [x,y] array or as a list [x,y,z].
        """
        if data is None:
            pass
        elif data is not None:
            return bool(any(isinstance(l, list) for l in data))

    def _assemble_data(self):
        if len(self.data) == 0:
            raise GeckoboardException("Must add at least one value.")

        self._label_data_check()  # Run through pair/list data checking.

        _data = {
            "series": self.data,
            "y_axis": {},
            "x_axis": {}
        }

        if self.x_axis_labels is not None:
            _data["x_axis"]["labels"] = self.x_axis_labels

        if self.x_axis_type is not None:
            _data["x_axis"]["type"] = self.x_axis_type

        if self.y_axis_format is not None:
            _data["y_axis"]["format"] = self.y_axis_format

        if self.y_axis_unit is not None:
            _data["y_axis"]["unit"] = self.y_axis_unit

        self._assemble_payload(_data)


class List(Widget):
    def __init__(self, text=None, name=None, color=None,
                 description=None, *args, **kwargs):
        super(List, self).__init__(*args, **kwargs)
        self.data = []

        if text is not None:
            self.add_data(text, name, color, description)

    def add_data(self, text, name=None, color=None, description=None):
        _data = {
            "title": {
                "text": text
            }
        }

        if name is not None and color is not None:
            _data["label"] = {}

        if name is not None:
            _data["label"]["name"] = name

        if color is not None:
            _data["label"]["color"] = color

        if description is not None:
            _data["description"] = description

        self.data.append(_data)

    def _assemble_data(self, *args, **kwargs):
        self._assemble_payload(self.data)


class Map(Widget):
    def __init__(self, city_name=None, country_code=None,
                 region_code=None, latitude=None, longitude=None, ip=None,
                 host=None, color=None, size=None, *args, **kwargs):
        super(Map, self).__init__(*args, **kwargs)
        self.data = []

        self._data_check(city_name, country_code, region_code, latitude,
                         longitude, ip, host)

        self.add_data(city_name, country_code, region_code, latitude,
                      longitude, ip, host, color, size)

    @staticmethod
    def _data_check(city_name=None, country_code=None,
                    region_code=None, latitude=None, longitude=None, ip=None,
                    host=None):
        """
        Method to check whether the right combinations of values have been
        submitted, otherwise raise an error.
        """

        # Checking if country code or region is provided but not city name
        if country_code or region_code is not None:
            if city_name is None:
                raise GeckoboardException("Widget missing required data.")

        # Checking for a missing longitude or latitude
        if bool(latitude) == bool(not longitude):
            raise GeckoboardException("Widget missing required data.")

        # Check if more than one set of data is added at a time.
        _combos = [any((city_name, country_code, region_code)),
                   any((latitude, longitude)),
                   bool(ip),
                   bool(host)]

        if sum(_combos) > 1:
            raise GeckoboardException(
                "Too much data.  Add one point at a time."
            )

    def add_data(self, city_name=None, country_code=None,
                 region_code=None, latitude=None, longitude=None, ip=None,
                 host=None, color=None, size=None, *args, **kwargs):

        self._data_check(city_name, country_code, region_code, latitude,
                         longitude, ip, host)

        _point = {}
        if city_name is not None:
            _point["city"] = {}
            _point["city"]["city_name"] = city_name

        if country_code is not None:
            _point["city"]["country_code"] = country_code

        if region_code is not None:
            _point["city"]["region_code"] = region_code

        if latitude is not None:
            _point["latitude"] = latitude

        if longitude is not None:
            _point["longitude"] = longitude

        if host is not None:
            _point["host"] = host

        if ip is not None:
            _point["ip"] = ip

        if color is not None:
            _point["color"] = color

        if size is not None:
            _point["size"] = size

        # Need a check because __init__ pushes all parameters into this fn
        # no matter if all values are None or populated
        if len(_point) > 0:
            self.data.append(_point)

    def _assemble_data(self, *args, **kwargs):
        _data = {
            "points": {
                "point": self.data
            }
        }

        self._assemble_payload(_data)


class Monitoring(Widget):
    def __init__(self, status=None, downtime=None, responsetime=None,
                 *args, **kwargs):
        super(Monitoring, self).__init__(*args, **kwargs)
        self.status = status
        self.downtime = downtime
        self.responsetime = responsetime

    def add_data(self, status, downtime=None, responsetime=None,
                 *args, **kwargs):
        if self.status is not None:
            raise GeckoboardException("Widget already initialized")
        else:
            self.status = status

        if downtime is not None:
            self.downtime = downtime

        if responsetime is not None:
            self.responsetime = responsetime

    def _assemble_data(self, *args, **kwargs):
        _data = {
            "status": self.status
        }

        if self.downtime is not None:
            _data["downTime"] = self.downtime

        if self.responsetime is not None:
            _data["responseTime"] = self.responsetime

        self._assemble_payload(_data)


class NumberAndSecondaryStat(Widget):
    def __init__(self, primary_value=None, secondary_value=None, text=None,
                 prefix=None, metric_type=None, absolute=None,
                 *args, **kwargs):
        super(NumberAndSecondaryStat, self).__init__(*args, **kwargs)
        self.metric_type = metric_type
        self.absolute = absolute
        self.data = []
        if primary_value is not None:
            self.add_data(primary_value, secondary_value, text, prefix)

    def add_data(self, primary_value, secondary_value=None, text=None,
                 prefix=None, *args, **kwargs):

        if secondary_value is None and text is not None:
            _item = {
                "value": primary_value
            }
            if text is not None:
                _item["text"] = text
            if prefix is not None:
                _item["prefix"] = prefix
            self.data.append(_item)

        elif secondary_value is not None and text is None:
            _item_1 = {
                    "value": primary_value
                }
            self.data.append(_item_1)

            # Check if secondary value is an integer or float
            if isinstance(secondary_value, int) or \
                    isinstance(secondary_value, float):

                _item_2 = {
                    "value": secondary_value
                }
                self.data.append(_item_2)

            # Check if the secondary value is a list and attach as an array as
            # per geckoboard api docs.
            elif isinstance(secondary_value, list):
                self.data.append(secondary_value)

        elif secondary_value is not None and text is not None:
            _item_1 = {
                    "value": primary_value,
                    "text": text
                }
            self.data.append(_item_1)

            # Check if secondary value is an integer or float
            if isinstance(secondary_value, int) or \
                    isinstance(secondary_value, float):

                _item_2 = {
                    "value": secondary_value
                }
                self.data.append(_item_2)

            # Check if the secondary value is a list, throw error if it is.
            elif isinstance(secondary_value, list):
                raise GeckoboardException(
                    "Secondary value can not be a list when both text and secondary value supplied."
                )

        elif secondary_value is None and text is None:
            _item = {
                "value": primary_value
            }
            self.data.append(_item)

        else:
            raise GeckoboardException(
                "Widget accepts text or a secondary value only."
            )

    def add(self, metric_type=None, absolute=None, *args, **kwargs):
        if metric_type is not None:
            self.metric_type = metric_type
        if absolute is not None:
            self.absolute = absolute

    def _assemble_data(self, *args, **kwargs):
        _data = {
            "item": self.data
        }
        if self.metric_type is not None:
            _data["type"] = self.metric_type

        if self.absolute is not None:
            _data["absolute"] = self.absolute

        self._assemble_payload(_data)


class PieChart(Widget):
    def __init__(self, value=None, label=None, color=None, *args, **kwargs):
        super(PieChart, self).__init__(*args, **kwargs)
        self.data = []

        if value is not None and label is not None:
            self.add_data(value, label, color)

    def add_data(self, value, label, color=None, *args, **kwargs):
        _slice = {
            "value": value,
            "label": label
        }

        if color is not None:
            _slice["color"] = color

        self.data.append(_slice)

    def _assemble_data(self, *args, **kwargs):
        _item = {
            "item": self.data
        }
        self._assemble_payload(_item)


class RAG(Widget):
    def __init__(self, text=None, value=None, prefix=None, reverse_type=None,
                 color=None, *args, **kwargs):
        super(RAG, self).__init__(*args, **kwargs)
        self.reverse_type = reverse_type
        self.data = [None, None, None]

        if text is not None:
            self.add_data(text, value, prefix, color=color)

    # Added color optional variable to facilitate placing the _color dict in
    # the right position.
    def add_data(self, text, value=None, prefix=None, color=None,
                 *args, **kwargs):
        if len(self.data) > 3:
            raise GeckoboardException(
                "This widget accepts a maximum of 3 items"
            )

        _color = {
            "text": text,
        }

        if value is not None:
            _color["value"] = value

        if prefix is not None:
            _color["prefix"] = prefix

        # Place _color data in proper position.
        if color is not None:
            if color == "red":
                self.data[0] = _color
            elif color == "amber":
                self.data[1] = _color
            elif color == "green":
                self.data[2] = _color
            else:
                GeckoboardException("Not a valid color")
        else:
            for i, item in enumerate(self.data):
                if item is None:
                    self.data[i] = _color
                    break

    def add(self, reverse_type=None, *args, **kwargs):
        if reverse_type is not None:
            self.reverse_type = reverse_type

    def _assemble_data(self, *args, **kwargs):
        # Remove any None values in self.item before appending it to payload.
        # If the value is omitted, the color will not be displayed.
        for i, item in enumerate(self.data):
            if item is None:
                item[i] = {"text": ""}

        _data = {
            "item": self.data
        }

        if self.reverse_type is not None:
            _data["type"] = self.reverse_type

        self._assemble_payload(_data)


class Text(Widget):
    def __init__(self, text=None, text_type=None, *args, **kwargs):
        super(Text, self).__init__(*args, **kwargs)
        self.data = []

        if text is not None:
            self.add_data(text, text_type)

    def add_data(self, text, text_type=None, *args, **kwargs):
        _item = {
            "text": text
        }
        if type is not None:
            _item["type"] = text_type

        self.data.append(_item)

    def _assemble_data(self, *args, **kwargs):
        if len(self.data) > 10:
            raise GeckoboardException("Text accepts a max of 10 items.")
        elif len(self.data) == 0:
            raise GeckoboardException("Must provide at least one item")

        _data = {
            "item": self.data
        }

        self._assemble_payload(_data)
