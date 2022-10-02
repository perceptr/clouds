import requests
import os


class MyYaDiskAPI:
    def __init__(self, url: str, token: str):
        self.URL = url
        # "y0_AgAAAABkpnbQAADLWwAAAADPHaXMCTSyU3M8TwucAzOBNPZS6nGMg0A"
        # "https://cloud-api.yandex.net/v1/disk"
        self.TOKEN = token
        self.headers = {'Content-Type': 'application/json', 'Accept': 'application/json',
                        'Authorization': f'OAuth {token}'}

    def __get_file_meta_information(self, path: str):
        return requests.get(f"{self.URL}/resources?path={path}", headers=self.headers).json()

    def create_folder(self, path: str):
        resp = requests.put(f"{self.URL}/resources?path={path}", headers=self.headers)
        return resp.status_code

    def remove_folder_or_file(self, path: str, permanently=False):
        return requests.delete(f"{self.URL}/resources?path={path}&permanently={permanently}",
                               headers=self.headers)

    def move_folder_or_file(self, path_from: str, path_to: str):
        return requests.post(f"{self.URL}/resources/move?from={path_from}&path={path_to}",
                             headers=self.headers)
        # "/bears", "/f4/bears/"

    def get_user_disk_info_bytes(self) -> str:
        response = requests.get(url=self.URL, headers=self.headers).json()
        return f"Total space: {response['total_space']} bytes\nTrash size: {response['trash_size']} bytes\n" \
               f"Used space: {response['used_space']} bytes\n" \
               f"Free space: {response['total_space'] - response['used_space']} bytes"

    def copy_file_or_folder(self, path_from: str, path_to_create: str):
        # "/f4/Море.jpg", "/f4/Море2.jpg"
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
                                         "unknown"):
        # print(get_files_list(20, "video")["items"][0]["name"])
        # for el in get_files_list(20)["items"]:
        #     print(el["name"])

        req = requests.get(f"{self.URL}/resources/files/?limit={limit}&media_type={media_type}",
                           headers=self.headers).json()

        for item in req["items"]:
            print(item["name"])

    def get_public_url(self, path_to_file_or_folder: str) -> str:
        requests.put(f"{self.URL}/resources/publish?path={path_to_file_or_folder}", headers=self.headers)
        return self.__get_file_meta_information(path_to_file_or_folder)["public_url"]

    def delete_public_url(self, path_to_file_or_folder: str):
        return requests.put(f"{self.URL}/resources/unpublish?path={path_to_file_or_folder}",
                            headers=self.headers)

    def __get_url_for_uploading(self, path_to_upload: str, replace=False) -> str:
        print(f"{self.URL}/resources/upload?path={path_to_upload}&overwrite={replace}'")
        return requests.get(f'{self.URL}/resources/upload?path={path_to_upload}&overwrite={replace}',
                            headers=self.headers).json()["href"]

    def upload_file(self, path_to_file: str, path_to_folder_on_yadisk: str, replace=False):
        # upload_file("beach.jpeg", "/f131/пляж")
        # upload_file("/Users/arsenii/Desktop/dsk/pyCourse/pics_for_clouds/test_folder/too/mustang.jpeg",
        # "/f4/f6/mustang_a.jpeg")
        # !!!uploading to goes with file_name.extension!!!
        res = self.__get_url_for_uploading(path_to_folder_on_yadisk, replace)
        with open(path_to_file, 'rb') as f:
            try:
                requests.put(res, files={'file': f})
            except KeyError:
                print(res)

    def clean_trash(self):
        return requests.delete(f"{self.URL}/trash/resources?path=", headers=self.headers)

    def __get_url_for_downloading(self, path_to_download_from: str) -> str:
        return requests.get(f"{self.URL}/resources/download?path={path_to_download_from}",
                            headers=self.headers).json()["href"]

    def download_file(self, path_to_downloading_file: str, save_directory: str):
        # download_file("meadow2213.jpeg", "/Users/arsenii/Desktop/dsk/pyCourse/cloudsrep/clouds/downloaded_pics")
        try:
            got_file = requests.get(self.__get_url_for_downloading(path_to_downloading_file)).content
            with open(save_directory + "/" + path_to_downloading_file.split("/")[-1], "wb") as file:
                file.write(got_file)
        except KeyError:
            raise Exception(f"Failed to download file {path_to_downloading_file}!")

    def get_info_about_file_or_folder(self, path_to_file_or_folder: str):
        # get_info_about_file_or_folder("/")
        response = requests.get(f"{self.URL}/resources?path={path_to_file_or_folder}", headers=self.URL).json()
        items = response["_embedded"]["items"]
        for i in range(len(items)):
            print(f"{i + 1})Name: {items[i]['name']}, Type: {items[i]['type']}")

    @staticmethod
    def __get_newest_folder(based: str, way: str) -> str:
        return way[len(based)::] + "/"

    def upload_directory(self, uploading_from: str, uploading_to: str):
        # upload_directory("/Users/arsenii/Desktop/dsk/pyCourse/pics_for_clouds", "/f7")
        based_folder = uploading_from[0:len(uploading_from) - len(uploading_from.split("/")[-1]) - 1]
        for address, dirs, files in os.walk(uploading_from):
            current_route = uploading_to + self.__get_newest_folder(based_folder, address)
            self.create_folder(current_route)
            files_except_hidden = list(filter(lambda x: x[0] != ".", files))
            for file in files_except_hidden:
                self.upload_file(address + "/" + file, current_route + file)


