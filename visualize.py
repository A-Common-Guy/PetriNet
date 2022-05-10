import plotly.graph_objects as go
from net import Net
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from plotly.graph_objs import *
 


# C matrix and M0 vector
net=Net(np.array([
    [-1,-1,0,0,2],
    [1,-1,0,0,0],
    [1,0,-1,0,0],
    [0,1,0,-1,0],
    [0,0,1,0,-1],
    [0,0,0,1,-1],
    [-1,1,0,0,0]
    ]),np.array([2,0,0,0,0,0,1]))


net.simulate(net.M0)
print(net.mark)
graph=net.getGraph()



print("p-invariants\n",net.p_reduce())

G=graph

pos=nx.spiral_layout(G)

#print(pos)
#print(G.edges())

edge_x = []
edge_y = []
for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_x.append(x0)
    edge_x.append(x1)
    edge_x.append(None)
    edge_y.append(y0)
    edge_y.append(y1)
    edge_y.append(None)

edge_trace = go.Scatter(
    x=edge_x, y=edge_y,
    line=dict(width=0.5, color='#888'),
    hoverinfo='none',
    mode='lines')


size_vect=[50 for i in range(len(G.nodes()))]
size_vect[0]=100

node_x = []
node_y = []
for node in pos.values():
    x, y = node
    node_x.append(x)
    node_y.append(y)

node_trace = go.Scatter(
    x=node_x, y=node_y,
    mode="lines+markers+text",
    hoverinfo='text',
    
    marker=dict(
        showscale=True,
        # colorscale options
        #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
        #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
        #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
        colorscale='YlGnBu',
        size = size_vect,

        reversescale=True,
        color=[],
        colorbar=dict(
            thickness=15,
            title='Node Connections',
            xanchor='left',
            titleside='right'
        ),
        line_width=2
        )
        )
node_adjacencies = []
textFor=np.copy(net.Mvect).astype(int)
node_text = ["M"+str(a)+"\n"+np.array2string(vec) for a,vec in enumerate(textFor)]



col = [int(a[1]) for a in net.mark]
col2 = [(a-(max(col)/2))/(max(col)*3) for a in col]
node_trace.marker.color = col2
node_trace.text = node_text


fig = go.Figure(data=[edge_trace, node_trace],
             layout=go.Layout(
                title='<br>Network graph made with Python',
                titlefont_size=16,
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                annotations=[ dict(
                    text="Petri Net Visualizer",
                    showarrow=True,
                    xref="paper", yref="paper",
                    x=0.005, y=-0.002 ) ],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                )
fig.show()
  