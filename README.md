#Geckopush v 0.2.0-dev
###Easy to use python library for pushing data your custom Geckoboard widgets.
Geckopush makes pushing data to your Geckoboard.com custom widgets painless.  It handles structuring your widgets' JSON, request, and subsequent push to Geckoboard's servers.  It takes the difficult work out of getting your custom data to your dashboard.

For Geckoboard specific custom widget information, please refer to the developer docs.
[Geckoboard API Docs](https://developer.geckoboard.com/)

##Installation:

For now, Git Clone the repo to your local machine.

    git clone https://github.com/patleeman/geckopush.git
    
*Coming soon: Pypi package.*


##Quickstart:

```python
from Geckopush import geckopush

# Initialize your dashboard by creating a dashboard object and assigning it to a variable.  You must provide the api_key parameter.
>>> api_key = '<api key from geckoboard>'
>>> d = geckopush.Dashboard(api_key)

# Wrangle up your data from your custom source.  Please see below for specifics of the data types that each widget accepts.
>>> data = [1, 2, 3, 4, 5]

# Grab the widget key for your custom widget from geckoboard.
>>> widget_key = '<widget key from geckoboard bar chart custom widget>'

# Create your bar chart widget and specify which dashboard object it is in and the widget key.
>>> bar_chart = geckopush.BarChart(dashboard=d, widget_key=widget_key)

# Add data.  Must be called once for each set of data and all data must be complete.  This means you can't add one parameter then call .add_data again to add a separate parameter on the next line.
>>> bar_chart.add_data(data)

# Add widget parameters (usually optional).  Additional fields correspond to optional fields in the Geckoboard documentation.
>>> bar.x_axis_labels = ["one", "two", "three"]
>>> bar.x_axis_type = "standard"
>>> bar.y_axis_format = "decimal"

# Push the data to the dashboard
>>> bar.push()
```

That's it, you've push some data to your geckoboard widget!


*Note: you can declare your data while initializing your widget or afterwards using the .add_data method.*

    >>> bar_chart = geckopush.BarChart(dashboard=d, widget_key=widget_key, data=[1,2,3,4,5]

    or

    >>> bar_chart = geckopush.BarChart(dashboard=d, widget_key=widget_key)
    >>> bar_chart.add_data([1,2,3,4,5])


Geckopush also has a convient push_all function within the Dashboard class (Dashboard.push_all()) allows you to first initialize all your widgets, add data, then with a single command push data to your widgets.:

```python
>>> from Geckopush import geckopush

>>> api_key = '<api key from geckoboard>'
>>> d = geckopush.Dashboard(api_key)

# Initialize your widgets but do not call the push() method yet.
# Widget 1
>>> data = [1, 2, 3, 4, 5]
>>> widget_key = '<widget key from geckoboard bar chart custom widget>'
>>> bar_chart = geckopush.BarChart(dashboard=d, widget_key=widget_key, data=data)
>>> bar.x_axis_labels = ["one", "two", "three"]
>>> bar.x_axis_type = "standard"
>>> bar.y_axis_format = "decimal"

# Widget 2
>>> bullet_widget_key = "<widget key from geckoboard bullet graph custom widget>"
>>> bullet = geckopush.BulletGraph(dashboard=d,
                               widget_key=bullet_widget_key)

>>> bullet.add_data(
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

# Then push to all your widgets at once as a method of the dashboard.
>>> d.push_all()
```

It's **that** easy!

Notes:

* You must supply an API key for each dashboard.  This is your account API key located in your Geckoboard settings.
* Each widget requires you to specify the dashboard and widget_key.

    ```python
    >>> dash = geckopush.Dashboard('API-KEY')
    >>> custom_widget = geckopush.<widget>(dashboard=dash, ...)
    ```

#Geckopush Structure
### Geckopush is structured in three layers:

* Dashboard layer: You interface with Geckopush by creating a Dashboard object first with the required parameters.  This object contains your account's API key, which can be found under your account details -> API Key.
    
    ```python
    >>> from Geckopush import geckopush
    >>> d = geckopush.Dashboard(api_key="API-Key-Goes-Here")
    ```

* Widget layer: This layer contains your custom widgets' data including which dashboard it belongs to and its widget key.  This object holds the relevant data points and methods to construct and POST your JSON payload.
    
    ```python
    >>> widget = geckopush.Text(dashboard=d, widget_key="Widget-Key-Goes-Here")
    ```
    
* Data layer: This is the data payload that you push to Geckoboard's servers.  This contains the JSON payload in a specific structure as laid out in the Geckoboard API Docs.  Each widget has a slightly different payload scheme and must be configured very specifically in order to successfully complete your POST request.

    ```python
    # Adding a parameter to your widget (note: the text widget does not contain any parameters, calling .add will raise an exception on this widget.)
    >>> widget.add(param="example")
    
    # Adding a data point to your widget
    >>> widget.add_data(text="This is a message to display on your widget", text_type=2)
    ```

The data layer is split into two types of data:
* widget attributes (added to your widget with the .add() method)
* data points (added to your widget with the .add_data() method)

This distinction affects how one accesses Geckopush's interface.  For widget attributes, you can usually call an attribute after setting it with .add.  
To retrieve the valuse, call 

    >>> widget.attribute_name
    ex:
    >>> 

To call data points, if a widget contains more than a single data point, you can call widget.data which will return a list with the formatted data points already initialized.


# Widget Types and Parameters

### Bar Chart
Parameter Name | Optional | Data Type | Notes | Instance Variable Name
:---------------|:----------|:-----------|:--------|:----------------------
data | no | list | list must contain integers | self.data
x_axis_labels | yes | list | list must contain strings | self.x_axis_labels
x_axis_type | yes | string | see Geckoboard API docs for parameters | self.x_axis_type
y_axis_format | yes | string | see Geckoboard API docs for parameters | self.y_axis_format
y_axis_unit | yes | string | see Geckoboard API docs for parameters | self.y_axis_unit

Instance Methods | Accepts Parameters | Notes
:--------------- | :----------------- | :-----
self.add_data() | data |
self.add() | x_axis_labels, x_axis_type, y_axis_format, y_axis_unit | 
self.push() | |


### Bullet Graph


### Funnel


### Geck-o-meter


### Highcharts


### Leaderboard


### Line Chart


### List


### Map


### Monitoring



### Number and Secondary Stat



### Pie Chart



### RAG



### Text
