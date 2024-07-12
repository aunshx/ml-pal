import requests
from bs4 import BeautifulSoup
import json
data = {}
url = ['https://huggingface.co/Ultralytics/YOLOv8', 'https://huggingface.co/foduucom/thermal-image-object-detection', 'https://huggingface.co/keras-io/Object-Detection-RetinaNet']
for links in url:
    response = requests.get(links)

    soup = BeautifulSoup(response.text, 'html.parser')

    model_overview = soup.find('div', class_='model-card-content')
    overview_text = model_overview.get_text() if model_overview else 'N/A'
    model_name = links.split('/')[-1]

    data[model_name] = {
        "Model Overview": overview_text
    }
with open('models.json', 'w') as file:
    json.dump(data, file, indent=4)