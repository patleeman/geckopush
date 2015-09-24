#Geckopush v 0.2.0-dev
###Easy to use python library for pushing data your custom Geckoboard widgets.
Geckopush makes pushing data to your Geckoboard.com custom widgets painless.  It handles structuring your widgets' JSON, request, and subsequent push to Geckoboard's servers.  It takes the difficult work out of getting your custom data to your dashboard.


For Geckoboard specific custom widget information, please refer to the developer docs.
###[Geckoboard API Docs](https://developer.geckoboard.com/)

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


*Note: you can declare your first set of data while initializing your widget or afterwards using the .add_data method.*

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
    >>> widget = geckopush.LineChart(dashboard=d, widget_key="Widget-Key-Goes-Here")
    ```
    
* Data layer: This is the data payload that you push to Geckoboard's servers.  This contains the JSON payload in a specific structure as laid out in the Geckoboard API Docs.  Each widget has a slightly different payload scheme and must be configured very specifically in order to successfully complete your POST request.

    ```python
    # Adding a parameter to your widget (note: the text widget does not contain any parameters, calling .add will raise an exception on this widget.)
    >>> lc.add(x_axis_type="datetime")
    >>> lc.add(y_axis_format="currency")
    >>> lc.add(y_axis_unit="USD")
    
    # Adding a data point to your widget
    >>> lc.add_data(name="One", data=[400, 500, 900, 900, 1000])
    >>> lc.add_data(name="Two", data=[1000, 900, 800, 200, 100])
    ```

The data layer is split into two types of data:
* widget attributes (added to your widget with the .add() method)
* data points (added to your widget with the .add_data() method)

This distinction affects how one accesses Geckopush's interface.  For widget attributes, you can usually call an attribute after setting it with .add.  
To retrieve the values, call 

    >>> widget.attribute_name
    ex: 
    >>> lc.x_axis_type
    "datetime"

To call data points, if a widget contains more than a single data point, you can call widget.data which will return a list with the formatted data points already initialized.


# Widget Types and Parameters
### Universal Instance Variables and Methods

All widgets inherit from a base Widget class which have methods and instance variables that are accessable from all widget subclasses.

Widget Class Variable/Methods | Notes
------------------------------|--------
self.dashboard | Stores the reference to the dashboard object
self.api_key | Stores the dashboard api_key
self.widget | Stores the widget key associated with the widget
self.get_payload() | Method which assembles the payload and returns it.  The payload is not assembled until either this method or push() is called.
self.push() | Method which assembles the payload, forms the POST request, and pushs the data to Geckoboard's servers.

If you wanted to see the structure of the final JSON after executing the .push() method, call self.payload.



### Bar Chart
Parameter Name | Optional | Data Type | Instance Variable Name | Notes
:---------------|:----------|:-----------|:--------|:----------------------
data | no | list | self.data |  list must contain integers 
x_axis_labels | yes | list | self.x_axis_labels | list must contain strings
x_axis_type | yes | string | self.x_axis_type | 
y_axis_format | yes | string |self.y_axis_format | 
y_axis_unit | yes | string | self.y_axis_unit | 

Instance Methods | Accepts Parameters | Notes
:--------------- | :----------------- | :-----
self.add_data() | data | variables stored in self.data
self.add() | x_axis_labels, x_axis_type, y_axis_format, y_axis_unit | 

######Example:

```python
bar = geckopush.BarChart(dashboard=d, widget_key=bar_widget_key, data=[1,2,3,4,5,6,7,8,9,10])
bar.x_axis_labels = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]
bar.x_axis_type = "standard"
bar.y_axis_format = "decimal"
bar.y_axis_unit = "USD"
bar.push()
```


### Bullet Graph
Parameter Name | Optional | Data Type | Instance Variable Name | Notes
:---------------|:----------|:-----------|:--------|:----------------------
orientation | yes | string | self.orientation |
label | no | string | | stored in self.data
axis | no | list | list must contain strings | 
red_start | no | integer | | stored in self.data
red_end | no | integer | | stored in self.data
amber_start | no | integer | | stored in self.data
amber_end | no | integer | | stored in self.data
green_start | no | integer | | stored in self.data
green_end | no | integer | | stored in self.data
measure_start | no | string | | stored in self.data
measure_end | no | string | | stored in self.data
projected_start | no | string | | stored in self.data
projected_end | no | string | | stored in self.data
comparative | no | string | | stored in self.data
sublabel | yes | string | | stored in self.data


Instance Methods | Accepts Parameters | Notes
:--------------- | :----------------- | :-----
self.add_data() | label, axis, red_start, red_end, amber_start,  amber_end, green_start, green_end, measure_start, measure_end, projected_start, projected_end, comparative, sublabel | 
self.add() | orientation | 

######Example:

```python
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
bullet.push()
```


### Funnel
Parameter Name | Optional | Data Type | Instance Variable Name | Notes
:---------------|:----------|:-----------|:--------|:----------------------
value | no | string | | stored in self.data
label | no | string | | stored in self.data
funnel_type | yes | string | self.funnel_type | 
percentage | yes | string | self.percentage |


Instance Methods | Accepts Parameters | Notes
:--------------- | :----------------- | :-----
self.add_data() | value, label | 

######Example:

```python
fun = geckopush.Funnel(dashboard=d, widget_key=funnel_widget_key)
fun.add_data(100, "one hundred")
fun.add_data(200, "two hundred")
fun.add_data(300, "three hundred")
fun.add_data(400, "four hundred")
fun.add_data(500, "five hundred")
fun.add_data(600, "six hundred")
fun.add_data(700, "seven hundred")
fun.add_data(800, "eight hundred")

fun.push()
```

### Geck-o-meter
Parameter Name | Optional | Data Type | Instance Variable Name | Notes
:---------------|:----------|:-----------|:--------|:----------------------
item | no | integer | self.item | 
min_value | no | integer | self.min_value |
max_value | no | integer | self.max_value | 

Instance Methods | Accepts Parameters | Notes
:--------------- | :----------------- | :-----
self.add_data() | item, min_value, max_value | 

######Example:

```python
gm = geckopush.GeckoMeter(dashboard=d, widget_key=geckometer_widget_key,
                          item=26, min_value=0, max_value=50)
gm.push()
```

### Highcharts
Parameter Name | Optional | Data Type | Instance Variable Name | Notes
:---------------|:----------|:-----------|:--------|:----------------------
highchart | no | string | self.highchart | highchart code must be within a string


Instance Methods | Accepts Parameters | Notes
:--------------- | :----------------- | :-----
self.add_data() | highchart | 

######Example:

```python
    highchart_str = "<HighCharts String>"
    hc = geckopush.HighCharts(dashboard=d,
                         widget_key=highchart_widget_key,
                         highchart=highchart_str)
    hc.push()
```


### Leaderboard
Parameter Name | Optional | Data Type | Instance Variable Name | Notes
:---------------|:----------|:-----------|:--------|:----------------------
label | no | string | | stored in self.data
value | yes | integer |  | stored in self.data
previous_rank | yes | string | | stored in self.data
number_format | yes | string | self.number_format |
unit | yes | string | self.unit |


Instance Methods | Accepts Parameters | Notes
:--------------- | :----------------- | :-----
self.add_data() | label, value, previous_rank | Widget accepts a max of 22 labels.

######Example:

```python
lb = geckopush.Leaderboard(dashboard=d, widget_key=leaderboard_widget_key)
lb.add_data("Jack", 100, 200)
lb.add_data("Bob", 50, 50)
lb.add_data("Renaldo", 100, 20)
lb.add_data("Barney", 0, 0)
lb.add_data("Farnsworth", 96, 4)
lb.push()
```

### Line Chart
Parameter Name | Optional | Data Type | Instance Variable Name | Notes
:---------------|:----------|:-----------|:--------|:----------------------
data | no | list | | stored in self.data
name | yes | string | | stored in self.data
incomplete_from | yes | string | | stored in self.data 
series_type | yes | string | | stored in self.data
x_axis_labels | yes | list | self.x_axis_labels | list must contain strings
x_axis_type | yes | string | self.x_axis_type | 
y_axis_format | yes | string | self.y_axis_format |
y_axis_unit | yes | string | self.y_axis_unit |

Instance Methods | Accepts Parameters | Notes
:--------------- | :----------------- | :-----
self.add_data() | data, name, incomplete_from, series_type | 
self.add() | x_axis_labels, x_axis_type, y_axis_format, y_axis_unit | 

######Example:

```python
lc = geckopush.LineChart(dashboard=d, widget_key=linechart_widget_key)
lc.add_data(name="One", data=[400, 500, 900, 900, 1000])
lc.add_data(name="Two", data=[1000, 900, 800, 200, 100])
lc.add(x_axis_labels=["2015-10-01", "2015-10-02", "2015-10-03", "2015-10-04", "2015-10-06"])
lc.add(x_axis_type="datetime")
lc.add(y_axis_format="currency")
lc.add(y_axis_unit="USD")
lc.push()
```

### List
Parameter Name | Optional | Data Type | Instance Variable Name | Notes
:---------------|:----------|:-----------|:--------|:----------------------
text | no | string | | stored in self.data
name | yes | string | | stored in self.data
color | yes | string | | stored in self.data
description | yes | string | | stored in self.data

Instance Methods | Accepts Parameters | Notes
:--------------- | :----------------- | :-----
self.add_data() | text, name, color, description | 

######Example:

```python
lt = geckopush.List(dashboard=d,
                    widget_key=lst_widget_key)
lt.add_data(text="12345", name="numbers",
            color="#ff2015", description="These are numbers")
lt.add_data(text="abcde", name="letters", color= "#ffffff", description="These are letters")
lt.push()
```

### Map
Parameter Name | Optional | Data Type | Instance Variable Name | Notes
:---------------|:----------|:-----------|:--------|:----------------------
city_name | | string | | stored in self.data
country_code | | string | | stored in self.data
region_code | | string | | stored in self.data
latitude | | float | | stored in self.data
longitude | | float | | stored in self.data
ip | | string | | stored in self.data
host | | string | | stored in self.data

Instance Methods | Accepts Parameters | Notes
:--------------- | :----------------- | :-----
self.add_data() | city_name, country_code, region_code, latitude, longitude, ip, host | 

When adding a map point, the method checks whether the correct set of variables are input.  For example, you can only call city_name, country_code, and region_code in the same add_data() call.  If you try to mix city_name and longitude, the method will raise an error.  The method also checks if both a text and secondary value are supplied and raises an error if so.


######Example:

```python
mp = geckopush.Map(dashboard=d, widget_key=map_widget_key)
mp.add_data(city_name="New York", country_code="US", size="10")
mp.add_data(host="google.com")
mp.add_data(ip="46.228.47.115")
mp.add_data(latitude=22.434355, longitude=11.12345, size=5, color="#ffffff")
mp.push()
```

### Monitoring
Parameter Name | Optional | Data Type | Instance Variable Name | Notes
:---------------|:----------|:-----------|:--------|:----------------------
status | no | string | self.status | accepts "up" or "down"
downtime | yes | string | self.downtime |
responsetime | yes | string | self.responsetime |

Instance Methods | Accepts Parameters | Notes
:--------------- | :----------------- | :-----
self.add_data() | status, downtime, responsetime |


######Example:

```python
monitoring_widget_key = WIDGET_KEYS["monitoring_widget_key"]
mo = geckopush.Monitoring(dashboard=d, widget_key=monitoring_widget_key)
mo.add_data(status="up", downtime="Never", responsetime= "123 ms")
mo.push()
```

### Number and Secondary Stat
Parameter Name | Optional | Data Type | Instance Variable Name | Notes
:---------------|:----------|:-----------|:--------|:----------------------
primary_value | no | int, float | | stored in self.data
secondary_value | yes | int, float, list | | stored in self.data.  list must contain integers or floats
text | yes | string | | stored in self.data
prefix | yes | string | | stored in self.data
metric_type | yes | string | self.metric_type |
absolute | yes | string | self.absolute

Instance Methods | Accepts Parameters | Notes
:--------------- | :----------------- | :-----
self.add_data() | primary_value, secondary_value, text, prefix |
self.add() | metric_type, absolute | 

The add_data() method checks whether the secondary_value is a single number or a list of numbers for use in a line chart to be displayed underneath the primary number.

######Example:

```python
ns = geckopush.NumberAndSecondaryStat(dashboard=d, widget_key=widget_key)
ns.add_data(primary_value=15, secondary_value=25)
ns.push()

or 

ns = geckopush.NumberAndSecondaryStat(dashboard=d, widget_key=widget_key)
ns.add_data(primary_value=15, text="Hola Amigo")
ns.push()

of

ns = geckopush.NumberAndSecondaryStat(dashboard=d, widget_key=widget_key)
ns.add_data(primary_value=15, secondary_value=[5,10,15,20])
ns.push()
```

### Pie Chart
Parameter Name | Optional | Data Type | Instance Variable Name | Notes
:---------------|:----------|:-----------|:--------|:----------------------
value | no | int, float? | | stored in self.data
label | no | string | | stored in self.data
color | yes | string | | stored in self.data

Instance Methods | Accepts Parameters | Notes
:--------------- | :----------------- | :-----
self.add_data() | value, label, color |

######Example:

```python
pi = geckopush.PieChart(dashboard=d, widget_key=piechart_widget_key)
pi.add_data(100, "Slice 1", "13699c")
pi.add_data(200, "Slice 2", "198acd")
pi.push()
```

### RAG (Red, Amber, Green)
Push to both RAG Number and RAG Column widgets.

Parameter Name | Optional | Data Type | Instance Variable Name | Notes
:---------------|:----------|:-----------|:--------|:----------------------
text | no | string | | stored in self.data
value | yes | integer | | stored in self.data
prefix | yes | string | | stored in self.data
reverse_type | yes | self.reverse_type | API only accepts "reverse" string
color | yes | string | | Accepts "red", "amber" or "green" only

Instance Methods | Accepts Parameters | Notes
:--------------- | :----------------- | :-----
self.add_data() | text, value, prefix | 
self.add() | reverse_type |

*Color: The Geckoboard API detects color assignment to Red, Amber or Green through the positioning of the text/value/prefix payloads.  This optional parameter allows you to specify the exact color you want to assign the data to without having to declare your data points in order.  If omitted, the .add_data() method will assign it to the next unassigned color in the order from Red->Amber->Green.  

######Example:

```python
rg = geckopush.RAG(dashboard=d, widget_key=widget_key)
rg.add_data(text="One", value=50, prefix="$", color="green")
rg.add_data(text="Two", value=100, prefix="$", color="amber")
rg.add_data(text="Three", value=150, prefix="$")  # Will be assigned to red automatically.
rg.push()
```

### Text
Parameter Name | Optional | Data Type | Instance Variable Name | Notes
:---------------|:----------|:-----------|:--------|:----------------------
text | no | string | | stored in self.data
text_type | yes | integer | | stored in self.data

Instance Methods | Accepts Parameters | Notes
:--------------- | :----------------- | :-----
self.add_data() | text, text_type |

This widget accepts a max of 10 text items.

######Example:

```python
rg = geckopush.Text(dashboard=d, widget_key=widget_key)
rg.add_data(text="Hello There My Friend", type=0)
rg.add_data(text="How are you doing?", type=1)
rg.push()
```



For questions, issues, bugs please contact the author through github or email.