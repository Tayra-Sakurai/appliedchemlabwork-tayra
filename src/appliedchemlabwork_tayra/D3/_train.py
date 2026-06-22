from roboflow import Roboflow
from roboflow.core.dataset import Dataset
from ultralytics import YOLO
from os import getenv
from getpass import getpass


def _load_data():
    api_key = getenv('ROBOFLOW_API_KEY') or getpass('API Key: ')
    rf = Roboflow(api_key=api_key)
    project = rf.workspace("lbiomic-laboratorio-de-biotecnologia-microbiana").project("gell_app_analysis")
    version = project.version(14)
    dataset = version.download("yolo26")
    return dataset


def _train(dataset: Dataset):
    model = YOLO('yolo26n.pt')
    trainresult = model.train(data=f'{dataset.location}/data.yaml', epochs=3, imgsz=640, save_dir='./trained-model')
    return trainresult


if __name__ == '__main__':
    print(_train(_load_data()))
