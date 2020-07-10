# Self-Driving-Steering-Angle-prediction
Steering wheel angle prediction

## data 数据

Through the vehicle driving simulator developed by unity company, the photos and data of driving are obtained.

## Learning objectives 学习目标

According to the picture of the car camera, it can automatically judge how to turn the steering wheel. Use end-to-end deep learning.

## simulator

<html>
<a href='https://pan.baidu.com/s/1qfzczPuRz0UgL3e4-x_-Ww'>get Simulator link</a>
  <p>pwd：82ii</p>
</html>

## Details About Files In This Directory

### `drive.py`
Usage of `drive.py` requires you have saved the trained model as an h5 file, i.e. `model.h5`. See the [Keras documentation](https://keras.io/getting-started/faq/#how-can-i-save-a-keras-model) for how to create this file using the following command:
```sh
model.save(filepath)
```
This file will establish a socket connection with the emulator.
### `train.py`
Usage of `train.py` requires you design your own CNN model and how to do image preprocessing and other operations.
You can use the following command:
```sh
python train.py
```
### Tips
- Please keep in mind that training images are loaded in BGR colorspace using cv2 while drive.py load images in RGB to predict the steering angles.





