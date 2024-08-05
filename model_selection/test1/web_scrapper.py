import requests
from bs4 import BeautifulSoup
import json

data = {}

urls = [
    'https://huggingface.co/facebook/detr-resnet-50',
    'https://huggingface.co/Ultralytics/YOLOv8',
    'https://huggingface.co/PekingU/rtdetr_r50vd',
    'https://huggingface.co/hustvl/yolos-tiny',
    'https://huggingface.co/foduucom/stockmarket-future-prediction',
    'https://huggingface.co/microsoft/table-transformer-detection',
    'https://huggingface.co/foduucom/web-form-ui-field-detection',
    'https://huggingface.co/PekingU/rtdetr_r50vd_coco_o365',
    'https://huggingface.co/jameslahm/yolov10x',
    'https://huggingface.co/omoured/YOLOv10-Document-Layout-Analysis',
    'https://huggingface.co/keras-io/Object-Detection-RetinaNet',
    'https://huggingface.co/nickmuchi/yolos-small-finetuned-license-plate-detection',
    'https://huggingface.co/microsoft/table-transformer-structure-recognition',
    'https://huggingface.co/valentinafeve/yolos-fashionpedia',
    'https://huggingface.co/fcakyon/mmdet-yolox-tiny',
    'https://huggingface.co/jozhang97/deta-resnet-50',
    'https://huggingface.co/ultralyticsplus/yolov8s',
    'https://huggingface.co/keremberke/yolov8s-plane-detection',
    'https://huggingface.co/keremberke/yolov8m-nlf-head-detection',
    'https://huggingface.co/jozhang97/deta-swin-large',
    'https://huggingface.co/rizavelioglu/fashionfail',
    'https://huggingface.co/unojcn9f/screenlist-slicing',
    'https://huggingface.co/mshamrai/yolov8x-visdrone',
    'https://huggingface.co/mw00/yolov7-lego',
    'https://huggingface.co/foduucom/table-detection-and-extraction',
    'https://huggingface.co/MuGeminorum/human-detector'
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

for link in urls:
    try:
        response = requests.get(link, headers=headers)
        response.raise_for_status()  

        soup = BeautifulSoup(response.text, 'html.parser')

        model_name = link.split('/')[-1]
        data[model_name] = {}

        model_overview = soup.find('div', class_='model-card-content')
        data[model_name]["Model Overview"] = model_overview.get_text(strip=True) if model_overview else 'N/A'

        sections = soup.find_all('section', class_='section')

        for section in sections:
            title = section.find('h2').get_text(strip=True) if section.find('h2') else 'Unknown Section'
            content = section.get_text(strip=True)
            data[model_name][title] = content

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {link}: {e}")
        data[model_name] = {"Model Overview": 'Error fetching data'}

with open('test_models/models_overview.json', 'w') as file:
    json.dump(data, file, indent=4)
