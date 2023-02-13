# Framework

## Pytorch vs Tensorflow

The image range is different for each framework. In PyTorch, the image range is 0-1 while TensorFlow uses a range from 0 to 255. To use TensorFlow, we have to adapt the image range.

### To TF

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

### pytorch dataset to tf dataset

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

```py
image = tf.io.read_file(filename=filepath)
image = tf.image.decode_jpeg(image, channels=3) #or decode_png
```

The opposite of `unsqueeze` and `squeeze` is `expand_dims`:

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

## mean and std

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

## DataGenerator(keras.utils.Sequence):
```py
import numpy as np
import keras

class DataGenerator(keras.utils.Sequence):
    'Generates data for Keras'
    def __init__(self, list_IDs, labels, batch_size=32, dim=(32,32,32), n_channels=1,
                 n_classes=10, shuffle=True):
        'Initialization'
        self.dim = dim
        self.batch_size = batch_size
        self.labels = labels
        self.list_IDs = list_IDs
        self.n_channels = n_channels
        self.n_classes = n_classes
        self.shuffle = shuffle
        self.on_epoch_end()

    def __len__(self):
        'Denotes the number of batches per epoch'
        return int(np.floor(len(self.list_IDs) / self.batch_size))

    def __getitem__(self, index):
        'Generate one batch of data'
        # Generate indexes of the batch
        indexes = self.indexes[index*self.batch_size:(index+1)*self.batch_size]

        # Find list of IDs
        list_IDs_temp = [self.list_IDs[k] for k in indexes]

        # Generate data
        X, y = self.__data_generation(list_IDs_temp)

        return X, y

    def on_epoch_end(self):
        'Updates indexes after each epoch'
        self.indexes = np.arange(len(self.list_IDs))
        if self.shuffle == True:
            np.random.shuffle(self.indexes)

    def __data_generation(self, list_IDs_temp):
        'Generates data containing batch_size samples' # X : (n_samples, *dim, n_channels)
        # Initialization
        X = np.empty((self.batch_size, *self.dim, self.n_channels))
        y = np.empty((self.batch_size), dtype=int)

        # Generate data
        for i, ID in enumerate(list_IDs_temp):
            # Store sample
            X[i,] = np.load('data/' + ID + '.npy')

            # Store class
            y[i] = self.labels[ID]

        return X, keras.utils.to_categorical(y, num_classes=self.n_classes)
```

```py
class ImageDataGenerator(tf.keras.preprocessing.image.ImageDataGenerator):
    def __init__(self):
        super().__init__(
            rescale=1.0 / 255.0,
            rotation_range=10,
            width_shift_range=0.2,
            height_shift_range=0.2,
            zoom_range=[0.95, 1.05],
            shear_range=0.1,
            fill_mode="wrap",
            horizontal_flip=True,
            vertical_flip=True,
        )


class Generator(object):
    def __init__(self, batch_size, name_x, name_y):

        data_f = None  # h5py.File(open_directory, "r")

        self.x = data_f[name_x]
        self.y = data_f[name_y]

        if len(self.x.shape) == 4:
            self.shape_x = (None, self.x.shape[1], self.x.shape[2], self.x.shape[3])

        if len(self.x.shape) == 3:
            self.shape_x = (None, self.x.shape[1], self.x.shape[2])

        if len(self.y.shape) == 4:
            self.shape_y = (None, self.y.shape[1], self.y.shape[2], self.y.shape[3])

        if len(self.y.shape) == 3:
            self.shape_y = (None, self.y.shape[1], self.y.shape[2])

        self.num_samples = self.x.shape[0]
        self.batch_size = batch_size
        self.epoch_size = self.num_samples // self.batch_size + 1 * (
            self.num_samples % self.batch_size != 0
        )

        self.pointer = 0
        self.sample_nums = np.arange(0, self.num_samples)
        np.random.shuffle(self.sample_nums)

    def data_generator(self):

        for batch_num in range(self.epoch_size):

            x = []
            y = []

            for elem_num in range(self.batch_size):

                sample_num = self.sample_nums[self.pointer]

                x += [self.x[sample_num]]
                y += [self.y[sample_num]]

                self.pointer += 1

                if self.pointer == self.num_samples:
                    self.pointer = 0
                    np.random.shuffle(self.sample_nums)
                    break

            x = np.array(x, dtype=np.float32)
            y = np.array(y, dtype=np.float32)

            yield x, y

    def get_dataset(self):
        dataset = tf.data.Dataset.from_generator(
            self.data_generator,
            output_signature=(
                tf.TensorSpec(shape=(), dtype=tf.int32),
                tf.RaggedTensorSpec(shape=(2, None), dtype=tf.int32),
            ),
        )
        dataset = dataset.prefetch(1)

        return dataset
```

```py
def _load_image(self, image_path):
        image = cv2.imread(image_path)  # BGR
        # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # image = tf.io.read_file(image_path)
        # image = tf.io.decode_image(
        #     image,
        #     channels=self.num_channels,
        #     dtype=tf.dtypes.uint8,
        #     expand_animations=False,
        # )
        # image = tf.image.resize(
        #     image,
        #     self.dim,
        #     method=tf.image.ResizeMethod.BILINEAR,
        #     preserve_aspect_ratio=True,
        #     antialias=False,
        #     name=None,
        # )
        # if not issubclass(image.dtype.type, np.floating):
        image = image.astype(np.float32)
        # image = image.astype(tf.keras.backend.floatx(), copy=False)
        image = self.apply_image_transforms(image)
        # 'RGB'->'BGR'
        # image = image[..., ::-1]
        # image = tf.image.convert_image_dtype(image, dtype=tf.uint8, saturate=False)
        # image = tf.cast(image, tf.float32)  # / 127.5
        # image -= 1.0
        mean = [103.939, 116.779, 123.68]
        # mean_tensor = tf.keras.backend.constant(-np.array(mean))
        # if tf.keras.backend.dtype(image) != tf.keras.backend.dtype(mean_tensor):
        #     image = tf.keras.backend.bias_add(
        #         image,
        #         tf.keras.backend.cast(mean_tensor, tf.keras.backend.dtype(image)),
        #         data_format="channels_last",
        #     )
        # else:
        #     image = tf.keras.backend.bias_add(image, mean_tensor, "channels_last")
        # image[0, :, :] -= mean[0]
        # image[1, :, :] -= mean[1]
        # image[2, :, :] -= mean[2]
        image[..., 0] -= mean[0]
        image[..., 1] -= mean[1]
        image[..., 2] -= mean[2]
        # image = tf.keras.applications.vgg16.preprocess_input(image)
        """ Preprocessed numpy.array or a tf.Tensor with type float32. The images are converted from RGB to BGR,
            then each color channel is zero-centered with respect to the ImageNet dataset, without scaling. """
        return image
```


## Unfreeze specific layers
Here is one way to **unfreeze** specific layers. We pick the same model and some layers (e.g. `block14_sepconv2`). The purpose is to **unfreeze** these layers and make the rest of the layers **freeze**.
```py
from tensorflow import keras

base_model = keras.applications.Xception(
    weights='imagenet',
    input_shape=(150,150,3),
    include_top=False
)

# free all layer except the desired layers
# which is in [ ... ]
for layer in base_model.layers:
    if layer.name not in ['block14_sepconv2', 'block13_sepconv1']:
        layer.trainable = False
    
    if layer.trainable:
        print(layer.name)

block14_sepconv2
block13_sepconv1
```

## Compute the trainable and non-trainable variables.
```py
import tensorflow.keras.backend as K
import numpy as np 

trainable_count = np.sum([K.count_params(w) \
                          for w in base_model.trainable_weights])
non_trainable_count = np.sum([K.count_params(w) \
                              for w in base_model.non_trainable_weights])
print('Total params: {:,}'.format(trainable_count + non_trainable_count))
print('Trainable params: {:,}'.format(trainable_count))
print('Non-trainable params: {:,}'.format(non_trainable_count))
```
```log
Total params: 20,861,480
Trainable params: 3,696,088
Non-trainable params: 17,165,392
```

## tensorflow-macos Releases

| tensorflow-macos | tensorflow-metal | macOS version | Features                          |
| ---------------- | ---------------- | ------------- | --------------------------------- |
| v2.5             | 0.1.2            | 12.0+         | Pluggable device                  |
| v2.6             | 0.2.0            | 12.0+         | Variable sequences for RNN layers |
| v2.7             | 0.3.0            | 12.0+         | Custom op support                 |
| v2.8             | 0.4.0            | 12.0+         | RNN performance improvements      |
| v2.9             | 0.5.0            | 12.1+         | Distributed training              |
