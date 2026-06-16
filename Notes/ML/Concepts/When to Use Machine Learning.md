---
tags: [ml, decision-framework]
parent: "[[MOCs/ML & Data Science Packages -- Map of Content]]"
created: 2026-06-15
status: complete
---

1. Learn: the system has the capacity to learn
2. Complex patterns: there are patterns to learn, and they are complex
3. Existing data: data is available, or it's possible to collect data
4. Predictions: it's a predictive problem
5. Unseen data: unseen data shares patterns with the training data
6. It's repetitive
7. The cost of wrong predictions is cheap
8. It's At scale: *making a lot of predictions*
9. The patterns are constantly changing

### Machine Learning & it's quirks
- When designing an ML system, people who haven't deployed an ML system often make the mistake of focusing too much on the model development part and not enough on the model deployment and maintenance part. 
-  The struggle btw latency vs throughput; prod vs model development 


##### Chapter 2
**Objective Functions**
- This is one of the biggest ideas in the chapter: ML systems optimize whatever metric you give them, not whatever intention you had in your head. Humans often assume those are the same thing. They rarely are.
- The solution isn't finding a perfect objective function. The uncomfortable reality is that perfect objective functions rarely exist. The solution is accepting that every metric is a proxy, then designing systems that compensate for the proxy's weaknesses.

> [!note]
> The architecture tells the model what it can learn, the data tells it what is available to learn, and the objective function tells it what learning is considered good
## Apendix
- [InterpretML](https://github.com/interpretml/interpret)
- 
