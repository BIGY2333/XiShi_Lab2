import unittest
import math
import random
from SDFGraph import *
from datetime import datetime
import logging

class SDFGraph_test(unittest.TestCase):
    def test_SDFGraph(self):
        SDF = SDFGraph('test')
        begin = datetime.now().microsecond
        # ina inb and inc are represent a b and c, their type are node.
        ina = queue.Queue(2)
        inb = queue.Queue(2)
        inc = queue.Queue(2)
        # output1 and output2 are represent two roots, their type are node.
        output1 = queue.Queue(3)
        output2 = queue.Queue(3)
        end = datetime.now().microsecond
        print(end - begin)
        logging.info("The queues are set")

        begin=datetime.now().microsecond
        SDF.add_node('a', lambda x: [x, x], ina, ['2a', '4ac'])
        SDF.add_node('b', lambda x: [x, x], inb, ['b^2-4ac', 'molecular'])
        SDF.add_node('d', lambda x: x, inc, ['b^2-4ac'])
        SDF.add_node('2a', lambda x: [2 * x, 2 * x], ['a'], ['root1', 'root2'])
        SDF.add_node('b^2-4ac', lambda x, a, c: x ** 2 - 4 * a * c, ['a', 'c'], ['sqrt'])
        SDF.add_node('sqrt', lambda x: x ** 0.5, ['b^2-4ac'], ['molecular'])
        SDF.add_node('molecular', lambda x, y: [-x - y, -x + y], ['b', 'sqrt'], ['root1', 'root2'])
        SDF.add_node('root1', lambda x, y: x / y, ['molecular', '2a'], output1)
        SDF.add_node('root2', lambda x, y: x / y, ['molecular', '2a'], output2)
        end = datetime.now().microsecond
        print(end - begin)
        logging.info("The nodes are added into queue")

        begin = datetime.now().microsecond
        abc = [(1, 2, 1)]
        for x in abc:
            expect = SDF.quadratic(x)
            ina.put(x[0])
            inb.put(x[1])
            inc.put(x[2])
            SDF.execute(15)
            self.assertEqual([-1.0, -1.0], expect)
        end = datetime.now().microsecond
        print(end - begin)
        logging.info("The process is ending")

    #Dear professor,here is a SR model but I dont know how to implement it concretely  0..0
    def test_SDFGraph_SR(self):
        Q = 1
        S = 0
        R = 1
        if S:
            Q = 0
        elif R:
            Q = 1
        else:
            Q = Q
        if Q == 1:
            print("The process is starting") #do the process

    def test_SDF_with_One_Node(self):
        SDF = SDFGraph('test1')
        ina = queue.Queue(2)
        output = queue.Queue(3)
        SDF.add_node('d', lambda x: x**2, ina, output)
        d = [2]
        expect = [d[0] * d[0]]
        ina.put(d[0])
        SDF.execute(2)
        res = [output.get()]
        self.assertEqual(res, expect)

class node_test(unittest.TestCase):
    def test_node_sin(self):
        f = lambda x: math.sin(x)
        node = Node('sin', f)
        x = queue.Queue(3)
        y = queue.Queue(3)
        xs = [1, 2, 3]
        for k in xs:
            x.put(k)
            node.inputs = [x]
            node.outputs = [y]
            node.calculate()
            self.assertEqual(y.get(), f(k))

    def test_node_add(self):
        f = lambda x: x + x
        node = Node('add', f)
        x = queue.Queue(3)
        y = queue.Queue(3)
        xs = [1, 2, 3]
        for k in xs:
            x.put(k)
            node.inputs = [x]
            node.outputs = [y]
            node.calculate()
            self.assertEqual(y.get(), f(k))

if __name__ == '__main__':
    unittest.main()
