import networkx
G = networkx.path_graph(4)
pos = networkx.spring_layout(G)
for node in G.nodes:
    G.nodes[node]["pos"] = list(pos[node])
print(G.nodes.data())


#attrs = {0: {"attr1": 20, "attr2": "nothing"}, 1: {"attr2": 3}}


#d = {'rating': 273, 'mediaRecommendation': {'id': 101921, 'popularity': 307544, 'title': {'romaji': 'Kaguya-sama wa Kokurasetai: Tensaitachi no Renai Zunousen'}}}
#
#def flatten(d, parent_key=''):
#    items = []
#    for k, v in d.items():
#        child_key = k if parent_key else k
#        if isinstance(v, dict):
#            items.extend(flatten(v, child_key).items())
#        else:
#            items.append((child_key, v))
#    return dict(items)
#
#fd = flatten(d)
#nd = {fd["id"]: fd}
#G.add_node(fd["id"])
#networkx.set_node_attributes(G, nd)

