import collections

def split_edges(lines):
    return [a.split(')') for a in lines.splitlines()]

def create_tree(edges):
    trees = collections.defaultdict(dict)

    for parent, child in edges:
        trees[parent][child] = trees[child]
    
    return {"COM": trees['COM']}

def count_orbits(edges):
    tree = create_tree(edges)

    path = ['COM']

    def search(tree, path):
        cur_vertex = tree
        for ele in path:
            cur_vertex = cur_vertex.get(ele, None)
            if not cur_vertex:
                return len(path) - 1
        
        orbits = len(path) - 1
        for child in cur_vertex.keys():
            orbits += search(tree, path + [child])

        return orbits
    
    return search(tree, path)

def find_path(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return path
    
    if start not in graph:
        return None
    
    for node in graph[start]:
        if node not in path:
            newpath = find_path(graph, node, end, path)
            if newpath: return newpath
    
    return None

def count_transfers(edges, start, end):
    edge_map = collections.defaultdict(list)
    for left, right in edges:
        edge_map[left].append(right)
        edge_map[right].append(left)

    path = find_path(edge_map, start, end) 
    
    return len(path) - 1 - 2