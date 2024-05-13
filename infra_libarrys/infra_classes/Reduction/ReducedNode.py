class ReducedNode:
    def __init__(self, original_object, package=False, old_edge=False):
        self.original_object = original_object
        self.package = None if not package else True
        self.old_edge = old_edge
        self.edges = set()

    def add_reduced_edge(self, reduce_edge):
        self.edges.add(reduce_edge)
