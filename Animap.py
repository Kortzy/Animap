import json
import networkx
import os
import requests
import matplotlib.pyplot as plt
import plotly.graph_objects as go

def flatten(dictionary):
    items = []
    for k, v in dictionary.items():
        if isinstance(v, dict):
            items.extend(flatten(v).items())
        else:
            items.append((k, v))
    return dict(items)

def anime_request():
    id = int(input("Anime ID: "))
    query = '''
query ($id: Int) { # Define which variables will be used in the query (id)
  Media (id: $id, type: ANIME) {
    id
    popularity
    title {
      romaji
    }
    recommendations (sort: RATING_DESC, perPage: 10) {
      nodes {
        rating
        mediaRecommendation {
          id
          popularity
          title {
            romaji
          }
          recommendations (sort: RATING_DESC, perPage: 3) {
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
    }
  }
}
'''
    variables = {
        'id': id
    }
    url = 'https://graphql.anilist.co'
    return flatten(json.loads(requests.post(url, json={'query': query, 'variables': variables}).text))

def tracing(G: networkx.graph):
    edge_x = []
    edge_y = []
    edge_desc_x = []
    edge_desc_y = []
    edge_desc_text = []
    for edge in G.edges:
        x0, y0 = G.nodes[edge[0]]["pos"]
        x1, y1 = G.nodes[edge[1]]["pos"]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        edge_desc_x += tuple([(x0 + x1) / 2])
        edge_desc_y += tuple([(y0 + y1) / 2])
        edge_desc_text.append(f"Rating:{G.edges[edge]['weight']}")


    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=3, color='Black'),
        mode='lines')

    edge_desc_trace = go.Scatter(
        x=edge_desc_x, y=edge_desc_y,
        hovertext=edge_desc_text,
        mode="markers",
        hoverinfo="text",
        hoverlabel={"bgcolor": "MediumSeaGreen", "font": {"color": "Black"}},
        marker=dict(
            size=20,
            color="Black"),
        opacity=0.2)
        
    node_x = []
    node_y = []
    node_text = []
    node_popularity = []
    for node in G.nodes:
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

    fig = go.Figure(data=[edge_trace, node_trace, edge_desc_trace],
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

def main_anime(anime_dict):
    anime = {k: v for k, v in anime_dict.items() if k != "nodes"}
    return {anime["id"]: anime}       
    
def node_attributes(anime_dict):
    rec_list = anime_dict["nodes"]
    attributes = main_anime(anime_dict)
    for anime in rec_list:
        recommended_dict = {k: v for k, v in flatten(anime).items() if k != "nodes"}
        attributes.update({recommended_dict["id"]: recommended_dict})
    return attributes

def network_graph(G: networkx.graph, attributes):
    main_d_id = next(iter(attributes))
    for k, v in attributes.items():
        G.add_node(k)
        if "rating" in v.keys():
            G.add_edge(main_d_id, k, weight=v["rating"])
        else:
            pass
        networkx.set_node_attributes(G, {k:v})
    pos = networkx.spring_layout(G)
    for node in G.nodes:
        G.nodes[node]["pos"] = list(pos[node])
    
def main():
    #json.dump(anime_dict, open(r'C:\Users\u227838\Documents\Animap\dict.json', "w"), indent=2)
    G = networkx.Graph()
    anime_dicti = anime_request()
    attributes = node_attributes(anime_dicti)
    network_graph(G, attributes)
    for nodes in anime_dicti["nodes"]:
        network_graph(G, node_attributes(flatten(nodes)))
    tracing(G)

if __name__ == "__main__":
    main()
