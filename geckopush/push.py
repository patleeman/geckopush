import json


class Widget(object):
    _api_endpoint = 'https://push.geckoboard.com/v1/send/'

    def __init__(self):
        self.payload = {
            "api_key": None,
            "data": {
                "item": [

                ]
            }
        }

    def push(self):
        # Form api endpoint

        # Push to geckoboard
        pass

    #Form the item payload
    def _form_payload(self):
        pass
    

class Dashboard(object):
    def __init__(self, api_key):
        self.api_key = api_key


    def __repr__(self):
        return "<DASHBOARD OBJECT, API KEY: {api_key}>".format(
            api_key=self.api_key)


class BarChart(Widget):
    _widget_payload = super().payload["data"]["item"]


    def __init__(self, dashboard, widget_key, data):
        self.api_key = dashboard.api_key
        self.widget_key = widget_key
        self.data = data
        self.x_axis_labels = None
        self.x_axis_type = None
        self.y_axis_format = None
        self.y_axis_unit = None
        super().__init__()

        # Call instance to form payload:



    #Attach to widget payload

        #Call super's push function.


'''{
  "x_axis": {
    "labels": [
      "2000",
      "2001",
      "2002",
      "2003",
      "2004",
      "2005"
    ]
  },
  "y_axis": {
    "format": "currency",
    "unit": "USD"
  },
  "series": [
    {
      "data": [
        1000,
        1500,
        30600,
        28800,
        22300,
        36900
      ]
    }
  ]
}
'''
