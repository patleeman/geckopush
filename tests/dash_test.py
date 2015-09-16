from geckopush import geckopush

api_key = input("Please enter an API key: ")
dashboard = geckopush.Dashboard(api_key)

test_data = [1.0, 2.0, 3.0, 2.0, 1.0]
x_axis_label = ["one", "two", "three", "four", "five"]

widget_key = input("Please enter a widget key: ")
bar_chart = geckopush.BarChart(widget_key=widget_key, data=test_data, dashboard=dashboard, x_axis_label=x_axis_label)
bar_chart.push()

