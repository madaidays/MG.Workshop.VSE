import os
import datetime
from .settings import Settings
from .utils.mime import mime_content_type
from azure.storage.blob import BlockBlobService, ContentSettings, ContainerPermissions, BlobPermissions
from singleton_decorator import singleton
from azure.storage.sharedaccesssignature import SharedAccessSignature


@singleton
class BlobStorageService:
    def __init__(self, account_name, account_key, socket_timeout=600):
        self.__settings = Settings()
        self.__account_name = account_name
        self.__account_key = account_key
        self.__blockblob_service = BlockBlobService(
            account_name=self.__account_name,
            account_key=self.__account_key, socket_timeout=socket_timeout)
        self.__blob_access_signature = SharedAccessSignature(
            self.__account_name, self.__account_key)

    def create_container(self, container_name):
        self.__blockblob_service.create_container(container_name)

    def delete_container(self, container_name):
        self.__blockblob_service.delete_container(container_name)

    def upload_file(self, container_name, blob_name, local_file=None, delete_local_file=False):
        local_file = blob_name if local_file == None else local_file
        self.create_container(container_name)
        return self.__upload_file(container_name, blob_name, local_file, delete_local_file)

    def upload_directory(self, container_name, directory, storage_path="", delete_local_file=False):
        self.create_container(container_name)
        files = self.__get_files(directory)
        directories = self.__get_directories(directory)

        blobs = list(map(lambda file: self.__upload_file(container_name,
                                                         os.path.join(
                                                             storage_path, os.path.basename(file)),
                                                         os.path.join(directory, file), delete_local_file), files))

        return blobs + list(map(lambda dir: self.upload_directory(
            container_name, os.path.join(directory, dir), storage_path, delete_local_file), directories))

    def upload_file_from_bytes(self, container_name, filename, file_in_bytes):
        self.create_container(container_name)
        return self.__blockblob_service.create_blob_from_bytes(
            container_name, filename, file_in_bytes)

    def upload_file_from_stream(self, container_name, filename, stream_file):
        self.create_container(container_name)
        return self.__blockblob_service.create_blob_from_stream(
            container_name, filename, stream_file)

    def list_blobs(self, container_name):
        return self.__blockblob_service.list_blobs(container_name)

    def create_blob_from_text(self, container_name, blob_name, text):
        self.create_container(container_name)
        return self.__blockblob_service.create_blob_from_text(container_name, blob_name, str(text))

    def get_blob_to_text(self, container_name, blob_name):
        return self.__blockblob_service.get_blob_to_text(container_name, blob_name)

    def download_blob(self, container_name, blob_name, local_file=None):
        local_file = blob_name if local_file == None else local_file
        self.__create_local_dir(os.path.split(local_file)[0])
        self.__blockblob_service.get_blob_to_path(
            container_name, blob_name, local_file)

    def download_blobs(self, container_name, local_path="", blob_path=""):
        blobs = self.__get_blobs_in_path(container_name, blob_path)
        base = self.__create_local_dir(local_path)

        list(map(lambda blob: self.download_blob(container_name, blob.name,
                                                 os.path.join(base, blob.name)), blobs))

    def read_blob_bytes(self, container_name, blob_name):
        return self.__blockblob_service.get_blob_to_bytes(container_name, blob_name)

    def delete_blob(self, container, blob_name):
        self.__blockblob_service.delete_blob(
            container, blob_name)

    def copy_blob(self, container_name, blob_name, blob_url):
        self.__blockblob_service.copy_blob(container_name, blob_name, blob_url)

    def make_blob_url(self, container_name, blob_name, sas_token=''):
        return self.__blockblob_service.make_blob_url(container_name, blob_name, sas_token=sas_token)

    def generate_container_sas_token(self, container_name, blob_name, days_to_keep=1):
        permission = ContainerPermissions(read=True, write=True)
        return self.__blockblob_service.generate_blob_shared_access_signature(container_name, blob_name,
                                                                              permission, protocol='https',
                                                                              start=datetime.datetime.utcnow(), expiry=datetime.datetime.utcnow() + timedelta(days=days_to_keep))

    def generate_blob_sas_token(self, container_name, blob_name, read=True, add=True, create=True, write=True, delete=False, days_to_keep=1):
        permission = BlobPermissions(read, add, create, write, delete)
        return self.__blob_access_signature.generate_blob(container_name, blob_name, permission=permission, protocol='https', expiry=datetime.now() + timedelta(days=days_to_keep))

    def __upload_file(self, container_name, filename, local_file, delete_local_file=False):
        blob = self.__blockblob_service.create_blob_from_path(container_name,
                                                              filename,
                                                              local_file,
                                                              content_settings=ContentSettings(content_type=self.__get_mime_type(local_file)))
        if delete_local_file:
            os.remove(local_file)
        return blob

    def __get_mime_type(self, file_path):
        return mime_content_type(file_path)

    def __get_blobs_in_path(self, container_name, blob_path):
        blobs = self.list_blobs(container_name)
        if not blob_path:
            return blobs
        return list(filter(lambda blob: blob.name.startswith(blob_path), blobs))

    def __create_local_dir(self, local_path):
        if local_path:
            os.makedirs(local_path, exist_ok=True)
        return os.path.join(os.getcwd(), local_path)

    def __get_directories(self, local_path):
        return [file for file in os.listdir(local_path) if os.path.isdir(
            os.path.join(local_path, file))]

    def __get_files(self, local_path):
        return [file for file in os.listdir(local_path) if os.path.isfile(
            os.path.join(local_path, file))]
