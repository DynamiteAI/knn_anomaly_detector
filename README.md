# Dynamite K-Nearest Neighbor (K-Means)

kNN is a simple, instance-based unsupervised machine learning algorithm. kNN is a non-parametric and employs lazy-learning.

- *Non-parametric* means there is no assumption of the underlying data-distribution, meaning that the model structure is determined from the dataset.
- *Lazy-learning* implies that there is no need for a training data-points for model generation. This is because all training data is used during the testing phase.

When applied to the domain of anomaly detection kNN is a wonderful candidate, however it does come with the caveat of being somewhat costly during the testing phase (`model.predict()`)

Our implementation is fully unsupervised, meaning it does not depend on labels, and is concerned only with `X` variables.
## Algorithm Walk-through

kNN algorithm can be broken into three high-level steps.

1. Calculate distance between neighbors
2. Find closest neighbors
3. Vote for labels (normal/anomalous)


### Calculate distance between neighbors

Our implementation relies on **Manhattan Distance (Taxicab Geometry)** for determining the distance between Zeek conn.log events.

![distance](https://miro.medium.com/max/260/1*boqym__Ai1n-WxaR1X6Dhw.png)

## `p=1`

The above formula simply calculates distance by  using an absolute sum of difference between its cartesian co-ordinates

![example](https://miro.medium.com/max/197/1*7NHkUCylraQu2H-S5N1nhA.png)

We chose this heuristic because it tends to work better on high-dimensional spaces compared to the more common Euclidean distance which excels in 2 dimensional space.

#### Selected Features

| Feature       | Description                                                                                            |
|---------------|--------------------------------------------------------------------------------------------------------|
| duration      | The amount of time between the beginning and end of a connection.                                      |
| orig_bytes    | The number of bytes sent (not including header)                                                        |
| orig_ip_bytes | The number of bytes sent (including header)                                                            |
| resp_ip_bytes | The number of bytes received (including header)                                                        |
| resp_pkts     | The number of packets received                                                                         |
| id.resp_p     | The port number that the recipient is listening on (more often than not this is a common service port) |

### Finding the closest neighbors
Once kNN returns the distance to the neighboring data points we calculate k-means which will return the distance to the centroids of clusters and you will have a general representation of your clusters.

![clusters](https://miro.medium.com/max/424/1*jAsCftgneoZILh8LxUYFVQ.png)

- Closely clustered - represent your "normal"
- Loosely clustered - represents your "anomalous"

### Vote for labels (normal/anomalous)

Each object then "votes" for their class and the class with the most votes is taken as the prediction. 

## Lessons Learned
- Limit the dimensionality of your data, kNN can be very computationally expensive during the testing (prediction) phase. kNN performed significantly slower when additional features were introduced.
- Choose your features wisely. The algorithm is only as good as the data we "train" it on. We intentionally chose features that describe an application protocols "behaviors".
- This algorithm missed several events that, based on our criteria, were anomalous. For best results this algorithm should be used alongside other anomaly detectors which can help cut down on false-positives and false negatives.
