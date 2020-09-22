import pandas as pd
from sklearn.utils import shuffle

from .files import list_dir, exists, join, rebase_path

def __read_and_clean_dataset(dataset_path):
    df = pd.read_csv(dataset_path, sep=';')
    df.dropna(inplace=True, subset=['preprocess_text'])
    return df


def filter_long_texts(df, max_words):
    mask = (df['tokenized_text'].str.split().str.len()
            < max_words)
    df = df.loc[mask]
    return df


def filter_existing_cards(df, images_path):
    filtered_captions = []
    filtered_image_paths = []
    image_paths = list_dir(images_path)

    for _, caption in df.iterrows():
        image_path = join(images_path, caption['id'] + ".jpg")
        if any(image_path in path for path in image_paths):
            filtered_captions.append(caption['tokenized_text'])
            filtered_image_paths.append(image_path)

    return filtered_captions, filtered_image_paths