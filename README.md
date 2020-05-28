# Computational Process Organization - Lab2
*Yao_Wangze  Sun_wei*

*laboratory work number ———— 4*

*variant description： eDSL for synchronous dataﬂow. 
						Node synchronous consume a single token on each input and produce a single token on each output. 
						Visualization by GraphViz DOT. 
						Should provide complex examples such as a quadratic formula. *

## Synopsis ##
In this lab,we should design an input language for building computational process description; We should design interpreter, which allows library user to execute a computational process description;We should achieve an interpreter for computational process models.

## Contribution summary for each group member ##

Yaowangze's contribution：Analyze the principle and be responsible for implementing part of the code.

Sunwei's contribution：Analyze the principle and be responsible for implementing part of the code.

## Explanation of taken design decisions and analysis ##
1. We define a class named SDFGraph and a class named Node.The former class is used to define a Synchronous Data Flow(SDF) class.
	Its initialization name means the object's name, list token_inputs and token_outputs means its literal meaning, list nodes means the set of all nodes.
	The latter class is used to define a Node class contain its input and output token and its function.
	Its initialization name means the node's name,list inputs and outputs means a node that connects it,list function means the function the node effects.
2. Secondly, we add all nodes to nodes list and  put the output token and input token into queue.They are used to calculate the solution of quadratic formula.
3. Thirdly, we traverse all nodes in list nodes, we calculate the function effected it and we also record their input and output,then we put them into a queue so that the relationship between nodes are recorded.

3.1  detail steps：Because we want to calculate the solution of quadratic formula,so we nead a, b and c.As we all know, the solution equals (-b±sqrt(b^2-4ac))/(2a),so we need set the following node:a,b,c,2a,-b,b^2-4ac.Then we connect node a to node 2a and node b^2-4ac, node b to node b^2-4ac and node molecular,node c to node b^2-4ac.Every node's token are put into queue at the same time.Then it starts calculate after function calculate() works.The node is got from queue and execute the function when afferent.After it, the output will be push into a queue to record.After traverse all nodes, the calculation process will stop.Meanwhile, the results are record.
4. Fourthly, we traverse all values in the queue and output them in 'fsm.dot' and achieve visualization by GraphViz DOT.
5. Fifthly, we write a set of decorators which allows checking the type and values of input data.
6. Finally, we test the features by the test function named SDFGraph_test.

## Operation result ##
![Alt text](/fig/fsm.png)

![Alt text](/fig/visualization.png)
## Conclusion ##
The synchronous dataﬂow is achieved through the tokens.And we can design an input language for building computational process description; We can design interpreter, which allows library user to execute a computational process description;We can achieve an interpreter for computational process models. 