from rest_framework import viewsets, generics
from .models import Item
from .serializers import ItemSerializer


import pickle
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from keras.preprocessing import image
from joblib import load
import numpy as np
from PIL import Image

from app.serializers import InjuryPredictSerializer
from rest_framework.response import Response
from rest_framework.views import APIView



class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class ItemDetail(generics.RetrieveAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

with open("models/imageClassifier.h5", 'rb') as file:
    loaded_model = pickle.load(file)
class InjuryPredict(APIView):
    def post(self, request):
        serializer = InjuryPredictSerializer(data=request.data)
        if serializer.is_valid():
            animal_image = request.data.get("AnimalImage")  # Get the uploaded image data

            # Read the image data and resize it to match the expected input shape of the model
            pil_image = Image.open(animal_image)
            pil_image = pil_image.convert('RGB')  # Ensure the image is in RGB format
            pil_image = pil_image.resize((180, 180))  # Resize the image to (180, 180)

            # Convert the resized image to a NumPy array
            x = image.img_to_array(pil_image)
            test_img = np.expand_dims(x, axis=0)

            result = loaded_model.predict(test_img)
            pred = np.argmax(result)
            return Response({"Result": pred})
        else:
            return Response(serializer.errors, status=400)