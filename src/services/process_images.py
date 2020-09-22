import requests
import shutil
import cv2
import pandas as pd

from services.data_provider import download_processed_dataset, upload_processed_image
from services.files import exists, rebase_path, create_dir, join


def get_data_from_storage(blob_service, container_name, blob_name, local_file_path, force_update=False):
    if exists(local_file_path) and not force_update:
        return
    blob_service.download_blob(container_name, blob_name, local_file_path)


def check_valid_card(card):
    if card['layout'] != 'normal':
        raise Exception(f"Layout {card['layout']} is invalid")

def download_card(card, tmp):
    local_path = join(tmp, f"{card['id']}.jpg")

    if exists(local_path):
        return

    resp = requests.get(card['image'], stream=True)
    local_file = open(local_path, 'wb')
    resp.raw.decode_content = True
    shutil.copyfileobj(resp.raw, local_file)


def preprocess_card(card, tmp, output):
    local_path = join(tmp, f"{card['id']}.jpg")
    processed_local_path = rebase_path(
        local_path, output)

    if exists(processed_local_path):
        return processed_local_path

    image = cv2.imread(local_path)
    crop = image[42:167, 27:197]
    cv2.imwrite(processed_local_path, crop)
    return processed_local_path


def process_images(df, skip, tmp, output):
    total = len(df.index)
    for index, row in df[skip:].iterrows():
        try:
            check_valid_card(row)
            download_card(row, tmp)
            preprocess_local_path = preprocess_card(row, tmp, output)
            upload_processed_image(preprocess_local_path)
        except Exception as e:
            print(e)