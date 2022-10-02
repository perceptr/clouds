import requests
import os
import zipfile

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
    def upload_file(path_to_file_pc: str, selectel_path_to_folder: str, zipped=False):
        file_name = path_to_file_pc.split("/")[-1]
        url = "https://api.selcdn.ru/v1/SEL_230657/pycloudstorage" + selectel_path_to_folder + "/" + file_name
        headers = {"X-Auth-Token": SelectelAPI.__get_auth_token()}
        with open(path_to_file_pc, 'rb') as file:
            try:
                if zipped:
                    with zipfile.ZipFile(file_name + ".zip", "w") as zip_file:
                        zip_file.write(file_name)
                    with open(file_name + ".zip", 'rb') as zip_file:
                        requests.put(url, headers=headers, files={'file': zip_file})
                    os.remove(file_name + ".zip")
                else:
                    requests.put(url, headers=headers, files={'file': file})
            except KeyError:
                print("Failed uploading file")

    @staticmethod
    def get_all_files_list():
        url = "https://api.selcdn.ru/v1/SEL_230657/pycloudstorage"
        headers = {"X-Auth-Token": SelectelAPI.__get_auth_token()}

        print(requests.get(url, headers=headers).text)

    @staticmethod
    def upload_directory(uploading_from: str, uploading_to: str, zipped: bool):
        # upload_directory_selectel("/Users/arsenii/Desktop/dsk/pyCourse/pics_for_clouds", "/")
        if zipped:
            with zipfile.ZipFile(uploading_from + ".zip", "w") as zip_file:
                for root, dirs, files in os.walk(uploading_from):
                    for file in files:
                        zip_file.write(os.path.join(root, file))

                SelectelAPI.upload_file(uploading_from + ".zip", uploading_to + "/" + uploading_from.split("/")[-1],
                                        zipped=False)
                os.remove(uploading_from + ".zip")
                return

        based_folder = uploading_from[0:len(uploading_from) - len(uploading_from.split("/")[-1]) - 1]
        for address, dirs, files in os.walk(uploading_from):
            current_route = uploading_to + address[len(based_folder)::] + "/"
            files_except_hidden = list(filter(lambda x: x[0] != ".", files))
            for file in files_except_hidden:
                SelectelAPI.upload_file(address + "/" + file, current_route + file)


# upload_directory_selectel("/Users/arsenii/Desktop/dsk/pyCourse/pics_for_clouds", "/")

