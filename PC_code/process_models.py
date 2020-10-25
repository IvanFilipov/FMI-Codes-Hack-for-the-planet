import tensorflow as tf
config = tf.ConfigProto()
config.gpu_options.allow_growth = True
sess = tf.Session(config=config)
import os
import tensorflow.keras as keras
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.layers import Conv2D, Flatten, MaxPooling2D,Dense,Dropout
from tensorflow.keras.models  import Sequential
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np

def softmax(w, t = 1.0):
    e = np.exp(np.array(w) / t)
    dist = e / np.sum(e)
    return dist
def argMax(w):
    currentIndex = 0
    currentV = w[currentIndex]
    for i, val in enumerate(w):
        if(val > currentV):
            currentV = val
            currentIndex = i
    return currentIndex

class ProcessModel(object):
    """docstring for ProcessModel"""
    def __init__(self, arg):
        super(ProcessModel, self).__init__()
        self.arg = arg
        self.modelPath = "D:\FMI code\VGG16 Garbage Classifier.h5"
        # modelPath = "D:\FMI code\models\my_model.h5"
        # modelPath = "D:\FMI code\CNN-Modelo.h5"
        # modelPath = "D:\FMI code\\trained_model.h5"
        # modelPath = "D:\FMI code\models\model_385-0.97.h5"

        print("Load model")
        self.new_model = tf.keras.models.load_model(modelPath)

        self.class_names = np.array(['Cardboard', 'Glass', 'Metal', 'Paper', 'Plastic', 'Trash'])

        self.img_width = new_model.input_shape[2]
        self.img_height = new_model.input_shape[1]

    def predict(self, imgUrl):
        print("Start predict")

        # forPredictImgUrl = "http://192.168.2.105/paper2.jpg"
        forPredictImg = tf.keras.utils.get_file('Red_sunflower', origin=imgUrl)
        # forPredictImg = 'D:/FMI code/test_images_save/images/1603562498.jpeg'


        img = keras.preprocessing.image.load_img(
            forPredictImg, target_size=(self.img_height, self.img_width)
        )

        img_array = keras.preprocessing.image.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0) # Create a batch

        predictions = self.new_model.predict(img_array, steps=1)
        score = tf.nn.softmax(predictions[0])

        maxArg = argMax(softmax(predictions[0]))
        predictedClassIndex = maxArg
        predictedClass = self.class_names[predictedClassIndex]

        print("Finish predict")
        print(softmax(predictions[0]))
        print("Predicted class {}".format(predictedClass))
        print("Predicted index {}".format(predictedClassIndex))

        argLimit = 2.5
        if(maxArg < argLimit):
            predictedClassIndex = 5
            predictedClass = "Trash"


        resultIndex = 0
        resultClass = ""
        if(predictedClass == "Paper" || predictedClass == "Cardboard"):
            resultIndex = 1
            resultClass = "Paper"
        else if(predictedClass == "Glass"):
            resultIndex = 2
            resultClass = "Glass"
        else if(predictedClass == "Plastic" || predictedClass == "Metal"):
            resultIndex = 3
            resultClass = "Plastic and Metal"
        else:
            resultIndex = 4
            resultClass = "Trash"


        return {resultIndex, resultClass}
        


modelPath = "D:\FMI code\VGG16 Garbage Classifier.h5"
# modelPath = "D:\FMI code\models\my_model.h5"
# modelPath = "D:\FMI code\CNN-Modelo.h5"
# modelPath = "D:\FMI code\\trained_model.h5"
# modelPath = "D:\FMI code\models\model_385-0.97.h5"

new_model = tf.keras.models.load_model(modelPath)

class_names = np.array(['Cardboard', 'Glass', 'Metal', 'Paper', 'Plastic', 'Trash'])

img_width = new_model.input_shape[2]
img_height = new_model.input_shape[1]

while(True):
    #

    print("Start predict")

    forPredictImgUrl = "http://192.168.2.105/paper2.jpg"
    forPredictImg = tf.keras.utils.get_file('Red_sunflower', origin=forPredictImgUrl)
    # forPredictImg = 'D:/FMI code/test_images_save/images/1603562498.jpeg'


    img = keras.preprocessing.image.load_img(
        forPredictImg, target_size=(img_height, img_width)
    )

    img_array = keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0) # Create a batch

    predictions = new_model.predict(img_array, steps=1)
    score = tf.nn.softmax(predictions[0])

    maxArg = argMax(softmax(predictions[0]))
    predictedClassIndex = maxArg
    predictedClass = class_names[predictedClassIndex]

    print("Finish predict")
    print(softmax(predictions[0]))
    print("Predicted class {}".format(predictedClass))
    print("Predicted index {}".format(predictedClassIndex))
    break
