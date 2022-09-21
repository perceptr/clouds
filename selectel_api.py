import requests
import os


class SelectelAPI:
    @staticmethod
    def __get_auth_token() -> str:
        url = "https://api.selcdn.ru/v2.0/tokens"
        headers = {"Content-type": "application/json"}
        data = {"auth": {"passwordCredentials": {"username": r"230657", "password": r"99Qu0@RK0c"}}}

        return requests.post(url, json=data, headers=headers).json()["access"]["token"]["id"]

    @staticmethod
    def download_file(path_to_downloading_file: str, save_directory: str):
        # download_file("https://api.selcdn.ru/v1/SEL_230657/pycloudstorage/meadow.jpeg",
        #               "/Users/arsenii/Desktop/dsk/pyCourse/cloudsrep/clouds/downloaded_pics")

        headers = {"X-Auth-Token": SelectelAPI.__get_auth_token()}
        res = requests.get(f"https://api.selcdn.ru/v1/SEL_230657/pycloudstorage/{path_to_downloading_file}",
                           headers=headers)

        try:
            got_file = res.content
            with open(save_directory + "/" + path_to_downloading_file.split("/")[-1], "wb") as file:
                file.write(got_file)
        except KeyError:
            raise Exception(f"Failed to download file {path_to_downloading_file}!")

    @staticmethod
    def upload_file(path_to_file_pc: str, selectel_path_to_folder: str):
        file_name = path_to_file_pc.split("/")[-1]
        url = "https://api.selcdn.ru/v1/SEL_230657/pycloudstorage" + selectel_path_to_folder + "/" + file_name
        headers = {"X-Auth-Token": SelectelAPI.__get_auth_token()}
        with open(path_to_file_pc, 'rb') as file:
            try:
                requests.put(url, headers=headers, files={'file': file})
            except KeyError:
                print("Failed uploading file")

    @staticmethod
    def get_all_files_list() -> str:
        url = "https://api.selcdn.ru/v1/SEL_230657/pycloudstorage"
        headers = {"X-Auth-Token": SelectelAPI.__get_auth_token()}

        return requests.get(url, headers=headers).text

    @staticmethod
    def upload_directory(uploading_from: str, uploading_to: str):
        # upload_directory_selectel("/Users/arsenii/Desktop/dsk/pyCourse/pics_for_clouds", "/")
        based_folder = uploading_from[0:len(uploading_from) - len(uploading_from.split("/")[-1]) - 1]
        for address, dirs, files in os.walk(uploading_from):
            current_route = uploading_to + address[len(based_folder)::] + "/"
            files_except_hidden = list(filter(lambda x: x[0] != ".", files))
            for file in files_except_hidden:
                SelectelAPI.upload_file(address + "/" + file, current_route + file)


# upload_directory_selectel("/Users/arsenii/Desktop/dsk/pyCourse/pics_for_clouds", "/")

