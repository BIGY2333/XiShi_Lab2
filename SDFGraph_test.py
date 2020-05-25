import unittest
import math
import random
from SDFGraph import *

class SDFGraph_test(unittest.TestCase):
    def test_SDFGraph(self):
        SDF = SDFGraph('test')
        ina = queue.Queue(2)
        inb = queue.Queue(2)
        inc = queue.Queue(2)
        output1 = queue.Queue(3)
        output2 = queue.Queue(3)

        SDF.add_node('a', lambda x: [x, x], ina, ['2a', ('4ac', 0)])
        SDF.add_node('b', lambda x: [x, x], inb, ['b^2-4ac', ('molecular', 0)])
        SDF.add_node('c', lambda x: x, inc, [('b^2-4ac', 1)])
        SDF.add_node('2a', lambda x: [2 * x, 2 * x], [('a', 0)], [('root1', 1), ('root2', 1)])
        SDF.add_node('b^2-4ac', lambda x, a, c: x**2 - 4 * a * c, [('a', 1), 'c'], [('sqrt', 1)])
        SDF.add_node('sqrt', lambda x: x**0.5, ['b^2-4ac'], [('molecular', 1)])
        SDF.add_node('molecular', lambda x, y: [-x - y, -x + y], [('b', 1), 'sqrt'], [('root1', 0), ('root2', 0)])
        SDF.add_node('root1', lambda x, y: x / y, [('molecular', 0), ('2a', 0)], output1)
        SDF.add_node('root2', lambda x, y: x / y, [('molecular', 1), ('2a', 1)], output2)

        abc = [(1, 2, 1)]
        for x in abc:
            expect = SDF.quadratic(x)
            ina.put(x[0])
            inb.put(x[1])
            inc.put(x[2])
            SDF.execute(10)
            self.assertEqual([-1.0, -1.0], expect)

class node_test(unittest.TestCase):
    def test_node_sin(self):
        f = lambda x: math.sin(x)
        node = Node('add', f)
        x = queue.Queue(10)
        y = queue.Queue(10)
        xs = [random.random() for i in range(10)]
        for k in xs:
            x.put(k)
            node.inputs = [x]
            node.outputs = [y]
            node.compute()
            self.assertEqual(y.get(), f(k))

    def test_node_add(self):
        f = lambda x: x + x
        node = Node('add', f)
        x = queue.Queue(10)
        y = queue.Queue(10)
        xs = [random.random() for i in range(10)]
        for k in xs:
            x.put(k)
            node.inputs = [x]
            node.outputs = [y]
            node.compute()
            self.assertEqual(y.get(), f(k))