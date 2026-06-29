# After 80 Years, Mathematicians Give Famed ‘Erdős Method’ an Upgrade

**Source:** Quanta  
**Author:** Leila Sloman  
**Date:** 2026-06-26  
**Link:** https://www.quantamagazine.org/after-80-years-mathematicians-give-famed-erdos-method-an-upgrade-20260626/

---

In 1947, Paul Erdős, the itinerant Hungarian mathematician, introduced what would become one of math’s most powerful tools. He wanted to prove that a certain kind of object existed — in this case, a network made of interconnected nodes. But strangely, his proof didn’t specify how to build it. Instead, he showed that if you consider all networks and select one at random, the chances that you’ll find a network with the property you want is greater than zero. That means that the desired network is out there somewhere, even if you know almost nothing about it.

Erdős’ approach, known as the probabilistic method, was simple but revolutionary. Before its development, “if I’m telling you that certain objects exist, you would tell me, ‘Show me,’” said [Benny Sudakov](https://people.math.ethz.ch/~sudakovb/), a mathematician at the Swiss Federal Institute of Technology Zurich. “But certain objects are so unusual that it’s hard for us to grasp that they exist at all.”

Erdős’ technique overcame this difficulty, demonstrating that randomness could be used in ways mathematicians had never imagined. “It was just astounding that you would use randomness,” said [Joel Spencer](https://cs.nyu.edu/~spencer/) of New York University. “Now, that’s the baseline.”

Today, the probabilistic method is used across mathematics and computer science — to figure out if a number is prime, to design better circuits, or to clean up data without introducing biases.

Researchers have strengthened the technique in various ways. But the original focus of the probabilistic method — the question about networks that Erdős sought to answer — has seen very little progress. For eight decades, mathematicians were unable to significantly improve on the solution that Erdős came up with.

That’s now finally starting to change.

## **A Voice in the Wilderness**

Imagine a network of nodes — a graph — in which every pair of nodes is connected by an edge.

Mark Belan/_Quanta Magazine_

Now color each edge either red or blue, but with one caveat: Don’t create any large clusters of nodes that are all connected by edges of the same color. These forbidden structures are called monochromatic cliques. Here’s a monochromatic clique consisting of three nodes, which mathematicians call a clique of size 3:

If your graph has enough nodes, it will be impossible to avoid creating a monochromatic clique, no matter how you color the edges. For instance, if you want to avoid a clique of size 3, your graph can have at most five nodes. A six-node graph will always have one:

Mathematicians therefore say that the “Ramsey number” for a clique of size 3, denoted _R_(3), is 6. Ramsey numbers measure how big graphs can get before the forbidden pattern inevitably emerges.

You can also have Ramsey numbers for red and blue cliques of different sizes. For example, you can color an eight-node graph so that it has no red cliques of size 3 or blue cliques of size 4. But if you add one more node to your graph, you will be forced to create at least one red or blue clique. Therefore, the Ramsey number _R_(3, 4) is 9.

As the cliques you want to avoid get bigger, the problem gets more and more difficult to solve. Mathematicians have been able to calculate only a handful of the smallest Ramsey numbers. “It’s very hard to create something that has no structure,” said [Paul Horn](https://science.du.edu/about/faculty-directory/paul-horn) of the University of Denver. “Maybe it’s because we’re human and we’re subject to our biases.”

And so mathematicians have spent decades trying to find better and better approximations of Ramsey numbers. That’s what Erdős was trying to do when he introduced his probabilistic method in 1947. Instead of building clique-free graphs directly, he considered every possible way to color a graph, then showed that at least some nonzero fraction of them must be clique-free.

Erdős used this argument to prove that, if you forbid red and blue cliques of size _k_ , the Ramsey number _R_(_k_) must be bigger than $latex \sqrt{2}^k$. Ramsey numbers for same-size red and blue cliques are called diagonal Ramsey numbers. Erdős could similarly get a lower bound on “off-diagonal” Ramsey numbers _R_(_k_ , _l_), in which you forbid red cliques of size _k_ and blue cliques of size _l_.

The proof was just a few lines long. But it was completely unexpected.

At first, mathematicians were loath to follow his lead. They wanted concrete examples. “For many years, Erdős was like a voice in the wilderness,” Spencer said. “He was getting these amazing results using randomness, and people had never done that before.”

But soon the probabilistic method proved its worth. It’s now one of the most ubiquitous techniques in “discrete” math, the study of objects (like graphs) that are separate rather than continuous. And it has seeped out of math into physics and [computer science](https://www.quantamagazine.org/how-randomness-improves-algorithms-20230403/). “The randomness, I think, just helps us get at something that is otherwise very ethereal,” Horn said.

More recently, mathematicians have been able to adapt Erdős’ method to get better estimates of Ramsey numbers where the forbidden cliques [differ vastly in size](https://www.quantamagazine.org/mathematicians-discover-new-way-to-predict-structure-in-graphs-20230622/). For instance, in 2025 Horn and three colleagues used an updated version of Erdős’ method to prove a more precise [lower bound for _R_(3, _l_)](https://arxiv.org/abs/2510.19718), where _l_ grows arbitrarily large. (That work, in turn, led to [a major breakthrough](https://arxiv.org/abs/2512.20392) in graph theory.)

Paul Erdős figured out how to use randomness to prove that certain mathematical objects exist, even if you don’t know how to construct them. His technique, today known as the probabilistic method, transformed many branches of math and computer science.

Archives of the Mathematisches Forschungsinstitut Oberwolfach ©Gabriella Bollobas

But when it came to Ramsey numbers where the forbidden cliques weren’t so different in size — particularly diagonal Ramsey numbers, the object of Erdős’ original interest — the probabilistic method stalled. Say you forbid cliques of size 1,000. Erdős showed that _R_(1,000) must be bigger than about 2500. Eight decades of effort changed that bound to about 2501. Similarly, from the 1970s onward, progress remained stock-still for off-diagonal Ramsey numbers where the forbidden red and blue cliques are both relatively large.

Then along came a graduate student with barely any expertise in Ramsey theory.

## **Correlated Coloring**

Wujie Shen had spent his first few semesters at Tsinghua University focused mainly on geometry and topology. But in the spring of 2024, he came across [a paper on Ramsey numbers](https://annals.math.princeton.edu/2024/199-2/p08) that captivated him.

He knew how Erdős’ method worked: You flip a coin to determine the color of each edge of your graph: Heads, the edge is red; tails, it’s blue. You then calculate the probability that you’ll get a clique-free coloring. But this calculation gets very difficult for larger graphs. Shen wondered whether there was a random model that could produce clique-free colorings more efficiently than Erdős’ approach.

Given Shen’s training, it’s perhaps no surprise that the model he came up with involved geometry. Typically, graph colorings don’t invoke geometry: All that matters to mathematicians is which nodes are connected by a red edge, and which are connected by a blue one. Whether those nodes sit close together or are scattered throughout space has no significance.

But Shen wanted to use geometry to help him decide which edges to color red and which to color blue. In particular, he wanted to use the geometry of high-dimensional spheres — that is, sets of points that are equidistant from a single central point.

These spheres “mess with all our intuitions completely,” said [David Conlon](https://www.its.caltech.edu/~dconlon/) of the California Institute of Technology. Many of our assumptions about what a sphere looks like are no longer true in high dimensions: A high-dimensional sphere has a tiny volume and massive surface area, and most of its points lie on the equator. It’s “pretty complicated to work with,” Sudakov said.

But Shen and two colleagues — [Jie Ma](http://staff.ustc.edu.cn/~jiema/), who was visiting Tsinghua to teach for the fall term, and Ma’s graduate student Shengjie Xie — wanted to try. Their method: First, place nodes one by one onto the surface of a high-dimensional sphere. Choose each node’s position at random — any point on the sphere is fair game, and the placement of each node has no influence over the placement of any other node.

Once you’ve placed all the nodes, color each edge based on the distance between the nodes. If two points are more than some fixed distance apart (which will happen with a probability of less than 1/2), color the edge connecting them red. If they’re closer together, color the edge blue.

From left/top: Jie Ma, Wujie Shen, and Shengjie Xie used the strange geometry of high-dimensional spheres to make progress on a problem that had been stalled for decades.

From left/top: Courtesy of Jie Ma; Courtesy of Wujie Shen; Ziyuan Zhao

With this approach, the graphs that Ma, Shen, and Xie created were less likely to form a red clique. That’s because to form a large red clique, you need many nodes that are all far away from one another. With only so much space on the sphere, this is unlikely to happen.

But there’s a catch. By the same token, this method also produces a greater fraction of colorings that have blue cliques than Erdős’ does. “There’s a trade-off that looks like it really helps in one color, but it doesn’t help at all in the other color,” Conlon said. “Why bother?”

Even so, Ma, Shen, and Xie were hopeful. They tested their method on smaller graphs, and it seemed to work: Among the tens of thousands of bad colorings it generated, there was still a nonzero chance of getting a good clique-free coloring as well. That reassured them that the benefits could outweigh the costs, even for much bigger graphs.

They then set out to prove it. The key turned out to be the very weird geometry of high-dimensional spheres.

Ultimately, to show that they could avoid cliques of a particular size, Ma, Shen, and Xie needed to limit the probability that their randomly placed nodes formed clusters that were all far apart, or all close together. They realized that if they drew lines from each node to the sphere’s center, those lines would almost all be perpendicular or close to perpendicular. That doesn’t happen if you randomly place nodes on a familiar two-dimensional sphere: Most nodes will not lie on perpendicular lines. But the team was able to prove that it was true in the much higher dimensions that they were working in.

That, in turn, restricted how far nodes could be from one another — thereby limiting their chances of forming a monochromatic clique.

After a year and 40 pages of dense computations, the trio [posted their paper](https://arxiv.org/abs/2507.12926) in July 2025. They’d improved Erdős’ lower bound on Ramsey numbers — but only when the forbidden blue cliques are larger than the red ones. When the blue cliques are just as small as the red ones, the benefits of the new approach disappear.

Still, when you want to avoid red cliques that are, say, half as large as blue ones, Ma, Shen, and Xie managed to nudge Erdős’ growth rate of $latex ((\sqrt{5} + 1)/2)^k$ up to $latex ((\sqrt{5} + 1)/2 + 10^{-21})^k$. While the change is tiny, their proof marks the first improvement for near-diagonal Ramsey numbers in 50 years.

“It’s lucky, and we feel like all our efforts are rewarded,” Ma said. “But it was tough for a long time.”

“It’s a bit shocking that a familiar thing works for a familiar problem,” said [Julian Sahasrabudhe](https://www.dpmms.cam.ac.uk/~jdrs2/) of the University of Cambridge. Their technique, he said, “was hidden in plain view.”

## **The Probabilistic Playground**

Ma, Shen, and Xie’s proof has already generated a spate of further progress. In December 2025, Sudakov and two of his graduate students [drastically simplified the team’s coloring model](https://arxiv.org/abs/2512.17718), improving their new bounds even further. Others have since used the model [to estimate Ramsey numbers](https://arxiv.org/abs/2601.15183) that involve three colors, not two.

That’s in keeping with the probabilistic method’s long history. For the past 80 years, mathematicians have been tinkering with Erdős’ randomness-based technique, finding more and more ways to mix in additional structure to boost its power. Inevitably, these new techniques have then proved useful elsewhere. “It’s a very fruitful playground for ideas,” Sudakov said.

Ma, Shen, and Xie’s work, then, is the latest chapter in this decades-old story. But it’s also the first one in a long time to revisit the near-diagonal Ramsey numbers.

The team’s new contribution — a geometric approach — might lead to more progress on that stubborn problem. Although the probabilistic method hasn’t been perfected yet, “it’s really very powerful now,” Spencer said. “It’s really changed so much.”
