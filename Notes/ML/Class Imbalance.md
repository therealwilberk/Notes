Class Imbalance

> [!note]
> The simplest mental model is this: recall measures how many real positives you captured, precision measures how trustworthy your positive predictions are, F1 measures the balance between those two, and ROC/AUC measures how well the model separates classes across all possible thresholds. Recall cares about missing positives. Precision cares about false alarms. F1 cares about both simultaneously. ROC cares about the classifier's ranking ability before you even choose a threshold.


$$
Precision = True Positive / (True Positive + False Positive)
$$
$$
Recall = True Positive / (True Positive + False Negative)
$$
$$
F1 = 2 × Precision × Recall / (Precision + Recall)
$$

- The area under the curve (AUC) measures the area under the ROC curve. Since
the closer to the perfect line the better, the larger this area the better

> [!Sampling]
> Sampling is not always the correct solution. Tree-based models such as Random Forests and Gradient Boosted Trees often handle moderate imbalance reasonably well. In many cases, adjusting class weights is more effective than modifying the dataset itself. A classifier can be instructed that misclassifying a fraud case is 20 times more costly than misclassifying a legitimate transaction. The model then naturally pays more attention to minority examples during training.
>
- Sampling techniques exist to address imbalance. The simplest approach is *undersampling*, where examples from the majority class are removed until the classes become more balanced.
- The opposite approach is *oversampling*. Instead of removing majority examples, minority examples are duplicated.
- **SMOTE** (Synthetic Minority Oversampling Technique) was developed to solve this problem. Rather than duplicating minority examples, SMOTE generates entirely new synthetic samples. It examines a minority-class observation, finds nearby minority neighbors, and creates new samples along the line connecting them


---
- [How to work wiith Class imbalance notebook](https://www.kaggle.com/code/rafjaa/resampling-strategies-for-imbalanced-datasets/notebook)

