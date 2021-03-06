#CONTROLADOR

from django.core.files.storage import FileSystemStorage
from rest_framework import generics #para microservicio
from apiSNN import models
from apiSNN import serializers
from keras.preprocessing import image
from django.shortcuts import render
import pyrebase #para consumo servicio base de datos de firebase
from apiSNN.Logica import modeloSNN #para utilizar modelo SNN


config = {

    'apiKey': "4/1AY0e-g4bsh3PT_PT4wJyasp5cdYKbzR5zGuOlcvAJQz3Oiaq2xqgDUXO1AM",
    'authDomain': "proyectotiendajpri.firebaseapp.com",
    'databaseURL': "https://proyectotiendajpri.firebaseio.com",
    'projectId': "proyectomldeportes",
    'storageBucket': "proyectomldeportes.uc.r.appspot.com",
    'messagingSenderId': "107199634301892604971",
    'appId': "1:1046831721926:web:7402a636a8cd165f4b16c7",
    'measurementId': "G-MKSCN84RDE",
    'storageBucket': "proyectomldeportes.uc.r.appspot.com",
    'messagingSenderId': "1046831721926",
    'appId': "1:1046831721926:web:7402a636a8cd165f4b16c7",
    'measurementId': "G-MKSCN84RDE"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

class Clasificacion():

    def determinarDeporte(request):
        context={'a':1}
        return render(request, "deportes.html",context)

    def predecirDeporte(request):
        
        fileObj=request.FILES['file']
        fs=FileSystemStorage()
        filePathName=fs.save(fileObj.name,fileObj)
        filePathName=fs.url(filePathName)
        #testimage='.'+filePathName
        #img = image.load_img(testimage)
        certeza, prediccion= modeloSNN.modeloSNN.predecirDeporte(modeloSNN.modeloSNN,filePathName)
        return render(request, "prediccion.html",{"pre":prediccion,"c":certeza})