from django.db import models
from django.urls import reverse
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from tensorflow.python.keras.models import load_model, model_from_json
from keras import backend as K
from apiSNN import models
from keras.preprocessing import image
import os
from tensorflow.python.keras.models import Sequential
import pathlib
import numpy 
from skimage.transform import resize
from PIL import Image
from django.conf import settings


class modeloSNN():
    """Clase modelo SNN"""
    Selectedmodel = Sequential()
    CLASS_NAMES=['americano', 'basket', 'beisball', 'boxeo', 'ciclismo', 'f1', 'futbol', 'golf', 'natacion', 'tennis']
    IMAGE_SIZE = (21, 28)

    def cargarRNN(archivoModelo,archivoPesos):
        K.reset_uids
        with open(archivoModelo+'.json','r') as f:
            model = model_from_json(f.read())

        model.load_weights(archivoPesos+'.h5')
        print("Red Neuronal Cargada")
        return model

    def predecirDeporte(self, path):

        print(path)
        archivoModelo=r'apiSNN/Logica/modeloRNN'
        archivoPesos=r'apiSNN/Logica/pesosRNN'
        self.Selectedmodel = self.cargarRNN(archivoModelo, archivoPesos) 
        print(self.Selectedmodel)
        print(self.Selectedmodel.summary())

        img = Image.open(settings.BASE_DIR + path).convert('RGB')
        img = img.resize(self.IMAGE_SIZE)
        img.save(settings.BASE_DIR + path, "JPEG", optimize=True)


        img = self.preprocesamiento(self, img=img)
        maxElement, certeza,predicion = self.predict(self, img)
        #dbReg = models.Image(image=path, label=prediction_result, probability=maxElement)
        #dbReg.save()
        return (certeza,predicion)

    def predict(self, imgT):
        print('---------------------------------------------------------------------------')
        print(imgT)
        predicted_classes = self.Selectedmodel.predict(imgT)[0]
        print('Predictions: ', predicted_classes)
        maxElement =numpy.amax(predicted_classes)
        certeza=str(round(maxElement*100,4))+'%'
        print('Certeza: ', str(round(maxElement*100,4))+'%')
        result=numpy.where(predicted_classes == numpy.amax(predicted_classes)) 
        print('Max :',maxElement )
        print('Lista de indices de maximo elemento : ' , result[0][0])
        index_sample_label = result[0][0] 
        predicion = self.CLASS_NAMES[index_sample_label]
        return (maxElement, certeza,predicion)
        
    def preprocesamiento(self, img):
        
        X = np.array(img, dtype=np.uint8)
        #test_X = X.reshape(1, self.IMAGE_SIZE[0], self.IMAGE_SIZE[1], 3)
        test_X = X.astype('float32')
        test_X = test_X / 255. 
        print(X)
        return test_X

