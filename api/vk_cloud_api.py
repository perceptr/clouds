import boto3
import os
import zipfile


class VkCloudAPI:
    """
    A class for working with the VK Cloud Object storage
    """
    def __init__(self):
        new_session = boto3.session.Session()
        self.session = new_session.client(
            service_name='s3',
            endpoint_url='https://hb.bizmrg.com',
            aws_access_key_id='w6ZvMqwisrKEeBq89FWAtE',
            aws_secret_access_key='89voBeu2QYr6XXPWDZMYfn1adgHG6KF1edwBTbVeoEKm'
        )

    def create_folder(self, folder_name: str) -> None:
        """
        Creates a folder in the cloud
        :param folder_name: name of the folder
        :return: None
        """
        self.session.put_object(Bucket='pyclouds', Key=folder_name + "/")

    def upload_file(self, path_to_file_on_pc: str, path_to_file_on_cloud: str, zipped: bool) -> None:
        """
        Uploads a file to the cloud
        :param path_to_file_on_pc: path to the file on the PC
        :param path_to_file_on_cloud: path to the file on the cloud
        :param zipped: if the file should be zipped
        :return: None
        """
        if zipped:
            with zipfile.ZipFile(path_to_file_on_pc + ".zip", "w") as zip_file:
                zip_file.write(path_to_file_on_pc)
            with open(path_to_file_on_pc + ".zip", 'rb') as zip_file:
                self.session.put_object(Bucket='pyclouds', Key=path_to_file_on_cloud, Body=zip_file)
            os.remove(path_to_file_on_pc + ".zip")
        else:
            self.session.upload_file(path_to_file_on_pc, 'pyclouds', path_to_file_on_cloud)

    def delete_file(self, path_to_file_on_cloud: str) -> None:
        """
        Deletes a file from the cloud
        :param path_to_file_on_cloud: path to the file on the cloud
        :return: None
        """
        self.session.delete_object(Bucket='pyclouds', Key=path_to_file_on_cloud)

    def download_file(self, path_to_file_on_cloud: str, path_to_file_on_pc: str) -> None:
        """
        Downloads a file from the cloud
        :param path_to_file_on_cloud: path to the file on the cloud
        :param path_to_file_on_pc: path to the file on the PC
        :return: None
        """
        self.session.download_file('pyclouds', path_to_file_on_cloud, path_to_file_on_pc)

    def get_all_files_list(self) -> None:
        """
        Returns a list of all files in the cloud
        :return: list of all files in the cloud
        """
        json_data = self.session.list_objects(Bucket='pyclouds')
        try:
            for file in json_data["Contents"]:
                print(file["Key"])
        except KeyError:
            print("No files in the cloud")

    def upload_directory(self, uploading_from: str, uploading_to: str, zipped: bool) -> None:
        """
        Uploads a directory to the cloud
        :param uploading_from: path to the directory on the PC
        :param uploading_to: path to the directory on the cloud
        :param zipped: if the directory should be zipped
        :return: None
        """
        if zipped:
            with zipfile.ZipFile(uploading_from + ".zip", "w") as zip_file:
                for root, dirs, files in os.walk(uploading_from):
                    for file in files:
                        zip_file.write(os.path.join(root, file))

                self.upload_file(uploading_from + ".zip", uploading_to + "/" + uploading_from.split("/")[-1],
                                 zipped=False)
                os.remove(uploading_from + ".zip")
                return

        based_folder = uploading_from[0:len(uploading_from) - len(uploading_from.split("/")[-1]) - 1]
        for address, dirs, files in os.walk(uploading_from):
            current_route = uploading_to + address[len(based_folder)::] + "/"
            files_except_hidden = list(filter(lambda x: x[0] != ".", files))
            for file in files_except_hidden:
                self.upload_file(address + "/" + file, current_route + file, zipped=False)

    def download_directory(self, downloading_from: str, downloading_to: str) -> None:
        """
        Downloads a directory from the cloud
        :param downloading_from: path to the directory on the cloud
        :param downloading_to: path to the directory on the PC
        :return: None
        """
        based_folder = downloading_from[0:len(downloading_from) - len(downloading_from.split("/")[-1]) - 1]
        for address, dirs, files in os.walk(downloading_from):
            current_route = downloading_to + address[len(based_folder)::] + "/"
            files_except_hidden = list(filter(lambda x: x[0] != ".", files))
            for file in files_except_hidden:
                self.download_file(address + "/" + file, current_route + file)
