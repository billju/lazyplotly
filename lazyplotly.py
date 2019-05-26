import plotly.graph_objs as go
from plotly import offline
offline.init_notebook_mode(connected=True)

def check_and_set(dic,key,subkey,value):
    if not key in dic:
        dic[key] = dict()
    dic[key][subkey] = value
    return dic
def plot(data,layout=None,output=False,config=None,cols=None,rows=None,
        rangeslider=False,no_padding=False,title='',xlabel='',ylabel=''):
    #初始化設定，不可使用dict作為預設變數，否則變數不會更新
    layout = {} if layout is None else layout
    config = {} if config is None else config
    #確保資料格式
    trace_id_list = []
    trace_id = 0
    if type(data)==list:
        trace_list = []    
        for trace in data:
            if type(trace)==list:
                trace_list.extend(trace)
                trace_id_list.extend([trace_id for _ in range(len(trace))])
            else:
                if not 'type' in trace:
                    trace['type'] = 'pie'
                trace_list.append(trace)
                trace_id_list.append(trace_id)
            trace_id+= 1
        data = trace_list
    else:
        data = [data]
        trace_id_list.append(trace_id)
    grid_count = max(trace_id_list)+1
    #設定子圖
    if rows and not cols:
        cols = grid_count//rows
        cols+= 1 if grid_count%rows>0 else 0
    elif cols and not rows:
        rows = grid_count//cols
        rows+= 1 if grid_count%cols>0 else 0
    if rows or cols:
        for i in range(len(data)):
            trace = data[i].copy()
            trace_id = trace_id_list[i]
            if trace['type'] in ['pie','sunburse','sankey']:
                trace['domain'] = dict(row=trace_id//cols,column=trace_id%cols)
            else:
                trace['xaxis'] = f'x{trace_id%cols+1}'
                trace['yaxis'] = f'y{trace_id//cols+1}'
            data[i] = trace
        layout['grid'] = go.layout.Grid(columns=cols, rows=rows) 
    #設定卷軸
    if not 'xaxis' in layout:
        layout['xaxis'] = dict()
    layout['xaxis']['rangeslider'] = dict(visible = rangeslider)
    if no_padding:
        layout['margin'] = dict(l=0,r=0,b=0,t=0)
    #設定標題
    if title:
        layout['title'] = title
    if xlabel:
        layout = check_and_set(layout,'xaxis','title',xlabel)
    if ylabel:
        layout = check_and_set(layout,'yaxis','title',ylabel)
    fig = go.Figure(data=data,layout=layout)
    #設定輸出
    return offline.plot(fig,config=config,filename=output,auto_open=False) if output else offline.iplot(fig,config=config)

class TypeError(Exception):
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def dropdown(datas,btn_labels=[],layout=None,output=False,config=None,
                no_padding=False,title='',xlabel='',ylabel=''):
    layout = {} if layout is None else layout
    config = {} if config is None else config
    buttons = []
    for i, data in enumerate(datas):
        arg_dict = {}
        try:
            for trace in data:
                for feature in ['x','y','labels','values','text','node','link']:
                    if feature in trace.keys():
                        if not feature in arg_dict.keys():
                            if feature in ['node','link']:
                                arg_dict[feature] = [trace[feature]]
                            else:
                                arg_dict[feature] = [list(trace[feature])]
                        else:
                            if feature in ['node','link']:
                                arg_dict[feature].append(trace[feature])
                            else:
                                arg_dict[feature].append(list(trace[feature]))
        except:
            raise TypeError('did you forgot to wrap these charts?')
        button = dict(
            method='update',
            label= i+1 if i+1>len(btn_labels) else btn_labels[i],
            args=[arg_dict]
        )
        buttons.append(button)
    layout['updatemenus'] = [dict(buttons=buttons)]
    if no_padding:
        layout['margin'] = dict(l=0,r=0,b=0,t=0)
    #設定標題
    if title:
        layout['title'] = title
    if xlabel:
        layout = check_and_set(layout,'xaxis','title',xlabel)
    if ylabel:
        layout = check_and_set(layout,'yaxis','title',ylabel)
    fig = go.Figure(data=datas[0],layout=layout)
    return offline.plot(fig,filename=output,auto_open=False) if output else offline.iplot(fig)
def slider(datas,prefix='',layout=None,config=None,output=False,
                no_padding=False,title='',xlabel='',ylabel=''):
    layout = {} if layout is None else layout
    config = {} if config is None else config
    steps = []
    for data in datas:
        arg_dict = {}
        try:
            for trace in data:
                for feature in ['x','y','labels','values','text','node','link']:
                    if feature in trace.keys():
                        if not feature in arg_dict.keys():
                            if feature in ['node','link']:
                                arg_dict[feature] = [trace[feature]]
                            else:
                                arg_dict[feature] = [list(trace[feature])]
                        else:
                            if feature in ['node','link']:
                                arg_dict[feature].append(trace[feature])
                            else:
                                arg_dict[feature].append(list(trace[feature]))
        except:
            raise TypeError('did you forgot to wrap these charts?')
        step = dict(
            method='update',
            args=[arg_dict]
        )
        steps.append(step)
    layout['sliders'] = [dict(currentvalue=dict(prefix=prefix),steps=steps)]
    if no_padding:
        layout['margin'] = dict(l=0,r=0,b=0,t=0)
    #設定標題
    if title:
        layout['title'] = title
    if xlabel:
        layout = check_and_set(layout,'xaxis','title',xlabel)
    if ylabel:
        layout = check_and_set(layout,'yaxis','title',ylabel)    
    fig = go.Figure(data=datas[0],layout=layout)
    return offline.plot(fig,filename=output,auto_open=False) if output else offline.iplot(fig)


cmap = ['Greys', 'YlGnBu', 'Greens', 'YlOrRd', 'Bluered', 'RdBu',
        'Reds', 'Blues', 'Picnic', 'Rainbow', 'Portland', 'Jet',
        'Hot', 'Blackbody', 'Earth', 'Electric', 'Viridis', 'Cividis']
def make_params(x,y,df,name):
    if df is not None:
        name = name if name else y
        x = df[x] if x else None
        y = df[y] if y else None
    return x,y,name
def bar(x,y,df=None,name=None,color=None,cmap=None,vertical=False,diverge=False):
    #orientation='h',hoverinfo='text',
    x,y,name = make_params(x,y,df,name)
    trace = dict(type='bar',x=x,y=y,name=name,marker=dict(color=color))
    if cmap:
        trace['marker'] = dict(color=y,colorscale=cmap)
    return trace
def scatter(x,y,df=None,name=None,color=None):
    x,y,name = make_params(x,y,df,name)
    trace = dict(type='scatter',x=x,y=y,name=name,mode='markers',marker=dict(color=color))
    return trace
def scatter3d(x,y,z,df=None,name=None,color=None,cmap=None):
    x,y,name = make_params(x,y,df,name)
    z = df[z] if df is not None else z
    trace = dict(type='scatter3d',x=x,y=y,z=z,name=name,mode='markers',marker=dict(color=color))
    if cmap:
        trace['marker'] = dict(color=z,opacity=0.8,colorscale=cmap)
    return trace
def line(x,y,df=None,name=None,color=None):
    x,y,name = make_params(x,y,df,name)
    trace = dict(type='scatter',x=x,y=y,name=name,mode='lines',line=dict(color=color))
    return trace
def line3d(x,y,z,df=None,name=None,color=None):
    x,y,name = make_params(x,y,df,name)
    z = df[z] if df is not None else z
    trace = dict(type='scatter3d',x=x,y=y,z=z,mode='lines')
    if color:
        trace['line'] = dict(color=color)
    return trace
def area(x,y,df=None,name=None,y2=None,color=None):
    #['tozeroy','tonexty','tozerox'][之間、底部、頂部]
    x,y,name = make_params(x,y,df,name)
    if y2:
        y2 = df[y2] if df is not None else y2
        trace_t = dict(type='scatter',x=x,y=y,name=name,mode='lines',fill=None,line=dict(color=color))
        trace_b = dict(type='scatter',x=x,y=y2,name=name,mode='lines',fill='tonexty',
                        fillcolor=color,line=dict(color=color))
        return [trace_t,trace_b]
    trace = dict(type='scatter',x=x,y=y,name=name,mode='lines',fill='tonexty')
    return trace
def area3d(x,y,z,df=None,name=None,color=None):
    x,y,name = make_params(x,y,df,name)
    z = df[z] if df is not None else z
    trace = dict(type='scatter3d',x=x,y=y,z=z,
                    mode='none',surfaceaxis=1,surfacecolor=color)
    return trace
def mesh3d(x,y,z,df=None,name=None,color=None):
    x,y,name = make_params(x,y,df,name)
    z = df[z] if df is not None else z
    trace = dict(type='mesh3d',x=x,y=y,z=z,alphahull=7,opacity=0.1)
    return trace
def box(y,df=None,name=None,color=None):
    _,y,name = make_params(None,y,df,name)
    trace = dict(type='box',y=y,marker=dict(color=color))
    return trace
def histogram(x,df=None,name=None,bins=None,cum=False,prob=False):
    x,_,name = make_params(x,None,df,name)
    trace = dict(type='histogram',x=x,name=name,cumulative=dict(enabled=cum))
    if bins:
        trace['nbinsx'] = bins
    if prob:
        trace['histnorm'] = 'probability'
    return trace
def pie(x,y,df=None,name=None,x2=None,hole=0,color=None):
    x,y,name = make_params(x,y,df,name)
    if x2:
        x2 = df[x2] if df is not None else x2
        trace = dict(type='sunburst',parents=x,labels=x2,
                        values=y,marker=dict(line=dict(width=2)))
    else:
        trace = dict(type='pie',labels=x,values=y,text=x,hole=hole)
    return trace
def heatmap(df,cmap='Viridis'):
    trace = dict(type='heatmap',x=df.index,y=df.columns,z=df.values,colorscale=cmap)
    return trace
def sankey(df):
    df = df.copy()
    df.columns = ['origin','destin','counts']
    node = list(set(df['origin']) | set(df['destin']))
    source = [node.index(origin) for origin in df['origin']]
    target = [node.index(destin) for destin in df['destin']]
    value = df['counts'].to_list()
    trace = dict(type='sankey',
                    node=dict(label=node),
                    link=dict(source=source,target=target,value=value)
                )
    return trace