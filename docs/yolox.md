# yolox
```sh
python tools/train.py -f exps/example/custom/nano.py -d 1 -b 2 -c yolox_nano.pth
```

```log
2023-04-20 08:49:15.731 | INFO     | yolox.data.datasets.mosaicdetection:__getitem__:161 - [ 12.       98.56714 250.26144  70.88641   9.62624]
2023-04-20 08:49:15.733 | INFO     | yolox.data.datasets.mosaicdetection:__getitem__:161 - [ 13.       130.93268  229.41734   91.643555  72.7481  ]
2023-04-20 08:49:16 | INFO     | yolox.core.trainer:261 - epoch: 5/5, iter: 60/62, gpu mem: 0Mb, mem: 5.4Gb, iter_time: 3.179s, data_time: 2.856s, total_loss: 1.6, iou_loss: 0.6, l1_loss: 0.1, conf_loss: 0.4, cls_loss: 0.4, lr: 3.085e-04, size: 416, ETA: 0:00:06
2023-04-20 08:49:18.890 | INFO     | yolox.data.datasets.mosaicdetection:__getitem__:161 - [ 58.       133.07756  166.66658    5.388448   4.927013]
2023-04-20 08:49:18.890 | INFO     | yolox.data.datasets.mosaicdetection:__getitem__:161 - [  6.      138.9172  213.91843  94.45138 352.15067]
2023-04-20 08:49:18.890 | INFO     | yolox.data.datasets.mosaicdetection:__getitem__:161 - [  4.      218.88423 140.31888 104.04545 165.01555]
2023-04-20 08:49:18.891 | INFO     | yolox.data.datasets.mosaicdetection:__getitem__:161 - [ 44.      141.09167 260.7022  282.48337 301.27512]
2023-04-20 08:49:18.893 | INFO     | yolox.data.datasets.mosaicdetection:__getitem__:161 - [ 14.       130.99757   47.066467  56.686657  20.449068]
2023-04-20 08:49:18.895 | INFO     | yolox.data.datasets.mosaicdetection:__getitem__:161 - [ 64.       220.6489   303.2769   114.6341   102.452896]
2023-04-20 08:49:18.895 | INFO     | yolox.data.datasets.mosaicdetection:__getitem__:161 - [ 61.       256.1682    55.158962  42.048447  45.89014 ]
2023-04-20 08:49:18.895 | INFO     | yolox.data.datasets.mosaicdetection:__getitem__:161 - [24.       19.571447 57.297344 19.864103 34.632   ]
2023-04-20 08:49:18.899 | INFO     | yolox.data.datasets.mosaicdetection:__getitem__:161 - [ 40.        178.63289   129.9869      7.916896    7.5660305]
2023-04-20 08:49:18.901 | INFO     | yolox.data.datasets.mosaicdetection:__getitem__:161 - [ 66.      319.8782  183.105   111.56579 109.044  ]
2023-04-20 08:49:18.901 | INFO     | yolox.data.datasets.mosaicdetection:__getitem__:161 - [ 54.      269.932   236.27823  85.54    143.03235]
2023-04-20 08:49:18.901 | INFO     | yolox.data.datasets.mosaicdetection:__getitem__:161 - [ 49.      340.53177 187.7362  147.19244 134.72554]
2023-04-20 08:49:18.903 | INFO     | yolox.data.datasets.mosaicdetection:__getitem__:161 - [ 69.      283.95578 123.04812 243.99066 180.18655]
2023-04-20 08:49:18.904 | INFO     | yolox.data.datasets.mosaicdetection:__getitem__:161 - [ 26.       183.09532  116.72701   26.500448  15.249037]
2023-04-20 08:49:18.904 | INFO     | yolox.data.datasets.mosaicdetection:__getitem__:161 - [ 12.       98.56714 250.26144  70.88641   9.62624]
2023-04-20 08:49:18.905 | INFO     | yolox.data.datasets.mosaicdetection:__getitem__:161 - [ 13.       285.06732  229.41734   91.643555  72.7481  ]
2023-04-20 08:49:22.045 | INFO     | yolox.data.datasets.mosaicdetection:__getitem__:161 - [  6.      138.0828  213.91843  94.45138 352.15067]
2023-04-20 08:49:22.045 | INFO     | yolox.data.datasets.mosaicdetection:__getitem__:161 - [ 58.       282.92242  166.66658    5.388448   4.927013]
2023-04-20 08:49:22.046 | INFO     | yolox.data.datasets.mosaicdetection:__getitem__:161 - [ 44.      242.90833 260.7022  282.48337 301.27512]
2023-04-20 08:49:22.047 | INFO     | yolox.data.datasets.mosaicdetection:__getitem__:161 - [  4.      218.88423 140.31888 104.04545 165.01555]
2023-04-20 08:49:22.049 | INFO     | yolox.data.datasets.mosaicdetection:__getitem__:161 - [ 14.       285.00244   47.066467  56.686657  20.449068]
2023-04-20 08:49:22.050 | INFO     | yolox.data.datasets.mosaicdetection:__getitem__:161 - [ 64.       220.6489   303.2769   114.6341   102.452896]
2023-04-20 08:49:22.050 | INFO     | yolox.data.datasets.mosaicdetection:__getitem__:161 - [ 24.       292.42856   57.297344  19.864103  34.632   ]
2023-04-20 08:49:22.051 | INFO     | yolox.data.datasets.mosaicdetection:__getitem__:161 - [ 61.       159.83177   55.158962  42.048447  45.89014 ]
2023-04-20 08:49:22.054 | INFO     | yolox.data.datasets.mosaicdetection:__getitem__:161 - [ 40.        237.36711   129.9869      7.916896    7.5660305]
2023-04-20 08:49:22.056 | INFO     | yolox.data.datasets.mosaicdetection:__getitem__:161 - [ 49.       75.46822 187.7362  147.19244 134.72554]
2023-04-20 08:49:22.056 | INFO     | yolox.data.datasets.mosaicdetection:__getitem__:161 - [ 54.      269.932   236.27823  85.54    143.03235]
2023-04-20 08:49:22.058 | INFO     | yolox.data.datasets.mosaicdetection:__getitem__:161 - [ 69.      283.95578 123.04812 243.99066 180.18655]
2023-04-20 08:49:22.059 | INFO     | yolox.data.datasets.mosaicdetection:__getitem__:161 - [ 26.       183.09532  116.72701   26.500448  15.249037]
2023-04-20 08:49:22.060 | INFO     | yolox.data.datasets.mosaicdetection:__getitem__:161 - [ 13.       285.06732  229.41734   91.643555  72.7481  ]
2023-04-20 08:49:22 | INFO     | yolox.core.trainer:364 - Save weights to ./YOLOX_outputs/nano
  0%|          | 0/3 [00:00<?, ?it/s]2023-04-20 08:49:23.548 | INFO     | yolox.data.datasets.coco:__getitem__:189 - [[0. 0. 0. 0. 0.]]
2023-04-20 08:49:23.549 | INFO     | yolox.data.datasets.coco:__getitem__:189 - [[0. 0. 0. 0. 0.]]
2023-04-20 08:49:23.552 | INFO     | yolox.data.datasets.coco:__getitem__:189 - [[0. 0. 0. 0. 0.]]
2023-04-20 08:49:23.557 | INFO     | yolox.data.datasets.coco:__getitem__:189 - [[0. 0. 0. 0. 0.]]
2023-04-20 08:49:23.560 | INFO     | yolox.data.datasets.coco:__getitem__:189 - [[0. 0. 0. 0. 0.]]
2023-04-20 08:49:23 | INFO     | yolox.utils.boxes:42 - tensor([[[-3.0691e-02, -6.9531e-01,  1.7874e+01,  ...,  7.3838e-03,
           2.3374e-03,  9.7559e-03],
         [ 1.1258e-01, -1.7617e+00,  3.6079e+01,  ...,  4.4751e-03,
           2.4137e-03,  1.6975e-02],
         [ 1.1568e+00, -5.3255e-01,  4.4746e+01,  ...,  4.3620e-03,
           2.2308e-03,  1.6169e-02],
         ...,
         [ 2.0542e+02,  3.2890e+02,  4.0200e+02,  ...,  2.4142e-02,
           1.8872e-02,  4.6836e-03],
         [ 2.5580e+02,  3.3263e+02,  4.0311e+02,  ...,  2.3758e-02,
           1.5198e-02,  1.0437e-02],
         [ 2.8720e+02,  3.2424e+02,  4.5185e+02,  ...,  2.1452e-02,
           1.5419e-02,  1.3066e-02]],

        [[-1.8283e+00, -2.5546e+00,  2.2447e+01,  ...,  5.3017e-03,
           1.2330e-03,  2.6441e-03],
         [-3.4582e+00, -3.6768e+00,  4.1270e+01,  ...,  2.6849e-03,
           1.1189e-03,  2.4038e-03],
         [-5.6546e+00, -3.1051e+00,  4.5746e+01,  ...,  2.2974e-03,
           5.3034e-04,  1.1495e-03],
         ...,
         [ 2.1253e+02,  3.0931e+02,  4.0027e+02,  ...,  1.1962e-02,
           2.6160e-02,  1.0538e-02],
         [ 2.2916e+02,  3.0754e+02,  4.5759e+02,  ...,  1.1956e-02,
           3.1521e-02,  1.2290e-02],
         [ 2.5522e+02,  2.9314e+02,  4.7906e+02,  ...,  1.3841e-02,
           2.9837e-02,  8.0685e-03]]])
 33%|###3      | 1/3 [00:01<00:02,  1.14s/it]2023-04-20 08:49:23 | INFO     | yolox.utils.boxes:42 - tensor([[[-1.9547e-01, -2.6602e-01,  1.9520e+01,  ...,  1.5079e-02,
           1.5027e-03,  1.1642e-02],
         [-4.5387e-01, -1.2133e+00,  2.7151e+01,  ...,  1.5102e-02,
           2.2074e-03,  1.4446e-02],
         [ 6.5304e-01, -1.3691e+00,  4.4025e+01,  ...,  1.7528e-02,
           2.2192e-03,  1.3043e-02],
         ...,
         [ 2.0673e+02,  3.0448e+02,  4.0279e+02,  ...,  7.8812e-03,
           1.2321e-02,  6.5607e-03],
         [ 2.3585e+02,  3.1618e+02,  4.4467e+02,  ...,  8.3829e-03,
           1.4222e-02,  7.0587e-03],
         [ 2.6112e+02,  3.0265e+02,  4.7150e+02,  ...,  9.6596e-03,
           2.5569e-02,  5.9508e-03]],

        [[-4.4389e-01, -8.9837e-01,  1.4791e+01,  ...,  4.5179e-03,
```