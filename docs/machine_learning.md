# machine_learning

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

**Implications of a larger batch-size**

    - Too large of a batch_size can produce memory problems, especially if you are using a GPU. Once you exceed the limit, dial it back until it works. This will help you find the max batch-size that your system can work with.
    - Too large of a batch size can get you stuck in a local minima, so if your training get stuck, I would reduce it some. Imagine here you are over-correcting the jumping-around and it's not jumping around enough to further minimize the loss function.
**When to reduce epochs**

    - If your train error is very low, yet your test/validation is very high, then you have over-fit the model with too many epochs.
    - The best way to find the right balance is to use early-stopping with a validation test set. Here you can specify when to stop training, and save the weights for the network that gives you the best validation loss. (I highly recommend using this always)
**When to adjust steps-per-epoch**

    - Traditionally, the steps per epoch is calculated as train_length // batch_size, since this will use all of the data points, one batch size worth at a time.
    - If you are augmenting the data, then you can stretch this a tad (sometimes I multiply that function above by 2 or 3 etc. But, if it's already training for too long, then I would just stick with the traditional approach.
