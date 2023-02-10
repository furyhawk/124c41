# Framework

## Pytorch vs Tensorflow
The image range is different for each framework. In PyTorch, the image range is 0-1 while TensorFlow uses a range from 0 to 255. To use TensorFlow, we have to adapt the image range.

## To TF

```py
def dataset_to_tf(
    dataset,
    cols_to_retain,
    collate_fn,
    collate_fn_args,
    columns_to_np_types,
    output_signature,
    shuffle,
    batch_size,
    drop_remainder,
):
    """Create a tf.data.Dataset from the underlying Dataset. This is a single-process method - the multiprocess
    equivalent is multiprocess_dataset_to_tf.

            Args:
                dataset (`Dataset`): Dataset to wrap with tf.data.Dataset.
                cols_to_retain (`List[str]`): Dataset column(s) to load in the
                    tf.data.Dataset. It is acceptable to include column names that are created by the `collate_fn` and
                    that do not exist in the original dataset.
                collate_fn(`Callable`): A function or callable object (such as a `DataCollator`) that will collate
                    lists of samples into a batch.
                collate_fn_args (`Dict`): A  `dict` of keyword arguments to be passed to the
                    `collate_fn`. Can be empty.
                columns_to_np_types (`Dict[str, np.dtype]`): A `dict` mapping column names to numpy dtypes.
                output_signature (`Dict[str, tf.TensorSpec]`): A `dict` mapping column names to
                    `tf.TensorSpec` objects.
                shuffle(`bool`): Shuffle the dataset order when loading. Recommended True for training, False for
                    validation/evaluation.
                batch_size (`int`): Size of batches to load from the dataset.
                drop_remainder(`bool`, default `None`): Drop the last incomplete batch when loading. If not provided,
                    defaults to the same setting as shuffle.

            Returns:
                `tf.data.Dataset`
    """
    if config.TF_AVAILABLE:
        import tensorflow as tf
    else:
        raise ImportError("Called a Tensorflow-specific function but Tensorflow is not installed.")

    getter_fn = partial(
        np_get_batch,
        dataset=dataset,
        cols_to_retain=cols_to_retain,
        collate_fn=collate_fn,
        collate_fn_args=collate_fn_args,
        columns_to_np_types=columns_to_np_types,
        return_dict=False,  # TF expects numpy_function to return a list and will not accept a dict
    )

    @tf.function(input_signature=[tf.TensorSpec(None, tf.int64)])
    def fetch_function(indices):
        output = tf.numpy_function(
            getter_fn,
            inp=[indices],
            # This works because dictionaries always output in the same order
            Tout=[tf.dtypes.as_dtype(dtype) for dtype in columns_to_np_types.values()],
        )
        return {key: output[i] for i, key in enumerate(columns_to_np_types.keys())}

    tf_dataset = tf.data.Dataset.from_tensor_slices(np.arange(len(dataset), dtype=np.int64))

    if shuffle:
        tf_dataset = tf_dataset.shuffle(len(dataset))

    tf_dataset = tf_dataset.batch(batch_size, drop_remainder=drop_remainder).map(fetch_function)

    def ensure_shapes(input_dict):
        return {key: tf.ensure_shape(val, output_signature[key].shape) for key, val in input_dict.items()}

    return tf_dataset.map(ensure_shapes)

```

```py
import tensorflow as tf
import torch

# Assume that we have a PyTorch Dataset object called 'dataset'

def pytorch_dataset_to_tensorflow_dataset(dataset):
  def generator():
    for data in dataset:
      # Convert data from PyTorch tensors to TensorFlow tensors
      data = [tf.convert_to_tensor(x) for x in data]
      yield data

  # Create a TensorFlow Dataset from the generator
  dataset = tf.data.Dataset.from_generator(generator, output_types=data[0].dtype, output_shapes=data[0].shape)

  return dataset

# Create a TensorFlow Dataset from the PyTorch Dataset
dataset = pytorch_dataset_to_tensorflow_dataset(dataset)

# Create a TensorFlow DataLoader from the TensorFlow Dataset
dataloader = tf.data.DataLoader(dataset, batch_size=32, num_parallel_calls=tf.data.AUTOTUNE)

```

Releases
tensorflow-macos	tensorflow-metal	macOS version	Features
v2.5	0.1.2	12.0+	Pluggable device
v2.6	0.2.0	12.0+	Variable sequences for RNN layers
v2.7	0.3.0	12.0+	Custom op support
v2.8	0.4.0	12.0+	RNN performance improvements
v2.9	0.5.0	12.1+	Distributed training

```py
image = tf.io.read_file(filename=filepath)
image = tf.image.decode_jpeg(image, channels=3) #or decode_png
```
the opposite of `unsqueeze` and `squeeze` is `expand_dims`:
```py
img = tf.expand_dims(img,axis=0)
```

yield the desired/necessary transformations.

As for the photos, I am quite sure that you missed a /255.0 in case of PyTorch or added a 255.0 division in case of TensorFlow.

In fact, when digging deep into the Keras backend, you can see that when you call your preprocessing function, it will call this function here:

```py
def _preprocess_numpy_input(x, data_format, mode):
  """Preprocesses a Numpy array encoding a batch of images.

  Arguments:
    x: Input array, 3D or 4D.
    data_format: Data format of the image array.
    mode: One of "caffe", "tf" or "torch".
      - caffe: will convert the images from RGB to BGR,
          then will zero-center each color channel with
          respect to the ImageNet dataset,
          without scaling.
      - tf: will scale pixels between -1 and 1,
          sample-wise.
      - torch: will scale pixels between 0 and 1 and then
          will normalize each channel with respect to the
          ImageNet dataset.

  Returns:
      Preprocessed Numpy array.
  """
  if not issubclass(x.dtype.type, np.floating):
    x = x.astype(backend.floatx(), copy=False)

  if mode == 'tf':
    x /= 127.5
    x -= 1.
    return x
  elif mode == 'torch':
    x /= 255.
    mean = [0.485, 0.456, 0.406]
    std = [0.229, 0.224, 0.225]
  else:
    if data_format == 'channels_first':
      # 'RGB'->'BGR'
      if x.ndim == 3:
        x = x[::-1, ...]
      else:
        x = x[:, ::-1, ...]
    else:
      # 'RGB'->'BGR'
      x = x[..., ::-1]
    mean = [103.939, 116.779, 123.68]
    std = None

  # Zero-center by mean pixel
  if data_format == 'channels_first':
    if x.ndim == 3:
      x[0, :, :] -= mean[0]
      x[1, :, :] -= mean[1]
      x[2, :, :] -= mean[2]
      if std is not None:
        x[0, :, :] /= std[0]
        x[1, :, :] /= std[1]
        x[2, :, :] /= std[2]
    else:
      x[:, 0, :, :] -= mean[0]
      x[:, 1, :, :] -= mean[1]
      x[:, 2, :, :] -= mean[2]
      if std is not None:
        x[:, 0, :, :] /= std[0]
        x[:, 1, :, :] /= std[1]
        x[:, 2, :, :] /= std[2]
  else:
    x[..., 0] -= mean[0]
    x[..., 1] -= mean[1]
    x[..., 2] -= mean[2]
    if std is not None:
      x[..., 0] /= std[0]
      x[..., 1] /= std[1]
      x[..., 2] /= std[2]
  return x
```

### mean and std

```py
mean = 0.0
std = 0.0
for images, _ in dl:
    batch_samples = images.size(0)  # batch size (the last batch can have smaller size!)
    images = images.view(batch_samples, images.size(1), -1)
    mean += images.mean(2).sum(0)
    std += images.std(2).sum(0)

mean /= len(dl.dataset)
std /= len(dl.dataset)

```

