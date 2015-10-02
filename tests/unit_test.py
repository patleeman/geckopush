from geckopush import geckopush
import unittest
import json

# Declare initial dashboard widget and test values.
d = geckopush.Dashboard(api_key="api-key-123")
widget_key = "Widget-Key"


# Monkey patch urlopen method to append the url and headers to return dict.
def dummy_urlopen(url):
    mock_api_return = {
        'success': True,
        'url': url.full_url,
        'headers': url.headers,
    }
    json_payload = json.dumps(mock_api_return)

    # The Widget.Push() method expects an object returned from the
    # urllib.request.urlopen() call.
    class Response(object):
        @staticmethod
        def read():
            return json_payload.encode('utf-8')
    return Response

geckopush.urllib.request.urlopen = dummy_urlopen

class Base(object):
    """
    Base class which sets up the payload and push tests
    """
    def setUp(self):
        self.payload = None
        self.widget = None

    def testPayload(self):
        """
        Testing the payload
        """
        generated = self.widget.get_payload()
        self.assertEqual(generated, self.payload, "Testing payload structure")

    def testPush(self):
        """
        Testing push functionality
        """
        push_result = self.widget.push()
        url = push_result['url']
        headers = push_result['headers']
        self.assertEqual(
            url,
            'https://push.geckoboard.com/v1/send/Widget-Key',
            "Testing URL structure"
        )
        self.assertEqual(
            headers,
            {'Content-type': 'application/json'}
        )


class TestBarChart(unittest.TestCase, Base):
    def setUp(self):
        self.widget = geckopush.BarChart(dashboard=d, widget_key=widget_key)
        self.widget.add_data(data=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        self.widget.x_axis_labels = ["one", "two", "three", "four", "five",
                                     "six", "seven", "eight", "nine", "ten"]
        self.widget.x_axis_type = "standard"
        self.widget.y_axis_format = "decimal"
        self.widget.y_axis_unit = "USD"
        self.payload = {'data': {'series': [{'data': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}], 'x_axis': {'labels': ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten'], 'type': 'standard'}, 'y_axis': {'unit': 'USD', 'format': 'decimal'}}, 'api_key': 'api-key-123'}



class TestBulletGraph(unittest.TestCase, Base):
    def setUp(self):
        self.payload = {'data': {'item': [{'sublabel': 'A test Bullet graph', 'comparative': {'point': '200'}, 'range': {'red': {'start': 0, 'end': 100}, 'green': {'start': 601, 'end': 1000}, 'amber': {'start': 101, 'end': 600}}, 'axis': {'point': ['0', '200', '400', '600', '800', '1000']}, 'measure': {'current': {'start': '0', 'end': '500'}, 'projected': {'start': '100', 'end': '900'}}, 'label': 'Test Bullet Graph'}, {'sublabel': 'womp womp womp', 'comparative': {'point': '100'}, 'range': {'red': {'start': 0, 'end': 200}, 'green': {'start': 301, 'end': 1000}, 'amber': {'start': 201, 'end': 300}}, 'axis': {'point': ['0', '200', '400', '600', '800', '1000']}, 'measure': {'current': {'start': '0', 'end': '800'}, 'projected': {'start': '600', 'end': '900'}}, 'label': 'Second Bullet Graph'}], 'orientation': None}, 'api_key': 'api-key-123'}
        self.widget = geckopush.BulletGraph(dashboard=d,
                                   widget_key=widget_key,
                                   label='Test Bullet Graph',
                                   axis=["0", "200", "400", "600", "800", "1000"],
                                   comparative="200",
                                   measure_start="0",
                                   measure_end="500",
                                   red_start=0,
                                   red_end=100,
                                   amber_start=101,
                                   amber_end=600,
                                   green_start=601,
                                   green_end=1000,
                                   sublabel="A test Bullet graph",
                                   projected_start='100',
                                   projected_end='900',
                                   )

        self.widget.add_data(label='Second Bullet Graph',
                             axis=["0", "200", "400", "600", "800", "1000"],
                             comparative="100",
                             measure_start="0",
                             measure_end="800",
                             red_start=0,
                             red_end=200,
                             amber_start=201,
                             amber_end=300,
                             green_start=301,
                             green_end=1000,
                             sublabel="womp womp womp",
                             projected_start='600',
                             projected_end='900'
                             )


class TestFunnel(unittest.TestCase, Base):
    def setUp(self):
        self.widget = geckopush.Funnel(dashboard=d, widget_key=widget_key)
        self.widget.add_data(100, "one hundred")
        self.widget.add_data(200, "two hundred")
        self.widget.add_data(300, "three hundred")
        self.widget.add_data(400, "four hundred")
        self.widget.add_data(500, "five hundred")
        self.widget.add_data(600, "six hundred")
        self.widget.add_data(700, "seven hundred")
        self.widget.add_data(800, "eight hundred")
        self.payload = {'data': {'item': [{'value': 100, 'label': 'one hundred'}, {'value': 200, 'label': 'two hundred'}, {'value': 300, 'label': 'three hundred'}, {'value': 400, 'label': 'four hundred'}, {'value': 500, 'label': 'five hundred'}, {'value': 600, 'label': 'six hundred'}, {'value': 700, 'label': 'seven hundred'}, {'value': 800, 'label': 'eight hundred'}]}, 'api_key': 'api-key-123'}


class TestGecko(unittest.TestCase, Base):
    def setUp(self):
        self.payload = {'data': {'max': {'value': 50}, 'item': 26, 'min': {'value': 0}}, 'api_key': 'api-key-123'}
        self.widget = geckopush.GeckoMeter(
            dashboard=d,
            widget_key=widget_key,
            item=26,
            min_value=0,
            max_value=50
        )

class TestHighchart(unittest.TestCase, Base):
    def setUp(self):
        self.payload = {'data': {'highchart': '{chart:{style: {color: "#b9bbbb"},renderTo:"container",backgroundColor:"transparent",lineColor:"rgba(35,37,38,100)",plotShadow: false,},credits:{enabled:false},title:{style: {color: "#b9bbbb"},text:"Monthly Average Temperature"},xAxis:{categories:["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]},yAxis:{title:{style: {color: "#b9bbbb"}, text:"Temperature"}},legend:{itemStyle: {color: "#b9bbbb"}, layout:"vertical",align:"right",verticalAlign:"middle",borderWidth:0},series:[{color:"#108ec5",name:"NewYork",data:[17.0,22.0,24.8,24.1,20.1,14.1,8.6,2.5]},{color:"#52b238",name:"Berlin",data:[13.5,17.0,18.6,17.9,14.3,9.0,3.9,1.0]},{color:"#ee5728",name:"London",data:[11.9,15.2,17.0,16.6,14.2,10.3,6.6,4.8]}]}'}, 'api_key': 'api-key-123'}
        highchart_str = "{chart:{style: {color: \"#b9bbbb\"},renderTo:\"container\",backgroundColor:\"transparent\",lineColor:\"rgba(35,37,38,100)\",plotShadow: false,},credits:{enabled:false},title:{style: {color: \"#b9bbbb\"},text:\"Monthly Average Temperature\"},xAxis:{categories:[\"Jan\",\"Feb\",\"Mar\",\"Apr\",\"May\",\"Jun\",\"Jul\",\"Aug\",\"Sep\",\"Oct\",\"Nov\",\"Dec\"]},yAxis:{title:{style: {color: \"#b9bbbb\"}, text:\"Temperature\"}},legend:{itemStyle: {color: \"#b9bbbb\"}, layout:\"vertical\",align:\"right\",verticalAlign:\"middle\",borderWidth:0},series:[{color:\"#108ec5\",name:\"NewYork\",data:[17.0,22.0,24.8,24.1,20.1,14.1,8.6,2.5]},{color:\"#52b238\",name:\"Berlin\",data:[13.5,17.0,18.6,17.9,14.3,9.0,3.9,1.0]},{color:\"#ee5728\",name:\"London\",data:[11.9,15.2,17.0,16.6,14.2,10.3,6.6,4.8]}]}"
        self.widget = geckopush.HighCharts(dashboard=d,
                         widget_key=widget_key,
                         highchart=highchart_str)


class TestLeaderBoard(unittest.TestCase, Base):
    def setUp(self):
        self.payload = {'data': {'items': [{'previous_rank': 200, 'value': 100, 'label': 'Jack'}, {'previous_rank': 50, 'value': 50, 'label': 'Bob'}, {'previous_rank': 20, 'value': 100, 'label': 'Renaldo'}, {'previous_rank': 0, 'value': 0, 'label': 'Barney'}, {'previous_rank': 4, 'value': 96, 'label': 'Farnsworth'}]}, 'api_key': 'api-key-123'}
        self.widget = geckopush.Leaderboard(dashboard=d, widget_key=widget_key)
        self.widget.add_data("Jack", 100, 200)
        self.widget.add_data("Bob", 50, 50)
        self.widget.add_data("Renaldo", 100, 20)
        self.widget.add_data("Barney", 0, 0)
        self.widget.add_data("Farnsworth", 96, 4)


class TestLineChart(unittest.TestCase, Base):
    def setUp(self):
        self.payload = {'data': {'x_axis': {'type': 'datetime', 'labels': ['2015-10-01', '2015-10-02', '2015-10-03', '2015-10-04', '2015-10-06']}, 'series': [{'data': [400, 500, 900, 900, 1000], 'name': 'One'}, {'data': [1000, 900, 800, 200, 100], 'name': 'Two'}], 'y_axis': {'format': 'currency', 'unit': 'USD'}}, 'api_key': 'api-key-123'}
        self.widget = geckopush.LineChart(dashboard=d,
                             widget_key=widget_key)
        self.widget.add_data(name="One", data=[400, 500, 900, 900, 1000])
        self.widget.add_data(name="Two", data=[1000, 900, 800, 200, 100])
        self.widget.add(x_axis_labels=["2015-10-01", "2015-10-02", "2015-10-03", "2015-10-04", "2015-10-06"])
        self.widget.add(x_axis_type="datetime")
        self.widget.add(y_axis_format="currency")
        self.widget.add(y_axis_unit="USD")


class TestList(unittest.TestCase, Base):
    def setUp(self):
        self.payload = {'data': [{'title': {'text': '12345'}, 'description': 'These are numbers', 'label': {'color': '#ff2015', 'name': 'numbers'}}, {'title': {'text': 'abcde'}, 'description': 'These are letters', 'label': {'color': '#ffffff', 'name': 'letters'}}], 'api_key': 'api-key-123'}
        self.widget = geckopush.List(dashboard=d,
                        widget_key=widget_key)
        self.widget.add_data(text="12345", name="numbers",
                    color="#ff2015", description="These are numbers")
        self.widget.add_data(text="abcde", name="letters", color= "#ffffff", description="These are letters")


class TestMap(unittest.TestCase, Base):
    def setUp(self):
        self.payload = {'data': {'points': {'point': [{'city': {'country_code': 'US', 'city_name': 'New York'}, 'size': '10'}, {'host': 'google.com'}, {'ip': '46.228.47.115'}, {'latitude': 22.434355, 'longitude': 11.12345, 'color': '#ffffff', 'size': 5}]}}, 'api_key': 'api-key-123'}
        self.widget = geckopush.Map(dashboard=d, widget_key=widget_key)
        self.widget.add_data(city_name="New York", country_code="US", size="10")
        self.widget.add_data(host="google.com")
        self.widget.add_data(ip="46.228.47.115")
        self.widget.add_data(latitude=22.434355, longitude=11.12345, size=5, color="#ffffff")


class TestMonitoring(unittest.TestCase, Base):
    def setUp(self):
        self.payload = {'data': {'responseTime': '123 ms', 'status': 'up', 'downTime': 'Never'}, 'api_key': 'api-key-123'}
        self.widget = geckopush.Monitoring(dashboard=d, widget_key=widget_key)
        self.widget.add_data(status="up", downtime="Never", responsetime= "123 ms")


class TestPieChart(unittest.TestCase, Base):
    def setUp(self):
        self.payload = {'data': {'item': [{'color': '13699c', 'value': 100, 'label': 'Slice 1'}, {'color': '198acd', 'value': 200, 'label': 'Slice 2'}]}, 'api_key': 'api-key-123'}
        self.widget = geckopush.PieChart(dashboard=d, widget_key=widget_key)
        self.widget.add_data(100, "Slice 1", "13699c")
        self.widget.add_data(200, "Slice 2", "198acd")


class TestNumberAndSecondary1(unittest.TestCase, Base):
    def setUp(self):
        self.payload = {'data': {'item': [{'value': 15}, {'value': 25}]}, 'api_key': 'api-key-123'}

        self.widget = geckopush.NumberAndSecondaryStat(dashboard=d, widget_key=widget_key)
        self.widget.add_data(primary_value=15, secondary_value=25)


class TestNumberAndSecondary2(unittest.TestCase, Base):
    def setUp(self):
        self.payload = {'data': {'item': [{'text': 'Hola Amigo', 'value': 15}]}, 'api_key': 'api-key-123'}
        self.widget = geckopush.NumberAndSecondaryStat(dashboard=d, widget_key=widget_key)
        self.widget.add_data(primary_value=15, text="Hola Amigo")


class TestNumberAndSecondary3(unittest.TestCase, Base):
    def setUp(self):
        self.payload = {'data': {'item': [{'value': 15}, [12345, 12345, 15555, 12345, 12322]]}, 'api_key': 'api-key-123'}
        self.widget = geckopush.NumberAndSecondaryStat(dashboard=d, widget_key=widget_key)
        self.widget.add_data(primary_value=15, secondary_value=[12345, 12345, 15555, 12345, 12322])


class TestRAG(unittest.TestCase, Base):
    def setUp(self):
        self.payload = {'data': {'item': [{'prefix': '$', 'value': 150, 'text': 'Three'}, {'prefix': '$', 'value': 100, 'text': 'Two'}, {'prefix': '$', 'value': 50, 'text': 'One'}]}, 'api_key': 'api-key-123'}
        self.widget = geckopush.RAG(dashboard=d, widget_key=widget_key)
        self.widget.add_data(text="One", value=50, prefix="$", color="green")
        self.widget.add_data(text="Two", value=100, prefix="$", color="amber")
        self.widget.add_data(text="Three", value=150, prefix="$", color="red")

class TestText(unittest.TestCase, Base):
    def setUp(self):
        self.payload = {'data': {'item': [{'text': 'Hello There My Friend', 'type': None}, {'text': 'How are you doing?', 'type': None}]}, 'api_key': 'api-key-123'}
        self.widget = geckopush.Text(dashboard=d, widget_key=widget_key)
        self.widget.add_data(text="Hello There My Friend", type=0)
        self.widget.add_data(text="How are you doing?", type=1)

if __name__ == '__main__':
    unittest.main()