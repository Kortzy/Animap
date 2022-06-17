import networkx
import os
import dash
import plotly.graph_objs as go
from colour import Color

G = networkx.read_graphml(os.getcwd() + "/Graphtst.graphml")

pos = networkx.spring_layout(G)
for node in G.nodes: 
    G.nodes[node]["pos"] = list(pos[node]) 

#print(G.nodes["125367"])
def get_edge_traces(G: networkx.graph) -> list:
    traces = []
    num_edges = len(G.edges())
    if num_edges == 0:
        return traces
    
    index = 0
    for edge in G.edges:
        x0, y0 = G.nodes[edge[0]]["pos"]
        x1, y1 = G.nodes[edge[1]]["pos"]
        trace = go.Scatter(
            x=tuple([x0, x1, None]),
            y=tuple([y0, y1, None]),
            mode="lines",
            line_shape="spline",
        )
        traces.append(trace)
        index = index +1
    return traces
    
def get_node_traces(G: networkx.graph) -> list:
    node_family = go.Scatter(
        x=[],
        y=[],
        hovertext=[],
        text=[],
        mode="markers+text",
        textposition="bottom center",
        hoverinfo="text",
        hoverlabel={"bgcolor": "MediumSeaGreen", "font": {"color": "Black"}},
        marker={"size": 8, "color": "ForestGreen",},
    )
    for id, node in G.nodes().items():
        x, y = node["pos"]

        node_family["x"] += tuple([x])
        node_family["y"] += tuple([y])
        node_family["hovertext"]
        node_family["text"]

    return node_family
    
print(get_node_traces(G))
print(get_edge_traces(G))

#G = networkx.random_regular_graph(8, 14)
#
#edge_x = []
#edge_y = []
#for edge in G.edges():
#    x0, y0 = G.nodes[edge[0]]['pos']
#    x1, y1 = G.nodes[edge[1]]['pos']
#    edge_x.append(x0)
#    edge_x.append(x1)
#    edge_x.append(None)
#    edge_y.append(y0)
#    edge_y.append(y1)
#    edge_y.append(None)
#
#edge_trace = go.Scatter(
#    x=edge_x, y=edge_y,
#    line=dict(width=0.5, color='#888'),
#    hoverinfo='none',
#    mode='lines')
#
#node_x = []
#node_y = []
#for node in G.nodes():
#    x, y = G.nodes[node]['pos']
#    node_x.append(x)
#    node_y.append(y)
#
#node_trace = go.Scatter(
#    x=node_x, y=node_y,
#    mode='markers',
#    hoverinfo='text',
#    marker=dict(
#        showscale=True,
#        # colorscale options
#        #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
#        #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
#        #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
#        colorscale='YlGnBu',
#        reversescale=True,
#        color=[],
#        size=10,
#        colorbar=dict(
#            thickness=15,
#            title='Node Connections',
#            xanchor='left',
#            titleside='right'
#        ),
#        line_width=2))
#        
#node_adjacencies = []
#node_text = []
#for node, adjacencies in enumerate(G.adjacency()):
#    node_adjacencies.append(len(adjacencies[1]))
#    node_text.append('# of connections: '+str(len(adjacencies[1])))
#
#node_trace.marker.color = node_adjacencies
#node_trace.text = node_text
#
#fig = go.Figure(data=[edge_trace, node_trace],
#             layout=go.Layout(
#                title='<br>Network graph made with Python',
#                titlefont_size=16,
#                showlegend=False,
#                hovermode='closest',
#                margin=dict(b=20,l=5,r=5,t=40),
#                annotations=[ dict(
#                    text="Python code: <a href='https://plotly.com/ipython-notebooks/network-graphs/'> https://plotly.com/ipython-notebooks/network-graphs/</a>",
#                    showarrow=False,
#                    xref="paper", yref="paper",
#                    x=0.005, y=-0.002 ) ],
#                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
#                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
#                )
#fig.show()
