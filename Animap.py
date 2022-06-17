import json
import networkx
import os
import requests
import matplotlib.pyplot as plt
import plotly.graph_objects as go


def anime_request(id):
    query = '''
query ($id: Int) { # Define which variables will be used in the query (id)
Media (id: $id, type: ANIME) {
    id
    popularity
    title {
    romaji
    }
    recommendations (sort: RATING_DESC) {
    nodes {
        rating
        mediaRecommendation {
        id
        popularity
        title {
            romaji
        }
        }
    }
    }
}
}
'''
    variables = {
        'id': id
    }
    url = 'https://graphql.anilist.co'
    return requests.post(url, json={'query': query, 'variables': variables})

def flatten(d, parent_key=''):
    items = []
    for k, v in d.items():
        child_key = k if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten(v, child_key).items())
        else:
            items.append((child_key, v))
    return dict(items)
    
def tracing(G: networkx.graph):
    edge_x = []
    edge_y = []
    edge_width = []
    for edge in G.edges:
        x0, y0 = G.nodes[edge[0]]["pos"]
        x1, y1 = G.nodes[edge[1]]["pos"]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        edge_width.append(G.edges[edge]['weight'])


    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=3, color='Black'),
        hoverinfo='text',
        hoverlabel={"bgcolor": "MediumSeaGreen", "font": {"color": "Black"}},
        text=edge_width,
        mode='lines')

    node_x = []
    node_y = []
    node_text = []
    node_popularity = []
    for node in G.nodes():
        x, y = G.nodes[node]['pos']
        node_x.append(x)
        node_y.append(y)
        node_text.append(f"name:{G.nodes[node]['romaji']}\npopularity:{G.nodes[node]['popularity']}")
        node_popularity.append(G.nodes[node]["popularity"])

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        hoverlabel={"bgcolor": "MediumSeaGreen", "font": {"color": "Black"}},
        text=node_text,
        marker=dict(
            size=50,
            colorscale='Picnic',
            showscale=True,
            color=node_popularity,
            colorbar=dict(
                thickness=25,
                title='Node Popularity',
                xanchor='left',
                titleside='right'
            ),
            line_width=3
        )
    )

    fig = go.Figure(data=[edge_trace, node_trace],
        layout=go.Layout(
            title=f'Recommendations for X',
            titlefont_size=16,
            showlegend=False,
            hovermode='closest',
            margin=dict(b=20,l=5,r=5,t=40),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
        )
    )
    fig.show()

def main():
    anime_input = int(input("Anime ID: "))
    # call anime_request function and format its response
    anime_dict = flatten(json.loads(anime_request(anime_input).text))
    rec_list = anime_dict["nodes"]
    del anime_dict["nodes"]
    main_anime_dict = {anime_dict["id"]: anime_dict}
    G = networkx.Graph()
    #create node for requested anime and give it its attributes
    G.add_node(anime_dict["id"])
    networkx.set_node_attributes(G, main_anime_dict)

    for anime in rec_list:
        recommended_dict = flatten(anime)
        del recommended_dict["rating"]
        anime_attributes = {recommended_dict["id"]: recommended_dict}
        G.add_node(recommended_dict["id"])
        G.add_edge(anime_dict["id"], recommended_dict["id"], weight=anime["rating"])
        networkx.set_node_attributes(G, anime_attributes)
    pos = networkx.spring_layout(G)
    for node in G.nodes:
        G.nodes[node]["pos"] = list(pos[node])
    tracing(G)

if __name__ == "__main__":
    main()
