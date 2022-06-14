import json
import networkx
import os
import requests

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
    print(G.nodes.data())
    print(G.edges.data())
#    networkx.write_graphml(G, r"C:\Users\u227838\Documents\Graphtst.gz")
if __name__ == "__main__":
    main()