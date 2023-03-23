# machine_learning

## Neural Network Playground

[https://furyhawk.github.io/playground/](https://furyhawk.github.io/playground/)

## Residual connections

When the network get too deep, to adjust the parameters for each function in the chain based on the error(loss) recorded on the output layer, each sucessful layers include more noise. The noise start to overwhelm gradient information. This is the *vanishing gradients* problem.


## Batch normalization

The paper stated that Batch normalization operates by "reducing internal covariate shift". Helps with gradient propagation, allowing for deeper networks.

```py
# Because the output of the Conv2D layer gets normalized, the layer doesn't need its own bias vector.
x = layers.Conv2D(32,3,use_bias)(x) # do not include activation
x = layers.BatchNormalization()(x)
x = layers.Activation("relu")(x)    # place activation after BatchNormalization layer
```


### Batch normalization and Fine tuning
When fine-tuning a model that includes BatchNormalization layers, leave these layers frozen( `trainable=False`). Otherwise they will keep updating their internal mean and variance, which can interfere with the very small updates applied to the surrounding *Conv2D* layers.

## Steps per Epoch
Based on what you said it sounds like you need a larger batch_size, and of course there are implications with that which could impact the steps_per_epoch and number of epochs.

**To solve for jumping-around**

    - A **larger batch size** will give you a better gradient and will help to prevent jumping around
    - You may also want to consider a smaller learning rate, or a learning rate scheduler (or decay) to allow the network to "settle in" as it trains


## Feature Extraction

All of the models in `timm` have consistent mechanisms for obtaining various types of features from the model for tasks besides classification.

### Penultimate Layer Features (Pre-Classifier Features)

The features from the penultimate model layer can be obtained in several ways without requiring model surgery (although feel free to do surgery). One must first decide if they want pooled or un-pooled features.

#### Unpooled

There are three ways to obtain unpooled features.

Without modifying the network, one can call `model.forward_features(input)` on any model instead of the usual `model(input)`. This will bypass the head classifier and global pooling for networks.

If one wants to explicitly modify the network to return unpooled features, they can either create the model without a classifier and pooling, or remove it later. Both paths remove the parameters associated with the classifier from the network.

##### forward_features()
```python hl_lines="3 6"
import torch
import timm
m = timm.create_model('xception41', pretrained=True)
o = m(torch.randn(2, 3, 299, 299))
print(f'Original shape: {o.shape}')
o = m.forward_features(torch.randn(2, 3, 299, 299))
print(f'Unpooled shape: {o.shape}')
```
Output:
```text
Original shape: torch.Size([2, 1000])
Unpooled shape: torch.Size([2, 2048, 10, 10])
```

##### Create with no classifier and pooling
```python hl_lines="3"
import torch
import timm
m = timm.create_model('resnet50', pretrained=True, num_classes=0, global_pool='')
o = m(torch.randn(2, 3, 224, 224))
print(f'Unpooled shape: {o.shape}')
```
Output:
```text
Unpooled shape: torch.Size([2, 2048, 7, 7])
```

##### Remove it later
```python hl_lines="3 6"
import torch
import timm
m = timm.create_model('densenet121', pretrained=True)
o = m(torch.randn(2, 3, 224, 224))
print(f'Original shape: {o.shape}')
m.reset_classifier(0, '')
o = m(torch.randn(2, 3, 224, 224))
print(f'Unpooled shape: {o.shape}')
```
Output:
```text
Original shape: torch.Size([2, 1000])
Unpooled shape: torch.Size([2, 1024, 7, 7])
```

#### Pooled

To modify the network to return pooled features, one can use `forward_features()` and pool/flatten the result themselves, or modify the network like above but keep pooling intact. 

##### Create with no classifier
```python hl_lines="3"
import torch
import timm
m = timm.create_model('resnet50', pretrained=True, num_classes=0)
o = m(torch.randn(2, 3, 224, 224))
print(f'Pooled shape: {o.shape}')
```
Output:
```text
Pooled shape: torch.Size([2, 2048])
```

##### Remove it later
```python hl_lines="3 6"
import torch
import timm
m = timm.create_model('ese_vovnet19b_dw', pretrained=True)
o = m(torch.randn(2, 3, 224, 224))
print(f'Original shape: {o.shape}')
m.reset_classifier(0)
o = m(torch.randn(2, 3, 224, 224))
print(f'Pooled shape: {o.shape}')
```
Output:
```text
Original shape: torch.Size([2, 1000])
Pooled shape: torch.Size([2, 1024])
```


### Multi-scale Feature Maps (Feature Pyramid)

Object detection, segmentation, keypoint, and a variety of dense pixel tasks require access to feature maps from the backbone network at multiple scales. This is often done by modifying the original classification network. Since each network varies quite a bit in structure, it's not uncommon to see only a few backbones supported in any given obj detection or segmentation library.

`timm` allows a consistent interface for creating any of the included models as feature backbones that output feature maps for selected levels. 

A feature backbone can be created by adding the argument `features_only=True` to any `create_model` call. By default 5 strides will be output from most models (not all have that many), with the first starting at 2 (some start at 1 or 4).

#### Create a feature map extraction model
```python hl_lines="3"
import torch
import timm
m = timm.create_model('resnest26d', features_only=True, pretrained=True)
o = m(torch.randn(2, 3, 224, 224))
for x in o:
  print(x.shape)
```
Output:
```text
torch.Size([2, 64, 112, 112])
torch.Size([2, 256, 56, 56])
torch.Size([2, 512, 28, 28])
torch.Size([2, 1024, 14, 14])
torch.Size([2, 2048, 7, 7])
```

#### Query the feature information

After a feature backbone has been created, it can be queried to provide channel or resolution reduction information to the downstream heads without requiring static config or hardcoded constants. The `.feature_info` attribute is a class encapsulating the information about the feature extraction points.

```python hl_lines="3 4"
import torch
import timm
m = timm.create_model('regnety_032', features_only=True, pretrained=True)
print(f'Feature channels: {m.feature_info.channels()}')
o = m(torch.randn(2, 3, 224, 224))
for x in o:
  print(x.shape)
```
Output:
```text
Feature channels: [32, 72, 216, 576, 1512]
torch.Size([2, 32, 112, 112])
torch.Size([2, 72, 56, 56])
torch.Size([2, 216, 28, 28])
torch.Size([2, 576, 14, 14])
torch.Size([2, 1512, 7, 7])
```

#### Select specific feature levels or limit the stride

There are two additional creation arguments impacting the output features. 

* `out_indices` selects which indices to output
* `output_stride` limits the feature output stride of the network (also works in classification mode BTW)

`out_indices` is supported by all models, but not all models have the same index to feature stride mapping. Look at the code or check feature_info to compare. The out indices generally correspond to the `C(i+1)th` feature level (a `2^(i+1)` reduction). For most models, index 0 is the stride 2 features, and index 4 is stride 32.

`output_stride` is achieved by converting layers to use dilated convolutions. Doing so is not always straightforward, some networks only support `output_stride=32`.

```python hl_lines="3 4 5"
import torch
import timm
m = timm.create_model('ecaresnet101d', features_only=True, output_stride=8, out_indices=(2, 4), pretrained=True)
print(f'Feature channels: {m.feature_info.channels()}')
print(f'Feature reduction: {m.feature_info.reduction()}')
o = m(torch.randn(2, 3, 320, 320))
for x in o:
  print(x.shape)
```
Output:
```text
Feature channels: [512, 2048]
Feature reduction: [8, 8]
torch.Size([2, 512, 40, 40])
torch.Size([2, 2048, 40, 40])
```

## GloabalPooling
Reduce computation by 75%. Summarise features.

### GlobalMaxPooling
Feature extraction after covn layer.

### Use of GlobalAvgPooling
One advantage of global average pooling over the fully connected layers is that it is more native to the convolution structure by enforcing correspondences between feature maps and categories. Thus the feature maps can be easily interpreted as categories confidence maps. Another advantage is that there is no parameter to optimize in the global average pooling thus overfitting is avoided at this layer. Futhermore, global average pooling sums out the spatial information, thus it is more robust to spatial translations of the input. We can see global average pooling as a structural regularizer that explicitly enforces feature maps to be confidence maps of concepts (categories). This is made possible by the mlpconv layers, as they makes better approximation to the confidence maps than GLMs.

## How filter init
Note that we use the same weight initialization formula as with the MLP. Weights are sampled randomly from a uniform distribution in the range [-1/fan-in, 1/fan-in], where fan-in is the number of inputs to a hidden unit. For MLPs, this was the number of units in the layer below. For CNNs however, we have to take into account the number of input feature maps and the size of the receptive fields.

## Transfer Learning
In practice, very few people train an entire Convolutional Network from scratch (with random initialization), because it is relatively rare to have a dataset of sufficient size. Instead, it is common to pretrain a ConvNet on a very large dataset (e.g. ImageNet, which contains 1.2 million images with 1000 categories), and then use the ConvNet either as an initialization or a fixed feature extractor for the task of interest. The three major Transfer Learning scenarios look as follows:

- ConvNet as fixed feature extractor. Take a ConvNet pretrained on ImageNet, remove the last fully-connected layer (this layer's outputs are the 1000 class scores for a different task like ImageNet), then treat the rest of the ConvNet as a fixed feature extractor for the new dataset. In an AlexNet, this would compute a 4096-D vector for every image that contains the activations of the hidden layer immediately before the classifier. We call these features CNN codes. It is important for performance that these codes are ReLUd (i.e. thresholded at zero) if they were also thresholded during the training of the ConvNet on ImageNet (as is usually the case). Once you extract the 4096-D codes for all images, train a linear classifier (e.g. Linear SVM or Softmax classifier) for the new dataset.

- Fine-tuning the ConvNet. The second strategy is to not only replace and retrain the classifier on top of the ConvNet on the new dataset, but to also fine-tune the weights of the pretrained network by continuing the backpropagation. It is possible to fine-tune all the layers of the ConvNet, or it's possible to keep some of the earlier layers fixed (due to overfitting concerns) and only fine-tune some higher-level portion of the network. This is motivated by the observation that the earlier features of a ConvNet contain more generic features (e.g. edge detectors or color blob detectors) that should be useful to many tasks, but later layers of the ConvNet becomes progressively more specific to the details of the classes contained in the original dataset. In case of ImageNet for example, which contains many dog breeds, a significant portion of the representational power of the ConvNet may be devoted to features that are specific to differentiating between dog breeds.

### When and how to fine-tune?
How do you decide what type of transfer learning you should perform on a new dataset? This is a function of several factors, but the two most important ones are the size of the new dataset (small or big), and its similarity to the original dataset (e.g. ImageNet-like in terms of the content of images and the classes, or very different, such as microscope images). Keeping in mind that ConvNet features are more generic in early layers and more original-dataset-specific in later layers, here are some common rules of thumb for navigating the 4 major scenarios:

- New dataset is small and similar to original dataset. Since the data is small, it is not a good idea to fine-tune the ConvNet due to overfitting concerns. Since the data is similar to the original data, we expect higher-level features in the ConvNet to be relevant to this dataset as well. Hence, the best idea might be to train a linear classifier on the CNN codes.

- New dataset is large and similar to the original dataset. Since we have more data, we can have more confidence that we won't overfit if we were to try to fine-tune through the full network.

- New dataset is small but very different from the original dataset. Since the data is small, it is likely best to only train a linear classifier. Since the dataset is very different, it might not be best to train the classifier form the top of the network, which contains more dataset-specific features. Instead, it might work better to train the SVM classifier from activations somewhere earlier in the network.

- New dataset is large and very different from the original dataset. Since the dataset is very large, we may expect that we can afford to train a ConvNet from scratch. However, in practice it is very often still beneficial to initialize with weights from a pretrained model. In this case, we would have enough data and confidence to fine-tune through the entire network.

### Practical advice.
There are a few additional things to keep in mind when performing Transfer Learning:

- *Constraints from pretrained models*. Note that if you wish to use a pretrained network, you may be slightly constrained in terms of the architecture you can use for your new dataset. For example, you can't arbitrarily take out Conv layers from the pretrained network. However, some changes are straight-forward: Due to parameter sharing, you can easily run a pretrained network on images of different spatial size. This is clearly evident in the case of Conv/Pool layers because their forward function is independent of the input volume spatial size (as long as the strides "fit"). In case of FC layers, this still holds true because FC layers can be converted to a Convolutional Layer: For example, in an AlexNet, the final pooling volume before the first FC layer is of size [6x6x512]. Therefore, the FC layer looking at this volume is equivalent to having a Convolutional Layer that has receptive field size 6x6, and is applied with padding of 0.

- *Learning rates*. It's common to use a smaller learning rate for ConvNet weights that are being fine-tuned, in comparison to the (randomly-initialized) weights for the new linear classifier that computes the class scores of your new dataset. This is because we expect that the ConvNet weights are relatively good, so we don't wish to distort them too quickly and too much (especially while the new Linear Classifier above them is being trained from random initialization).

**Implications of a larger batch-size**

    - Too large of a batch_size can produce memory problems, especially if you are using a GPU. Once you exceed the limit, dial it back until it works. This will help you find the max batch-size that your system can work with.
    - Too large of a batch size can get you stuck in a local minima, so if your training get stuck, I would reduce it some. Imagine here you are over-correcting the jumping-around and it's not jumping around enough to further minimize the loss function.
**When to reduce epochs**

    - If your train error is very low, yet your test/validation is very high, then you have over-fit the model with too many epochs.
    - The best way to find the right balance is to use early-stopping with a validation test set. Here you can specify when to stop training, and save the weights for the network that gives you the best validation loss. (I highly recommend using this always)
**When to adjust steps-per-epoch**

    - Traditionally, the steps per epoch is calculated as train_length // batch_size, since this will use all of the data points, one batch size worth at a time.
    - If you are augmenting the data, then you can stretch this a tad (sometimes I multiply that function above by 2 or 3 etc. But, if it's already training for too long, then I would just stick with the traditional approach.

## When to Scale
Rule of thumb I follow here is any algorithm that computes distance or assumes normality, scale your features!!!
Some examples of algorithms where feature scaling matters are:

    - k-nearest neighbors with an Euclidean distance measure is sensitive to magnitudes and hence should be scaled for all features to weigh in equally.
	  - Scaling is critical, while performing Principal Component Analysis(PCA). PCA tries to get the features with maximum variance and the variance is high for high magnitude features. This skews the PCA towards high magnitude features.
    - We can speed up gradient descent by scaling. This is because θ will descend quickly on small ranges and slowly on large ranges, and so will oscillate inefficiently down to the optimum when the variables are very uneven.
    - Tree based models are not distance based models and can handle varying ranges of features. Hence, Scaling is not required while modelling trees.

Algorithms like Linear Discriminant Analysis(LDA), Naive Bayes are by design equipped to handle this and gives weights to the features accordingly. Performing a features scaling in these algorithms may not have much effect.

## PyTorch Loss Function Cheatsheet

PyTorch Loss-Input Confusion (Cheatsheet)

- [`torch.nn.functional.binary_cross_entropy`](https://pytorch.org/docs/stable/generated/torch.nn.functional.binary_cross_entropy.html) takes logistic sigmoid values as inputs
- [`torch.nn.functional.binary_cross_entropy_with_logits`](https://pytorch.org/docs/stable/generated/torch.nn.functional.binary_cross_entropy_with_logits.html) takes logits as inputs
- [`torch.nn.functional.cross_entropy`](https://pytorch.org/docs/stable/generated/torch.nn.functional.cross_entropy.html#torch.nn.functional.cross_entropy) takes logits as inputs (performs log_softmax internally)
- [`torch.nn.functional.nll_loss`](https://pytorch.org/docs/stable/generated/torch.nn.functional.nll_loss.html) is like `cross_entropy` but takes log-probabilities (log-softmax) values as inputs