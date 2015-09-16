from Geckopush import geckopush
import pprint
import json

api_key = 'THIS-IS-AN-API-KEY'
d = geckopush.Dashboard(api_key)

bar = geckopush.BarChart(dashboard=d, widget_key='stuff', data=[1,2,3])
bar.push()

bullet = geckopush.BulletGraph(dashboard=d,
                               widget_key='widdy_keey',
                               orientation='horizontal',
                               label='this is the label',
                               axis=['one', 'two', 'three'],
                               comparative="two",
                               measure_start="1",
                               measure_end="2",
                               red_start="1",
                               red_end="2",
                               amber_start="3",
                               amber_end="4",
                               green_start="1",
                               green_end="2",
                               sublabel="something",
                               projected_start='one',
                               projected_end='two',
                               )

bullet.add(orientation='horizontal',
                   label='this is the label',
                   axis=['one', 'two', 'three'],
                   comparative="two",
                   measure_start="1",
                   measure_end="2",
                   red_start="1",
                   red_end="2",
                   amber_start="3",
                   amber_end="4",
                   green_start="1",
                   green_end="2",
                   sublabel="something",
                   projected_start='one',
                   projected_end='two',)

bullet.add(orientation='horizontal',
                   label='this is the label',
                   axis=['one', 'two', 'three'],
                   comparative="two",
                   measure_start="1",
                   measure_end="2",
                   red_start="1",
                   red_end="2",
                   amber_start="3",
                   amber_end="4",
                   green_start="1",
                   green_end="2",
                   sublabel="something",
                   projected_start='one',
                   projected_end='two',)

bullet.add(orientation='horizontal',
                   label='this is the label',
                   axis=['one', 'two', 'three'],
                   comparative="two",
                   measure_start="1",
                   measure_end="2",
                   red_start="1",
                   red_end="2",
                   amber_start="3",
                   amber_end="4",
                   green_start="1",
                   green_end="2",
                   sublabel="something",
                   projected_start='one',
                   projected_end='two',)


bullet.push()

fun = geckopush.Funnel(dashboard=d, widget_key='funnel_widget_key')
fun.add(34, "step1")
fun.add(44, "step2")
fun.add(55, "step3")

fun.push()
pprint.pprint(fun.payload)

