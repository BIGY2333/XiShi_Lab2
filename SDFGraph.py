from collections import OrderedDict, namedtuple
import graphviz
import math
import queue

# This function develops a set of decorators.
def arg_type(*ty2):
    def common(fun):
        def deal(*fun_x):
            ty = map(ToCheckFun, ty2)
            if ty:
                x_list = [a for a in fun_x]
                x_list_it = iter(x_list)
                result = []
                for t_check in ty:
                    r = t_check(x_list_it.__next__())
                    result.append(r)
                print('param check result: ', result)
            return fun(*fun_x)
        return deal
    return common

def ToCheckFun(t):
    return lambda x: isinstance(x, t)

# define a Synchronous Data Flow class
class SDFGraph():
    def __init__(self, name):
        self.name = name
        self.token_inputs = []
        self.token_outputs = []
        self.token_queues = []
        self.nodes = []

    # This function is used to build a node and put the output token and input token into queue.
    @arg_type(object, str, object, object, object)
    def add_node(self, name, function, inputs, outputs):
        node = Node(name, function)
        node.inputs = self.join_queue(name, inputs, True)
        node.outputs = self.join_queue(name, outputs, False)
        self.nodes.append(node)
        return node

    # This function is used to judge whether the node is in nodes.
    @arg_type(object, object)
    def get_node(self, name):
        current_name = name[0] if (type(name) == tuple) else name
        for value in self.nodes:
            if value.name == current_name:
                return value
        return None

    # This function is used to achieve the feature which put the output token and input token into queue in function add_node()
    @arg_type(object, str, object, bool)
    def join_queue(self, current_name, node_list, input_flag):
        result = []
        if type(node_list) != list and type(node_list) != tuple:
            self.token_queues.append(node_list)
            result.append(node_list)
            if input_flag:
                self.token_inputs.append((current_name, node_list))
            else:
                self.token_outputs.append((current_name, node_list))
        elif type(node_list) == tuple:
            for current_queue in node_list:
                self.token_queues.append(current_queue)
                result.append(current_queue)
        else:
            for name in node_list:
                if type(name) != tuple:
                    node = self.get_node(name)
                    if not node:
                        q = queue.Queue(2)
                        self.token_queues.append(q)
                        result.append(q)
                    else:
                        if input_flag:
                            result.append(node.outputs[0])
                        else:
                            result.append(node.inputs[0])
                else:
                    node = self.get_node(name)
                    if not node:
                        q = queue.Queue(2)
                        self.token_queues.append(q)
                        result.append(q)
                    else:
                        k = name[-1]
                        if input_flag:
                            result.append(node.outputs[k])
                        else:
                            result.append(node.inputs[k])
        return result

    # This function is used to start to execute the data flow and set the clock.
    @arg_type(object, int)
    def execute(self, clk):
        for i in range(clk):
            for node in self.nodes:
                node.calculate()

    # This function is used to search the result of q's connection node.
    def back_queue(self, q, input_flag=True):
        res = []
        for i, n in enumerate(self.nodes):
            if input_flag:
                queues = n.inputs
            else:
                queues = n.outputs
            if q in queues:
                res.append(i)
        return res

    # This function is used to generate the connection method of each node and output them in fsm.dot
    def visualize(self):
        res = []
        res.append("digraph G {")
        res.append(" rankdir=LR;")
        for (name, q) in self.token_inputs:
            res.append(" {}[shape=rarrow];".format(name))
        for n, q in self.token_outputs:
            res.append(" {}[shape=rarrow];".format(n))
        for i, n in enumerate(self.nodes):
            res.append(' n_{}[label="{}"];'.format(i, n.name))
        for i, n in enumerate(self.nodes):
            for q in n.outputs:
                nodes_index = self.back_queue(q)
                for j in nodes_index:
                    res.append(' n_{} -> n_{};'.format(i, j))
        for name, q in self.token_inputs:
            nodes_index = self.back_queue(q)
            for i in nodes_index:
                res.append(' {} -> n_{};'.format(name, i))
        for name, q in self.token_outputs:
            nodes_index = self.back_queue(q, input_flag=False)
            for i in nodes_index:
                res.append(' n_{} -> {};'.format(i, name))
        res.append("}")
        return "\n".join(res)

    # This function is used to calculate the solution through direct calculation.
    # The res is used to compare with the result calculated in Synchronous Data Flow in test function.
    @arg_type(list)
    def quadratic(self, x):
        a = x[0]
        b = x[1]
        c = x[2]
        k = b ** 2 - 4 * a * c
        if k >= 0:
            _sqrt = math.sqrt(k)
            res = [(-b - _sqrt) / (2 * a), (-b + _sqrt) / (2 * a)]
            return res
        else:
            print('No root')

# define a Node class contain its input and output token and its function.
class Node(object):
    def __init__(self, name, function):
        self.name = name
        self.inputs = []
        self.outputs = []
        self.function = function

    def IsEmpty(self, current_queue):
        if current_queue.empty():
            return False

    # This function is used to judge whether queue is empty.
    def if_activate(self):
        for current_queue in self.inputs:
            # if self.IsEmpty(current_queue):
            if current_queue.empty():
                return False
        return True

    # This function is used to get the input from queue.
    def get_input_from_queue(self):
        if not self.inputs:
            quit()
        get_input = []
        activate_flag = self.if_activate()
        if activate_flag:
            for input_queue in self.inputs:
                get_input.append(input_queue.get())
        return get_input

    # This function is used to put the output into queue.
    def put_output_to_queue(self, out):
        if not self.outputs:
            quit()
        if not(type(out) == list):
            out = [out]
        if len(out) != len(self.outputs):
            return None
        for i, output_queue in enumerate(self.outputs):
            output_queue.put(out[i])

    # This function is used to calculate the result of the function of input.
    def calculate(self):
        get_input = self.get_input_from_queue()
        if get_input:
            output = self.function(*get_input)
            self.put_output_to_queue(output)
            return output

# This module is used to initialize nodes and graphs, then execute it and achieve visualization by GraphViz DOT.
if __name__ == "__main__":
    SDF = SDFGraph('test')
    ina = queue.Queue(2)
    inb = queue.Queue(2)
    inc = queue.Queue(2)
    ina.put(1)
    inb.put(-1)
    inc.put(-2)
    output1 = queue.Queue(2)
    output2 = queue.Queue(2)

    SDF.add_node('a', lambda x: [x, x], ina, ['2a', ('4ac', 0)])
    SDF.add_node('b', lambda x: [x, x], inb, ['b^2-4ac', ('molecular', 0)])
    SDF.add_node('d', lambda x: x, inc, [('b^2-4ac', 1)])
    SDF.add_node('2a', lambda x: [2 * x, 2 * x], [('a', 0)], [('root1', 1), ('root2', 1)])
    SDF.add_node('b^2-4ac', lambda x, a, c: x ** 2 - 4 * a * c, [('a', 1), 'c'], [('sqrt', 1)])
    SDF.add_node('sqrt', lambda x: x ** 0.5, ['b^2-4ac'], [('molecular', 1)])
    SDF.add_node('molecular', lambda x, y: [-x - y, -x + y], [('b', 1), 'sqrt'], [('root1', 0), ('root2', 0)])
    SDF.add_node('root1', lambda x, y: x / y, [('molecular', 0), ('2a', 0)], output1)
    SDF.add_node('root2', lambda x, y: x / y, [('molecular', 1), ('2a', 1)], output2)

    SDF.execute(10)

    g = SDF.visualize()
    f = open('fsm.dot', 'w')
    f.write(g)
    f.close()
    with open("fsm.dot") as f:
        dot_graph = f.read()
    dot = graphviz.Source(dot_graph)
    dot.view()