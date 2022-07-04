from typing import Optional, Callable, List


class JetData:
    def __init__(self, value=None, source=None, outputs=None):
        if outputs is None:
            outputs = []
        self.source = source
        self.outputs = outputs
        self.value = value

    def change_signal(self):
        for output in self.outputs:
            output.change_handler()

    def set(self, value):
        self.value = value
        self.change_signal()

    def get(self):
        return self.value

    def add_output(self, result):
        self.outputs.append(result)
        if self not in result.inputs:
            result.inputs.append(self)

    def set_source(self, source):
        self.source = source
        if self.source.result is not self:
            self.source.result = self

    def __str__(self):
        return f"JetData({str(self.value)})"

    def __repr__(self):
        return f"JetData({repr(self.value)})"


class JetNode:
    def __init__(self, inputs: Optional[List[JetData]] = None, result: Optional[JetData] = None, func: Callable = None):
        if inputs is None:
            inputs = []
        self.inputs = inputs
        self.result = result
        self.func = func

    def set_func(self, func: Callable):
        self.func = func

    def change_handler(self):
        args = [source.get() for source in self.inputs]
        new_value = self.func(*args)
        self.result.set(new_value)

    def add_source(self, source: JetData):
        self.inputs.append(source)
        if self not in source.outputs:
            source.outputs.append(self)

    def set_result(self, result: JetData):
        self.result = result
        if self.result.source is not self:
            self.result.source = self


def exp(x, n):
    res = [1]
    for i in range(1, n):
        elem = res[-1] * x / i
        res.append(elem)
    return res


if __name__ == '__main__':
    x = JetData(value=0)
    seq = JetData()
    node = JetNode()
    node.set_func(lambda x: exp(x, 10))
    node.add_source(x)
    node.set_result(seq)
    print(seq)
    x.set(1)
    print(seq)
