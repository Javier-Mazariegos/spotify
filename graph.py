class Graph:
    def __init__(self):
        self.adjacency_lists = {}
    
    def __repr__(self):
        g = ""
        for key, value in self.adjacency_lists.items():
            g += key +":"+ str(value) +"\n"
        return g

    def add_node(self, node_label):
        self.adjacency_lists[node_label] = []

    def add_edge(self, start_node, end_node):
        self.adjacency_lists[start_node].append(end_node)
    
    def find_path(self, start, end, path=[]):
        path = path + [start]
        if start == end:
            return path
        if start not in self.adjacency_lists.keys() or end not in self.adjacency_lists.keys():
            return None
        for node in self.adjacency_lists[start]:
            if node not in path:
                newpath = self.find_path(node, end, path)
                if newpath: return newpath
        return None

    def find_all_paths(self, start, end, path=[]):
        path = path + [start]
        if start == end:
            return [path]
        if start not in self.adjacency_lists.keys() or end not in self.adjacency_lists.keys():
            return []
        paths = []
        for node in self.adjacency_lists[start]:
            if node not in path:
                newpaths = self.find_all_paths(node, end, path)
                for newpath in newpaths:
                    paths.append(newpath)
        return paths

    def find_shortest_path(self, start, end, path=[]):
        path = path + [start]
        if start == end:
            return path
        if start not in self.adjacency_lists.keys() or end not in self.adjacency_lists.keys():
            return None
        shortest = None
        for node in self.adjacency_lists[start]:
            if node not in path:
                newpath = self.find_shortest_path(node, end, path)
                if newpath:
                    if not shortest or len(newpath) < len(shortest):
                        shortest = newpath
        return shortest