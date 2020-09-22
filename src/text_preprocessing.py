from services.preprocessing import Preprocessor
import config.configuration as config
import re

def replace_tokens(df):
    df['tokenized_text'] = df.apply(
        lambda row: row['text'].replace(row['name'], '<CARDNAME>'), axis=1)
    for regex in config.REGEX:
        df['tokenized_text'] = df['tokenized_text'].apply(
            lambda text: re.sub(regex['regex'], regex['token'], text))
    return df

def preprocess_text(df):
    preprocessor = Preprocessor()
    df['preprocess_text'] = df['tokenized_text'].apply(
        lambda text: preprocessor.set_text(text).pipeline().get_text())
    df['preprocess_flavor'] = df['flavor'].apply(
        lambda text: preprocessor.set_text(text).pipeline().get_text())
    return df