from django.shortcuts import render, HttpResponse
import os
from io import BytesIO
from PIL import Image
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import numpy as np

import torch

@csrf_exempt
def detect_mask(request):
    if request.method == 'POST':
        print('sicc')
        print(request.FILES)
        print(request)
        if request.FILES.get('image'):
            print(os.getcwd() , " directory")
        # Load YOLOv5 model
            model = torch.hub.load('ultralytics/yolov5:v6.0', 'custom', path='mask_yolov5.pt')  # Replace with your model path

            # Get the uploaded image
            image = request.FILES['image']
            print('hi')

            image_bytes = image.read()
            pil_image = Image.open(BytesIO(image_bytes))
            image_np = np.array(pil_image)

            # Perform face mask detection
            # results = model(image.temporary_file_path())
            results = model(image_np)

            # Process the results as needed
            boxes = results.xyxy[0][:, :4].cpu().numpy().tolist()
            scores = results.xyxy[0][:, 4].cpu().numpy().tolist()
            labels = results.xyxy[0][:, 5].cpu().numpy().tolist()
            print(boxes, scores, labels)

            response_data = {
                'boxes': boxes,
                'scores': scores,
                'labels': labels,
            }
            return JsonResponse(response_data)
    else:
        return HttpResponseBadRequest("Invalid request. Please provide an image file.")


def home(request):
    return HttpResponse('Hello')
