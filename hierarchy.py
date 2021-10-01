from osmapi import OsmApi
from json import dumps, loads
import time

LANGUAGE = "de"

def slow(ret):
    time.sleep(0.15)
    return ret

def get_name(relation):
    if ('name:' + LANGUAGE) in relation['tag']:
        return relation['tag']['name:' + LANGUAGE]

    return relation['tag']['name']

def add_path(path, fullpath, upaths):
    added = False
# TODO reverse paths
    if path[0] in fullpath:
        print("found begin")
        pos = border.index(path[0])
        border[pos+1:pos+1] = path[1:]
        added = True
    elif path[-1] in fullpath:
        print("found end")
        pos = fullpath.index(path[-1])
        fullpath[pos:pos] = path[:-1]
        added = True
    else:
        upaths.append(path)

    # We need to check recursively if the unknown paths fits
    if added:
        new_upaths = upaths
        for p in upaths:
            if len(p) and p in new_upaths:
                ret, paths, new_upaths = add_path(p, fullpath, new_upaths)

    return added, fullpath, upaths

def __get_area(relation, recursionlevel, notlastlevel):
    area = {
        'name': get_name(relation),
        'boundary': relation['tag']['boundary'],
        'admin_level': relation['tag']['admin_level']
    }

    print("--" * (recursionlevel - notlastlevel), area['name'], "Relation ID:", relation['id'])
    subareas = []
    polypath = []
    borderways = []
    for member in relation['member']:        
        if notlastlevel and "subarea" == member['role'] and "relation" == member['type']:
            subareas.append(__get_area(api.RelationGet(member['ref']), recursionlevel, notlastlevel - 1))
        elif "outer" == member['role'] and "way" == member['type']:
            borderways.append(member['ref'])

    if len(subareas):
        print(len(subareas))
        area['subareas'] = subareas

    if len(polypath):
        area['subareas'] = subareas

    if len(borderways):
        area['borderways'] = borderways

    return area

def get_area(relation, recursionlevel = 1):
    return __get_area(relation, recursionlevel, recursionlevel)

api = OsmApi()
# Region Hannover 62764
bways = get_area(api.RelationGet(slow(11623875)), 5)['borderways']

for way in bways:
    w = api.WayGet(slow(way))
    path = w['nd']
    print(path)

#print(get_area(api.RelationGet(slow(11623875)), 5))

'''
For borderways:
        border = []
        unknownpaths = []
            way = api.WayGet(slow(member['ref']))
            path = way['nd']
            if way['visible'] and len(path):
                ret, border, unknownpaths = add_path(path, border, unknownpaths)
                
    if len(border) and border[0] == border[-1]:
        print("Complete path")
        for nodes in border:
            n = api.NodeGet(slow(node))
            polypath.append((n['lat'], n['lon']))
'''
