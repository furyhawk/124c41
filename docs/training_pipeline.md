trainer.train

trainer-stage
train, valid, test

dict_keys(['train_loss', 'valid_loss', 'valid_trues', 'valid_logits', 'valid_preds', 'valid_probs', 'valid_elapsed_time', 'val_MulticlassAccuracy', 'val_MulticlassPrecision', 'val_MulticlassRecall', 'val_MulticlassAUROC', 'val_MulticlassCalibrationError', ('val_MulticlassCalibrationError', 'train_loss')])

python tools/train.py -f exps/example/custom/nano.py -d 1 -b 8 -c yolox_nano.pth