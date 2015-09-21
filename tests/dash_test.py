import pprint
import json

from Geckopush import geckopush
from tests import pull_keys


widget_keys = pull_keys.get_keys()

api_key = widget_keys['api_key']
d = geckopush.Dashboard(api_key)

def test_bar_chart():
    bar_widget_key = widget_keys['bar_widget_key']
    bar = geckopush.BarChart(dashboard=d, widget_key=bar_widget_key, data=[1,2,3])
    bar.x_axis_labels = ["one", "two", "three"]
    bar.x_axis_type = "standard"
    bar.y_axis_format = "decimal"
    bar.push()
    print(bar.payload)

def test_bullet_graph():
    bullet_widget_key = widget_keys['bullet_widget_key']
    bullet = geckopush.BulletGraph(dashboard=d, widget_key=bullet_widget_key,)

    bullet = geckopush.BulletGraph(dashboard=d,
                                   widget_key=bullet_widget_key,
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
    bullet.add_data(
       label='Second Bullet Graph',
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
    print(bullet.data)
    print(bullet.payload)
    bullet.push()

def test_funnel():
    funnel_widget_key = widget_keys['funnel_widget_key']
    fun = geckopush.Funnel(dashboard=d, widget_key=funnel_widget_key)
    fun.add_data(100, "Prepare romantic dinner")
    fun.add_data(200, "Wrap present")
    fun.add_data(300, "Cut a hole in the box")
    fun.add_data(400, "Put your junk in the box")
    fun.add_data(500, "Make her open the box")
    fun.add_data(600, "That's the way you do it")
    fun.add_data(700, "That's my dk in a box")
    fun.add_data(800, "dk in a box, yeah.")

    fun.push()


def test_geckometer():
    geckometer_widget_key = widget_keys['geckometer_widget_key']
    gm = geckopush.GeckoMeter(dashboard=d, widget_key=geckometer_widget_key,
                              item=26, min_value=0, max_value=50)
    gm.push()


def test_highchart():
    highchart_widget_key = widget_keys["highchart_widget_key"]
    highchart_str = "{chart:{style: {color: \"#b9bbbb\"},renderTo:\"container\",backgroundColor:\"transparent\",lineColor:\"rgba(35,37,38,100)\",plotShadow: false,},credits:{enabled:false},title:{style: {color: \"#b9bbbb\"},text:\"Monthly Average Temperature\"},xAxis:{categories:[\"Jan\",\"Feb\",\"Mar\",\"Apr\",\"May\",\"Jun\",\"Jul\",\"Aug\",\"Sep\",\"Oct\",\"Nov\",\"Dec\"]},yAxis:{title:{style: {color: \"#b9bbbb\"}, text:\"Temperature\"}},legend:{itemStyle: {color: \"#b9bbbb\"}, layout:\"vertical\",align:\"right\",verticalAlign:\"middle\",borderWidth:0},series:[{color:\"#108ec5\",name:\"NewYork\",data:[17.0,22.0,24.8,24.1,20.1,14.1,8.6,2.5]},{color:\"#52b238\",name:\"Berlin\",data:[13.5,17.0,18.6,17.9,14.3,9.0,3.9,1.0]},{color:\"#ee5728\",name:\"London\",data:[11.9,15.2,17.0,16.6,14.2,10.3,6.6,4.8]}]}"
    hc = geckopush.HighCharts(dashboard=d,
                         widget_key=highchart_widget_key,
                         highchart=highchart_str)

    hc.push()

def test_leaderboard():
    leaderboard_widget_key = widget_keys["leaderboard_widget_key"]
    lb = geckopush.Leaderboard(dashboard=d,
                               widget_key=leaderboard_widget_key)
    lb.add_data("Jack", 1, 0)
    lb.add_data("Bob", 2, 1)
    lb.add_data("Renaldo", 10, 6)
    lb.add_data("Barney", 0, 0)
    lb.add_data("Farnsworth", 1, 1)
    lb.push()


def test_line_chart():
    linechart_widget_key = widget_keys["linechart_widget_key"]
    lc = geckopush.LineChart(dashboard=d,
                             widget_key=linechart_widget_key)
    lc.add_data(data=[[1,2],[2,3],[3,5]], name="BonerJamz")
    lc.add_data(data=[[2,2], [3,4], [4,5]], name="Smooth")

    lc.push()
    pprint.pprint(lc.payload)

def test_line_chart_list():
    linechart_widget_key = widget_keys["linechart_widget_key"]
    lc = geckopush.LineChart(dashboard=d,
                             widget_key=linechart_widget_key)
    lc.add_data(data=[1,2,3,4,5], name="womp")
    lc.add_data(data=[2,5,5,1,1], name="omp")
    lc.add(x_axis_labels=['one', 'two', 'three', 'four', 'five'])
    lc.push()
    pprint.pprint(lc.payload)


def test_line_chart_datetime():
    linechart_widget_key = widget_keys["linechart_widget_key"]
    lc = geckopush.LineChart(dashboard=d,
                             widget_key=linechart_widget_key)
    lc.add_data(name="data over time", data=[['2015-09-07', 400], ['2015-09-02', 500]], series_type="secondary")
    lc.add(x_axis_type="datetime")
    #lc.add(y_axis_format="currency")
    #lc.add(y_axis_unit="EUR")
    lc.push()
    pprint.pprint(lc.payload)

def test_line_chart_datetime2():
    linechart_widget_key = widget_keys["linechart_widget_key"]
    lc = geckopush.LineChart(dashboard=d,
                             widget_key=linechart_widget_key)
    lc.add_data(name="data over time", data=[400, 500, 900, 900, 1000])
    lc.add_data(name="boners over time", data=[1000,900,800,200,100])
    lc.add(x_axis_labels=["2015-10-01", "2015-10-02", "2015-10-03", "2015-10-04", "2015-10-06"])
    lc.add(x_axis_type="datetime")
    lc.add(y_axis_format="currency")
    lc.add(y_axis_unit="USD")
    lc.push()
    pprint.pprint(lc.payload)


def test_List():
    lst_widget_key = widget_keys["list_widget_key"]
    lt = geckopush.List(dashboard=d,
                        widget_key=lst_widget_key)
    lt.add_data(text="stuff", name="HOT",
                color="#ff2015", description="Something describes here")

    lt.push()
    print(lt.payload)


def test_map():
    map_widget_key = widget_keys["map_widget_key"]
    mp = geckopush.Map(dashboard=d, widget_key=map_widget_key)
    mp.add_data(city_name="New York", country_code="US", size="10")
    mp.add_data(host="google.com")
    mp.add_data(ip="46.228.47.115")
    mp.add_data(latitude=22.434355, longitude=11.12345, size=5, color="#ffffff")
    mp.push()

def test_monitoring():
    monitoring_widget_key = widget_keys["monitoring_widget_key"]
    mo = geckopush.Monitoring(dashboard=d, widget_key=monitoring_widget_key)
    mo.add_data(status="up", downtime="Never", responsetime= "123 ms")
    mo.push()
    print(mo.status)
    print(mo.payload)

def pie_chart():
    piechart_widget_key = widget_keys["piechart_widget_key"]
    pi = geckopush.PieChart(dashboard=d, widget_key=piechart_widget_key)
    pi.add_data(100, "stuff", "13699c")
    pi.add_data(200, "boring", "198acd")


if __name__ == '__main__':
    #test_bar_chart()
    #test_funnel()
    #test_bullet_graph()
    #test_geckometer()
    #test_highchart()
    #test_leaderboard()
    #test_line_chart()
    #test_line_chart_list()
    test_line_chart_datetime()
    #test_line_chart_datetime2()
    #test_List()
    #test_map()
    #test_monitoring()