# lazyplotly
A wrapper of interactive visualization package plotly. Sometimes we are just too lazy to writer every parameter. Especially creating dropdown menus or slide bars is a way too time-consuming. How about write it simply with a line of code?

### Installation
```
$ pip install plotly lazyplotly
```
### Quick Start
```
import lazyplotly as lp

# using list data type to fit
bar = lp.bar(x=[1,2,3], y=[23,43,32], cmap='Viridis')

# add layout in plot function
lp.plot(bar,xlabel='category', ylabel='value', title='MyAwesomeTitle')
```
### Custom extension
```
# using dataframe object by setting xy variables with column name
df = dict(order=[1,2,3,4,5],lower=[21,32,43,54,32],upper=[23,34,50,60,60])
area = lp.area(x='order', y='lower', y2='upper', df=df, color='orange')

# add output variable to export as a html file
lp.plot(
    data = area, 
    rangeslider = True,
    layout = dict(title='So Easy Right?'),
    config = dict(displayModeBar=True),
    output = 'MyPlot.html'
)
```
### Subplot
```
df = dict(x=[1,2,3,4,5],y=[21,32,43,54,32],y2=[23,34,50,60,60])
df2 = dict(x=[1,2,3,4,5],y=[23,35,43,34,22],y2=[25,43,60,60,70])

bar = lp.bar(x='x', y='y', df=df, name='season 1', color='#c2185b')
bar1 = lp.bar(x='x', y='y2', df=df2, name='season 2', color='#0097a7')
bar2 = lp.bar(x='x', y='y', df=df, name='season 3', color='#afb42b')
bar3 = lp.bar(x='x', y='y2', df=df2, name='season 4', color='#0288d1')
lp.plot([bar,bar1,bar2,bar3], rows=2)
```
```
# subplot with grouped stack bar
lp.plot([[bar,bar1],[bar2,bar3]], cols=2, layout=dict(barmode='stack'))
```
```
# subplot with pie charts
pie = lp.pie(x='x',y='y',df=df)
pie1 = lp.pie(x='x',y='y',df=df, hole=0.2)
pie2 = lp.pie(x='x',y='y',df=df, hole=0.4)
lp.plot([pie,pie1,pie2],cols=3)
```
### Boxplot
```
box = lp.box(y='y',df=df)
box1 = lp.box(y='y2',df=df)
box2 = lp.box(y='y',df=df2)
box3 = lp.box(y='y2',df=df2)
lp.plot([box,box1,box2,box3])
```
### 3D scatter
```
df = dict(x=[1,2,3,4,5],y=[21,32,43,54,32],z=[23,34,50,60,60])

scatter3d = lp.scatter3d(x='x',y='y',z='z', df=df)
lp.plot(scatter3d, no_padding=True)
```
### Widget
```
df = dict(x=[1,2,3,4,5],y=[21,32,43,54,32],y2=[23,34,50,60,60])
df2 = dict(x=[1,2,3,4,5],y=[23,35,43,34,22],y2=[25,43,60,60,70])

scatter = lp.scatter(x='x',y='y',df=df)
scatter1 = lp.scatter(x='x',y='y2',df=df)
scatter2 = lp.scatter(x='x',y='y',df=df2)
scatter3 = lp.scatter(x='x',y='y2',df=df2)

# dropdown menu (wrap datas with two dimensional list)
lp.dropdown([[scatter,scatter1],[scatter2,scatter3]])

# slider bar
lp.slider([[scatter],[scatter1],[scatter2],[scatter3]])
```
### Some charts are only supported with dataframe
```
import pandas as pd

df = pd.DataFrame(dict(origin=[1,2,3,4,5],destin=[21,32,43,54,32],count=[23,34,50,60,60]))
# heatmap
lp.plot(lp.heatmap(df=df, cmap='Viridis'))

# sankey diagram
sankey = lp.sankey(df=df)
lp.dropdown([[sankey],[sankey]])
```
### APIs
```
lp.cmap     # show all colorscales available in plotly
plot()      # subplot(data, layout=None, output=False, config=None,
                        cols=None, rows=None, rangeslider=False,
                        no_padding=False, title='', xlabel='', ylabel='')
dropdown()  # accept two dim lists
slider()    # same as dropdown
bar(x, y, df, name, color, cmap)
scatter(x, y, df, name, color)
scatter3d(x, y, z, df, name, color, cmap)
line(x, y, df, name, color)
line3d(x, y, z, df, name, color)
area(x, y, y2, df, name, color)
area3d(x, y, z, df, name, color)
mesh3d(x, y, z, df, name, color)
box(y, df, name, color)
histogram(x, df, name, color, <int>bins, <bool>cum, <bool>prob)
pie(x, x2, y, df, name, hole, color)
heatmap(df, cmap)
sankey(df)
```