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
    bullet = geckopush.BulletGraph(dashboard=d,
                                   widget_key=bullet_widget_key,
                                   orientation='vertical',
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
    bullet.add(
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
    bullet.push()
    pprint.pprint(bullet.payload)

def test_funnel():
    funnel_widget_key = widget_keys['funnel_widget_key']
    fun = geckopush.Funnel(dashboard=d, widget_key=funnel_widget_key)
    fun.add(100, "Prepare romantic dinner")
    fun.add(200, "Wrap present")
    fun.add(300, "Cut a hole in the box")
    fun.add(400, "Put your junk in the box")
    fun.add(500, "Make her open the box")
    fun.add(600, "That's the way you do it")
    fun.add(700, "That's my dk in a box")
    fun.add(800, "dk in a box, yeah.")

    fun.push()
    pprint.pprint(fun.payload)


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
    lb.add("Jack", 1, 0)
    lb.add("Bob", 2, 1)
    lb.add("Renaldo", 10, 6)
    lb.add("Barney", 0, 0)
    lb.add("Farnsworth", 1, 1)
    lb.push()
    print(lb.payload)

if __name__ == '__main__':
    #test_funnel()
    #test_highchart()
    test_leaderboard()
