from django.db import models
from django.urls import reverse
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from tensorflow.python.keras.models import load_model, model_from_json
from keras import backend as K
from skimage.transform import resize   
import matplotlib.pyplot as plt
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
    CLASS_NAMES=['ciclismo', 'basket', 'tenis', 'futbol', 'americano', 'golf', 'beisball', 'boxeo', 'natacion', 'f1']
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
        img = self.preprocesamiento(self, path=path)
        certeza,predicion = self.predict(self, img)
        print('La prediccion es ',predicion )
        db=models.Image(image=path,label=predicion,probability=certeza)
        db.save()
        return (certeza,predicion)

    def predict(self, imgT):
        #print('---------------------------------------------------------------------------')
       # print(imgT)
        predicted_classes = self.Selectedmodel.predict(imgT)
        print("Predicciones")
        #predicted_classes = sport_model.predict(test_X)
        #resultados = sport_model.predict(predicted_classes)
        print(predicted_classes)
        maxElement = numpy.amax(predicted_classes)
        certeza=str(round(maxElement*100,4))
        print('Certeza: ', str(round(maxElement*100,4))+'%')
        result = numpy.where(predicted_classes == numpy.amax(predicted_classes))
        print('Max :',maxElement )
        print('Lista de indices de maximo elemento : ' , result[0][0])
        index_sample_label = result[0][0] 

        print(self.CLASS_NAMES)
        for i, img_tagged in enumerate(predicted_classes):
            predicion=self.CLASS_NAMES[img_tagged.tolist().index(max(img_tagged))]
            #print("Cantidad etiquetas creadas: ",len(labels))
            print('Etiqueta de Prediccion :',self.CLASS_NAMES[img_tagged.tolist().index(max(img_tagged))])


        return (certeza,predicion)
        
    def preprocesamiento(self, path):
        images=[]

        for filepath in path:
            image = plt.imread(settings.BASE_DIR + path,0)
            image_resized = resize(image, (21, 28),anti_aliasing=True,clip=False,preserve_range=True)
            images.append(image_resized)

        X = np.array(images, dtype=np.uint8) #convierto de lista a numpy
        test_X = X.astype('float32')
        test_X = test_X / 255.
        #img = img.resize(self.IMAGE_SIZE , clip=False)
        #imgResizec = resize(img, self.IMAGE_SIZE,anti_aliasing=True,clip=False,preserve_range=True)
        #X = np.array(img, dtype=np.uint8)
        #test_X = X.reshape(1, self.IMAGE_SIZE[0], self.IMAGE_SIZE[1], 3)
        #test_X = X.astype('float32')
        #test_X = X / 255. 
        #print(X)
        return test_X

