# anomaly_detection

## Deep Learning for Anomaly Detection: A survey

1901.03407.pdf (arxiv.org) https://arxiv.org/pdf/1901.03407.pdf

### Type of Anomaly

- Point Anomalies

    - represent an irregularity or deviation that happens randomly and may have no particular interpretation.

- Contextual Anomaly Detection

    - conditional anomaly is a data instance that could be considered as anomalous in some specific context.

    - Contextual anomaly is identified by considering both contextual and behavioural features. The contextual features, normally used are time and space. While the behavioral features may be a pattern of spending money, the occurrence of system log events or any feature used to describe the normal behavior.

- Collective or Group Anomaly Detection.

    - Anomalous collections of individual data points are known as collective or group anomalies, wherein each of the individual points in isolation appears as normal data instances while observed in a group exhibit unusual characteristics.

- Output of DAD Techniques

    - Anomaly Score

    - Labels

## Diversity-Measurable Anomaly Detection | Papers With Code
https://paperswithcode.com/paper/diversity-measurable-anomaly-detection

Improvement of Autoencoders and Generative Adversarial Networks.

**Limitations**. Focuses on anomaly with measurable geometrical diversity, the most common type in anomaly detection. However, as for anomaly with other kind of diversities, e.g. colors, the proposed diversity measure may not be positively correlated to anomaly severity.

## Attribute-based Representations for Accurate and Interpretable Video Anomaly Detection | Papers With Code
https://paperswithcode.com/paper/attribute-based-representations-for-accurate

- Video anomaly detection

- Use object detection to extract features:

    - Velocity

    - Pose

    - Deep features(pre-trained CLIP)

- Use kNN to detect anomaly on the extracted features.

Could use similar approach to extract detective features.

## DSR -- A dual subspace re-projection network for surface anomaly detection | Papers With Code

https://paperswithcode.com/paper/dsr-a-dual-subspace-re-projection-network-for

Proposes an architecture based on quantized feature space representation with dual decoders, DSR, that avoids the image-level anomaly synthesis requirement. Without making any assumptions about the visual properties of anomalies, DSR generates the anomalies at the feature level by sampling the learned quantized feature space, which allows a controlled generation of near-in-distribution anomalies.