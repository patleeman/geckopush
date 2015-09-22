"""
This very basic test suite is a very quick and dirty way to test to see if all the widgets are working.
This requires a file named geckoboard_push_settings with widget API keys located in the parent directory
that geckopush shares.
"""

from Geckopush import geckopush
from tests import pull_keys


WIDGET_KEYS = pull_keys.get_keys()
API_KEY = WIDGET_KEYS['api_key']
d = geckopush.Dashboard(API_KEY)


def test_bar_chart():
    bar_widget_key = WIDGET_KEYS['bar_widget_key']
    bar = geckopush.BarChart(dashboard=d, widget_key=bar_widget_key, data=[1,2,3,4,5,6,7,8,9,10])
    bar.x_axis_labels = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]
    bar.x_axis_type = "standard"
    bar.y_axis_format = "decimal"
    bar.y_axis_unit = "USD"
    ret = bar.push()
    if ret:
        return True
    else:
        return False


def test_bullet_graph():
    bullet_widget_key = WIDGET_KEYS['bullet_widget_key']
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

    ret = bullet.push()
    if ret:
        return True
    else:
        return False


def test_funnel():
    funnel_widget_key = WIDGET_KEYS['funnel_widget_key']
    fun = geckopush.Funnel(dashboard=d, widget_key=funnel_widget_key)
    fun.add_data(100, "one hundred")
    fun.add_data(200, "two hundred")
    fun.add_data(300, "three hundred")
    fun.add_data(400, "four hundred")
    fun.add_data(500, "five hundred")
    fun.add_data(600, "six hundred")
    fun.add_data(700, "seven hundred")
    fun.add_data(800, "eight hundred")

    ret = fun.push()
    if ret:
        return True
    else:
        return False


def test_geckometer():
    geckometer_widget_key = WIDGET_KEYS['geckometer_widget_key']
    gm = geckopush.GeckoMeter(dashboard=d, widget_key=geckometer_widget_key,
                              item=26, min_value=0, max_value=50)
    ret = gm.push()
    if ret:
        return True
    else:
        return False


def test_highchart():
    highchart_widget_key = WIDGET_KEYS["highchart_widget_key"]
    highchart_str = "{chart:{style: {color: \"#b9bbbb\"},renderTo:\"container\",backgroundColor:\"transparent\",lineColor:\"rgba(35,37,38,100)\",plotShadow: false,},credits:{enabled:false},title:{style: {color: \"#b9bbbb\"},text:\"Monthly Average Temperature\"},xAxis:{categories:[\"Jan\",\"Feb\",\"Mar\",\"Apr\",\"May\",\"Jun\",\"Jul\",\"Aug\",\"Sep\",\"Oct\",\"Nov\",\"Dec\"]},yAxis:{title:{style: {color: \"#b9bbbb\"}, text:\"Temperature\"}},legend:{itemStyle: {color: \"#b9bbbb\"}, layout:\"vertical\",align:\"right\",verticalAlign:\"middle\",borderWidth:0},series:[{color:\"#108ec5\",name:\"NewYork\",data:[17.0,22.0,24.8,24.1,20.1,14.1,8.6,2.5]},{color:\"#52b238\",name:\"Berlin\",data:[13.5,17.0,18.6,17.9,14.3,9.0,3.9,1.0]},{color:\"#ee5728\",name:\"London\",data:[11.9,15.2,17.0,16.6,14.2,10.3,6.6,4.8]}]}"
    hc = geckopush.HighCharts(dashboard=d,
                         widget_key=highchart_widget_key,
                         highchart=highchart_str)

    ret = hc.push()
    if ret:
        return True
    else:
        return False


def test_leaderboard():
    leaderboard_widget_key = WIDGET_KEYS["leaderboard_widget_key"]
    lb = geckopush.Leaderboard(dashboard=d,
                               widget_key=leaderboard_widget_key)
    lb.add_data("Jack", 100, 200)
    lb.add_data("Bob", 50, 50)
    lb.add_data("Renaldo", 100, 20)
    lb.add_data("Barney", 0, 0)
    lb.add_data("Farnsworth", 96, 4)
    ret = lb.push()
    if ret:
        return True
    else:
        return False


def test_line_chart_datetime():
    linechart_widget_key = WIDGET_KEYS["linechart_widget_key"]
    lc = geckopush.LineChart(dashboard=d,
                             widget_key=linechart_widget_key)
    lc.add_data(name="One", data=[400, 500, 900, 900, 1000])
    lc.add_data(name="Two", data=[1000, 900, 800, 200, 100])
    lc.add(x_axis_labels=["2015-10-01", "2015-10-02", "2015-10-03", "2015-10-04", "2015-10-06"])
    lc.add(x_axis_type="datetime")
    lc.add(y_axis_format="currency")
    lc.add(y_axis_unit="USD")
    ret = lc.push()
    if ret:
        return True
    else:
        return False


def test_List():
    lst_widget_key = WIDGET_KEYS["list_widget_key"]
    lt = geckopush.List(dashboard=d,
                        widget_key=lst_widget_key)
    lt.add_data(text="12345", name="numbers",
                color="#ff2015", description="These are numbers")

    lt.add_data(text="abcde", name="letters", color= "#ffffff", description="These are letters")
    ret = lt.push()
    if ret:
        return True
    else:
        return False

def test_map():
    map_widget_key = WIDGET_KEYS["map_widget_key"]
    mp = geckopush.Map(dashboard=d, widget_key=map_widget_key)
    mp.add_data(city_name="New York", country_code="US", size="10")
    mp.add_data(host="google.com")
    mp.add_data(ip="46.228.47.115")
    mp.add_data(latitude=22.434355, longitude=11.12345, size=5, color="#ffffff")
    ret = mp.push()
    if ret:
        return True
    else:
        return False

def test_monitoring():
    monitoring_widget_key = WIDGET_KEYS["monitoring_widget_key"]
    mo = geckopush.Monitoring(dashboard=d, widget_key=monitoring_widget_key)
    mo.add_data(status="up", downtime="Never", responsetime= "123 ms")
    ret = mo.push()
    if ret:
        return True
    else:
        return False

def test_pie_chart():
    piechart_widget_key = WIDGET_KEYS["pie_chart_widget_key"]
    pi = geckopush.PieChart(dashboard=d, widget_key=piechart_widget_key)
    pi.add_data(100, "Slice 1", "13699c")
    pi.add_data(200, "Slice 2", "198acd")
    ret = pi.push()
    if ret:
        return True
    else:
        return False

def test_number_and_secondary_stat_1():
    widget_key = WIDGET_KEYS["number_and_secondary_stat_widget_key_1"]
    ns = geckopush.NumberAndSecondaryStat(dashboard=d, widget_key=widget_key)
    ns.add_data(primary_value=15, secondary_value=25)
    ret = ns.push()
    if ret:
        return True
    else:
        return False

def test_number_and_secondary_stat_2():
    widget_key = WIDGET_KEYS["number_and_secondary_stat_widget_key_2"]
    ns = geckopush.NumberAndSecondaryStat(dashboard=d, widget_key=widget_key)
    ns.add_data(primary_value=15, text="Hola Amigo")
    ret = ns.push()
    if ret:
        return True
    else:
        return False

def test_rag_numbers():
    widget_key = WIDGET_KEYS["RAG_numbers_widget_key"]
    rg = geckopush.RAG(dashboard=d, widget_key=widget_key)
    rg.add_data(text="One", value=50, prefix="$", color="green")
    rg.add_data(text="Two", value=100, prefix="$", color="amber")
    rg.add_data(text="Three", value=150, prefix="$", color="red")
    ret = rg.push()
    if ret:
        return True
    else:
        return False

def test_rag_columns():
    widget_key = WIDGET_KEYS["RAG_columns_widget_key"]
    rg = geckopush.RAG(dashboard=d, widget_key=widget_key)
    rg.add_data(text="One", value=50, prefix="$", color="green")
    rg.add_data(text="Two", value=100, prefix="$", color="amber")
    rg.add_data(text="Three", value=150, prefix="$", color="red")
    ret = rg.push()
    if ret:
        return True
    else:
        return False

def test_text():
    widget_key = WIDGET_KEYS["text_widget_key"]
    rg = geckopush.Text(dashboard=d, widget_key=widget_key)
    rg.add_data(text="Hello There My Friend", type=0)
    rg.add_data(text="How are you doing?", type=1)
    ret = rg.push()
    if ret:
        return True
    else:
        return False

if __name__ == '__main__':
    tests = [
        test_bar_chart,
        test_funnel,
        test_bullet_graph,
        test_geckometer,
        test_highchart,
        test_leaderboard,
        test_line_chart_datetime,
        test_List,
        test_map,
        test_monitoring,
        test_pie_chart,
        test_number_and_secondary_stat_1,
        test_number_and_secondary_stat_2,
        test_rag_numbers,
        test_rag_columns,
        test_text
        ]

    successful = []
    failed = []
    for i, test in enumerate(tests):
        result = test()
        if result:
            successful.append(test)
            print("{} test successful".format(test.__name__))
        else:
            failed.append(test)
            print("{} test failed".format(test.__name__))

    print("")
    if len(failed) > 0:
        print("{}/{} tests failed".format(len(failed),len(tests)))
    else:
        print("ALL TESTS SUCCESSFUL")


