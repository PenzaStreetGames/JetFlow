import typing as tp


class JetNode:
    def __init__(self, value=None):
        self.value = value
        self.in_edge: tp.Optional[JetEdge] = None
        self.out_edges: tp.List[JetEdge] = []

    def set(self, val):
        self.value = val
        for out_edge in self.out_edges:
            out_edge.update()

    def get(self):
        return self.value


class JetEdge:
    def __init__(self, in_nodes: tp.List[JetNode] = (),
                 out_node: tp.Optional[JetNode] = None,
                 func: tp.Callable = None):
        self.out_node: tp.Optional[JetNode] = out_node
        if out_node is not None:
            out_node.in_edge = self
        self.in_nodes: tp.List[JetNode] = in_nodes
        for in_node in in_nodes:
            in_node.out_edges.append(self)
        self.func: tp.Callable = func

    def update(self):
        res = self.func(*[node.get() for node in self.in_nodes])
        if self.out_node is not None:
            self.out_node.set(res)


def exp(x, n):
    res = [1]
    for i in range(1, n):
        elem = res[-1] * x / i
        res.append(elem)
    return res


if __name__ == '__main__':
    x, series, series_sum = \
        JetNode(value=0), JetNode(value=[]), JetNode(value=0)
    JetEdge(in_nodes=[x], out_node=series,
            func=lambda arg: exp(arg, 8))
    JetEdge(in_nodes=[series], out_node=series_sum, func=sum)
    for i in range(10):
        x.set(i)
        print(f"exp({x.get()}) = ",
              " + ".join(f"{num:.4f}" for num in series.get()),
              f" = {series_sum.get():.4f}")
