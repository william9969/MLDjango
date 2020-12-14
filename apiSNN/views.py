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

    'apiKey': "AIzaSyDBYpL2tb3yh3SIPo2BFhlS7slKruVGOic",
    'authDomain': "proyectotiendajpri.firebaseapp.com",
    'databaseURL': "https://proyectotiendajpri.firebaseio.com",
    'projectId': "proyectotiendajpri",
    'storageBucket': "proyectotiendajpri.appspot.com",
    'messagingSenderId': "1046831721926",
    'appId': "1:1046831721926:web:7402a636a8cd165f4b16c7",
    'measurementId': "G-MKSCN84RDE"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

class UploadImage():
    def image_view(request):
        if request.method == 'POST':
            form = forms.ImageForm(request.POST, request.FILES)
            
        return render(request, 'deportes.html')

    def success(request):
        path = request.POST.get('image')
        print(path)
        #Predecir imagen
        predecirDeportes(request)

class Clasificacion():
    #imagen = models.ImageField(upload_to='imagenes')
    #prediccion = models.CharField(max_length=200, blank=True)

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
        resultado= modeloSNN.modeloSNN.predecirDeporte(modeloSNN.modeloSNN,filePathName)
        return render(request, "prediccion.html")#,{"e":resul})