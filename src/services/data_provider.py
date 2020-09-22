from services.files import join, exists, list_dir, create_dir, get_filename
from services.storage import BlobStorageService
from services.settings import Settings


def __create_storage_service():
    return BlobStorageService(Settings().get(
        "STORAGE_ACCOUNT_NAME"), Settings().get("STORAGE_ACCOUNT_KEY"))


def __download_file(container_name, filepath, blob_path, force):
    if exists(filepath) and not force:
        return filepath

    blob_service = __create_storage_service()
    blob_service.download_blob(container_name, blob_path, filepath)
    return filepath


def __download_folder(container_name, local_path, blob_path, force):
    if len(list_dir(local_path)) > 0 and not force:
        return local_path

    blob_service = __create_storage_service()
    blob_service.download_blobs(container_name, local_path, blob_path)
    return local_path


def __upload_file(container_name, blob_name, filepath=None):
    blob_service = __create_storage_service()
    blob_service.upload_file(container_name, blob_name, filepath)
    return filepath


def generate_raw_dataset_filename(language):
    return f"dataset-{language}.csv"


def generate_processed_dataset_filename(language):
    return f"preprocess-dataset-{language}.csv"


def generate_processed_images_folder(language):
    return f"images-{language}"


def download_raw_dataset(language, force=False, output_path=None):
    filename = generate_raw_dataset_filename(language)
    local_path = filename if not output_path else join(output_path, filename)
    return __download_file(Settings().get(
        "RAW_DATASET_CONTAINER_NAME"), local_path, filename, force)


def download_processed_dataset(language, force=False, output_path=None):
    filename = generate_processed_dataset_filename(language)
    local_path = filename if not output_path else join(output_path, filename)
    return __download_file(Settings().get(
        "PREPROCESSED_DATASET_CONTAINER_NAME"), local_path, filename, force)


def download_processed_images(language, force=False, output_path=None):
    local_path = join(
        output_path, generate_processed_images_folder(language))
    return __download_folder(Settings().get(
        "PREPROCESSED_IMAGES_CONTAINER_NAME"), local_path, None, force)


def upload_raw_dataset(language):
    return __upload_file(Settings().get(
        "RAW_DATASET_CONTAINER_NAME"), generate_raw_dataset_filename(language))


def upload_processed_dataset(language):
    return __upload_file(Settings().get(
        "PREPROCESSED_DATASET_CONTAINER_NAME"), generate_processed_dataset_filename(language))


def upload_processed_image(filepath):
    return __upload_file(Settings().get(
        "PREPROCESSED_IMAGES_CONTAINER_NAME"), get_filename(filepath), filepath)
