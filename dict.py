d = {'rating': 273, 'mediaRecommendation': {'id': 101921, 'popularity': 307544, 'title': {'romaji': 'Kaguya-sama wa Kokurasetai: Tensaitachi no Renai Zunousen'}}}

def flatten(d, parent_key=''):
    items = []
    for k, v in d.items():
        child_key = k if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten(v, child_key).items())
        else:
            items.append((child_key, v))
    return dict(items)

fd = flatten(d)
nd = {fd["id"]: fd}
t = [{k: v} for k,v in fd.items()]
print(del fd["rating"])


