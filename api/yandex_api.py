import requests
import os
import zipfile


class YandexAPI:
    """
    Yandex Disk API class with all methods for working with Yandex Disk
    """
    def __init__(self, url: str, token: str):
        """
        :param url: url to Yandex Disk
        :param token: private user token
        """
        self.URL = url
        # token: "y0_AgAAAABkpnbQAADLWwAAAADPHaXMCTSyU3M8TwucAzOBNPZS6nGMg0A"
        # url: "https://cloud-api.yandex.net/v1/disk"
        self.TOKEN = token
        self.headers = {'Content-Type': 'application/json', 'Accept': 'application/json',
                        'Authorization': f'OAuth {token}'}

    def __get_file_meta_information(self, path: str) -> dict:
        """
        Returns meta information about file or folder
        :param: path: path to file or folder
        :return: dict: meta information
        """
        return requests.get(f"{self.URL}/resources?path={path}", headers=self.headers).json()

    def create_folder(self, path: str) -> int:
        """
        Creates folder on Yandex Disk
        :param path: path to create folder
        :return: int: 200 if folder created, 409 if folder already exists
        """
        resp = requests.put(f"{self.URL}/resources?path={path}", headers=self.headers)
        return resp.status_code

    def remove_folder_or_file(self, path: str, permanently=False) -> requests.Response:
        """
        Removes folder or file from Yandex Disk
        :param path: path to folder or file
        :param permanently: if True - removes permanently, if False - moves to trash
        :return: requests.Response
        """
        return requests.delete(f"{self.URL}/resources?path={path}&permanently={permanently}",
                               headers=self.headers)

    def move_folder_or_file(self, path_from: str, path_to: str) -> int:
        """
        Moves folder or file from path_from to path_to
        :param path_from: path to folder or file
        :param path_to: path to move folder or file
        :return: int
        """
        resp = requests.post(f"{self.URL}/resources/move?from={path_from}&path={path_to}",
                             headers=self.headers)
        return resp.status_code

    def get_user_disk_info_bytes(self) -> str:
        """
        Returns user disk info in bytes
        :return: str: user disk info in bytes
        """
        response = requests.get(url=self.URL, headers=self.headers).json()
        return f"Total space: {response['total_space']} bytes\nTrash size: {response['trash_size']} bytes\n" \
               f"Used space: {response['used_space']} bytes\n" \
               f"Free space: {response['total_space'] - response['used_space']} bytes"

    def copy_file_or_folder(self, path_from: str, path_to_create: str) -> requests.Response:
        """
        Copies file or folder from path_from to path_to_create
        :param path_from: path to file or folder
        :param path_to_create: path to create file or folder
        :return: requests.Response
        """
        return requests.post(f"{self.URL}/resources/copy/?from={path_from}&path={path_to_create}",
                             headers=self.headers)

    def get_files_list(self, limit: int = 20,
                       media_type: str = "audio,"
                                         "video,"
                                         "book,"
                                         "compressed,"
                                         "data,"
                                         "diskimage,"
                                         "document,"
                                         "encoded,"
                                         "image,"
                                         "web,"
                                         "unknown") -> None:
        """
        Prints files list
        :param limit: limit of files to print
        :param media_type: type of files to print
        :return: None
        """

        req = requests.get(f"{self.URL}/resources/files/?limit={limit}&media_type={media_type}",
                           headers=self.headers).json()

        for item in req["items"]:
            print(item["name"])

    def get_public_url(self, path_to_file_or_folder: str) -> str:
        """
        Returns public url for file or folder
        :param path_to_file_or_folder: path to file or folder
        :return: str: public url
        """
        requests.put(f"{self.URL}/resources/publish?path={path_to_file_or_folder}", headers=self.headers)
        return self.__get_file_meta_information(path_to_file_or_folder)["public_url"]

    def delete_public_url(self, path_to_file_or_folder: str) -> requests.Response:
        """
        Deletes public url for file or folder
        :param path_to_file_or_folder: path to file or folder
        :return: requests.Response
        """
        return requests.put(f"{self.URL}/resources/unpublish?path={path_to_file_or_folder}",
                            headers=self.headers)

    def __get_url_for_uploading(self, path_to_upload: str, replace=False) -> str:
        """
        Returns url for uploading file to Yandex Disk
        :param path_to_upload: path to upload file
        :param replace: if True - replaces file if exists, if False - creates new file
        :return: str: url for uploading file
        """
        return requests.get(f'{self.URL}/resources/upload?path={path_to_upload}&overwrite={replace}',
                            headers=self.headers).json()["href"]

    def upload_file(self, path_to_file: str, path_to_folder_on_yadisk: str, zipped=False, replace=False) -> int:
        """
        Uploads file to Yandex Disk

        !!!uploading to goes with file_name.extension!!!
        :param path_to_file: path to file
        :param path_to_folder_on_yadisk: path to folder on Yandex Disk
        :param zipped: if True - zips file before uploading
        :param replace: if True - replaces file if exists, if False - creates new file
        :return: int
        """
        res = self.__get_url_for_uploading(path_to_folder_on_yadisk, replace)
        with open(path_to_file, 'rb') as f:
            try:
                if zipped:
                    with zipfile.ZipFile(path_to_file + ".zip", "w") as zip_file:
                        zip_file.write(path_to_file)
                    with open(path_to_file + ".zip", 'rb') as zip_file:
                        resp = requests.put(res, files={'file': zip_file})
                    os.remove(path_to_file + ".zip")
                    return resp.status_code
                else:
                    resp = requests.put(res, files={'file': f})
                    return resp.status_code
            except KeyError:
                print(res)

    def clean_trash(self) -> int:
        """
        Cleans trash
        :return: int
        """
        resp = requests.delete(f"{self.URL}/trash/resources?path=", headers=self.headers)
        return resp.status_code

    def __get_url_for_downloading(self, path_to_download_from: str) -> str:
        """
        Returns url for downloading file from Yandex Disk
        :param path_to_download_from: path to download file from
        :return: str: url for downloading file
        """
        return requests.get(f"{self.URL}/resources/download?path={path_to_download_from}",
                            headers=self.headers).json()["href"]

    def download_file(self, path_to_downloading_file: str, save_directory: str) -> int:
        """
        Downloads file from Yandex Disk
        :param path_to_downloading_file: path to downloading file
        :param save_directory: path to save file
        :return: int
        """

        try:
            resp = requests.get(self.__get_url_for_downloading(path_to_downloading_file))
            got_file = resp.content
            with open(save_directory + "/" + path_to_downloading_file.split("/")[-1], "wb") as file:
                file.write(got_file)
            return resp.status_code

        except KeyError:
            raise Exception(f"Failed to download file {path_to_downloading_file}!")

    def get_info_about_file_or_folder(self, path_to_file_or_folder: str) -> None:
        """
        Prints info about file or folder
        :param path_to_file_or_folder: path to file or folder
        :return: None
        """
        response = requests.get(f"{self.URL}/resources?path={path_to_file_or_folder}", headers=self.URL).json()
        items = response["_embedded"]["items"]
        for i in range(len(items)):
            print(f"{i + 1})Name: {items[i]['name']}, Type: {items[i]['type']}")

    @staticmethod
    def __get_newest_folder(based: str, way: str) -> str:
        """
        Returns the newest folder in path
        :param based: path to folder
        :param way: path to folder
        :return: str: newest folder
        """
        return way[len(based)::] + "/"

    def upload_directory(self, uploading_from: str, uploading_to: str, zipped: bool) -> None:
        """
        Uploads directory to Yandex Disk
        :param uploading_from: path to uploading directory
        :param uploading_to: path to uploading directory on Yandex Disk
        :param zipped: if True - zips directory before uploading
        :return: None
        """
        based_folder = uploading_from[0:len(uploading_from) - len(uploading_from.split("/")[-1]) - 1]
        if zipped:
            with zipfile.ZipFile(uploading_from + ".zip", "w") as zip_file:
                for root, dirs, files in os.walk(uploading_from):
                    for file in files:
                        zip_file.write(os.path.join(root, file))

                self.upload_file(uploading_from + ".zip", uploading_to + "/" + uploading_from.split("/")[-1],
                                 zipped=False)
                os.remove(uploading_from + ".zip")
                return

        for address, dirs, files in os.walk(uploading_from):
            current_route = uploading_to + self.__get_newest_folder(based_folder, address)
            self.create_folder(current_route)
            files_except_hidden = list(filter(lambda x: x[0] != ".", files))
            for file in files_except_hidden:
                self.upload_file(address + "/" + file, current_route + file)
