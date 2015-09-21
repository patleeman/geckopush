#Geckopush v 0.1.0-dev
###Easy to use python library for pushing data your custom Geckoboard widgets
The goal behind this library is to make pushing data to your Geckoboard widgets quick and painless.

[Geckoboard API Docs](https://developer.geckoboard.com/)

Install:
    Todo: package for pypi
    

Quickstart:

```python
from Geckopush import geckopush

# Initialize your dashboard by creating a dashboard object
api_key = '<api key from geckoboard>'
d = geckopush.Dashboard(api_key)

# Wrangle up your data from your custom source.
data = [1, 2, 3, 4, 5]

# Grab your widget key for your custom widget
widget_key = '<widget key from geckoboard bar chart custom widget>'

# Create your bar chart widget and specify what dashboard you'd like to use
bar_chart = geckopush.BarChart(dashboard=d, widget_key=widget_key)

# Add your data
bar_chart.add_data(data)

# Add additional data if desired.  Additional fields correspond to optional
# fields in the Geckoboard documentation.
bar.x_axis_labels = ["one", "two", "three"]
bar.x_axis_type = "standard"
bar.y_axis_format = "decimal"

# Push the data to the dashboard
bar.push()
```

That's it, you've push some data to your geckoboard widget!


*Note: you can declare your data while initializing your widget or afterwards using the .add_data method.*

    bar_chart = geckopush.BarChart(dashboard=d, widget_key=widget_key, data=[1,2,3,4,5]

    or

    bar_chart = geckopush.BarChart(dashboard=d, widget_key=widget_key)
    bar_chart.add_data([1,2,3,4,5])


If you want to initialize multiple widgets, then send data to them all at once:
```python
from Geckopush import geckopush

api_key = '<api key from geckoboard>'
d = geckopush.Dashboard(api_key)

# Initialize your widgets
# Widget 1
data = [1, 2, 3, 4, 5]
widget_key = '<widget key from geckoboard bar chart custom widget>'
bar_chart = geckopush.BarChart(dashboard=d, widget_key=widget_key, data=data)
bar.x_axis_labels = ["one", "two", "three"]
bar.x_axis_type = "standard"
bar.y_axis_format = "decimal"

# Widget 2
bullet_widget_key = "<widget key from geckoboard bullet graph custom widget>"
bullet = geckopush.BulletGraph(dashboard=d,
                               widget_key=bullet_widget_key)

bullet.add_data(
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
            projected_end='900'
            )

# Then push to all your widgets at once
d.push_all()
```

It's **that** easy!

Notes:

* Each widget must specify which dashboard object you're using.

    ```python
    dash = geckopush.Dashboard('API-KEY')
    custom_widget = geckopush.<widget>(dashboard=dash, ...)
    ```
