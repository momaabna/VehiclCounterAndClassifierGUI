#AlexNet Model
import tensorflow as tf
from sklearn.utils import shuffle
import cv2
import numpy as np
#from tensorflow.contrib.keras.python.keras.optimizers import SGD
#from tensorflow.contrib.keras.python.keras.backend import clear_session
#from tensorflow.contrib.keras.python.keras.models import Sequential
#from tensorflow.contrib.keras.python.keras.layers import Conv2D,Dense,MaxPooling2D,Activation,Flatten,Dropout
#from tensorflow.contrib.keras.python.keras.utils.np_utils import to_categorical
#from tensorflow.contrib.keras.python.keras.utils import normalize

from tensorflow.contrib.keras.python.keras.optimizers import SGD
from tensorflow.contrib.keras.python.keras.backend import clear_session
from tensorflow.contrib.keras.python.keras.models import Sequential
from tensorflow.contrib.keras.python.keras.layers import Conv2D,Dense,MaxPooling2D,Activation,Flatten,Dropout
from tensorflow.contrib.keras.python.keras.utils.np_utils import to_categorical
from tensorflow.contrib.keras.python.keras.utils import normalize
class AlexNet:
    def __init__(self):
        #Layer 1
        clear_session()
        self.model =Sequential()
        self.model.add(Conv2D(96,kernel_size=(11,11),strides=(4,4),input_shape=(224,224,3),padding='valid'))
        self.model.add(Activation('relu'))
        self.model.add(MaxPooling2D(pool_size=(3,3),strides=(2,2)))
        #Layer 2
        self.model.add(Conv2D(256, (5, 5),padding='valid'))
        self.model.add(Activation('relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2),strides=(2,2)))
        # Layer 3
        self.model.add(Conv2D(384, (3, 3),padding='valid'))
        self.model.add(Activation('relu'))

        # Layer 4
        self.model.add(Conv2D(384, (3, 3), padding='valid'))
        self.model.add(Activation('relu'))

        # Layer 5
        self.model.add(Conv2D(256, (3, 3),padding='valid'))
        self.model.add(Activation('relu'))
        self.model.add(MaxPooling2D(pool_size=(3, 3),strides=(2,2)))
        #Layer 7
        self.model.add(Flatten())
        self.model.add(Dense(4096))
        self.model.add(Activation('relu'))
        self.model.add(Dropout(0.4))
        #Layer 8
        self.model.add(Dense(4096))
        self.model.add(Activation('relu'))
        self.model.add(Dropout(0.4))
        #Layer 9
        self.model.add(Dense(1000))
        self.model.add(Activation('relu'))
        self.model.add(Dropout(0.4))
        
        self.model.add(Dense(11))
        self.model.add(Activation('softmax'))
        self.model.compile(optimizer=SGD(lr=0.005),loss='categorical_crossentropy',metrics=['accuracy'])
    def train(self):
        import pickle
        import numpy as np
        X = np.array(pickle.load(open('trainx.pcl','rb')))
        
        Y = to_categorical(np.array(pickle.load(open('trainy.pcl','rb'))))
        
        X,Y=shuffle(X,Y)
        patch=64

        self.model.fit(X,Y,batch_size=patch,validation_split=0.1,epochs=100)
    def save(self):
        self.model.save('model.h5')

    def predict(self,imgs):

        return np.array(to_categorical(self.model.predict_classes(imgs),11))
    def loadmodel(self):
        self.model.load_weights('model_final74.h5')
    def distroy(self):
        clear_session()

        print('End Session')

