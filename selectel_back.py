import requests
import os


def get_auth_token():
    url = "https://api.selcdn.ru/v2.0/tokens"
    headers = {"Content-type": "application/json"}
    data = {"auth": {"passwordCredentials": {"username": r"230657", "password": r"99Qu0@RK0c"}}}

    return requests.post(url, json=data, headers=headers).json()["access"]["token"]["id"]


def download_file(path_to_downloading_file: str, save_directory: str):
    # download_file("https://api.selcdn.ru/v1/SEL_230657/pycloudstorage/meadow.jpeg",
    #               "/Users/arsenii/Desktop/dsk/pyCourse/cloudsrep/clouds/downloaded_pics")

    headers = {"X-Auth-Token": get_auth_token()}
    res = requests.get("https://api.selcdn.ru/v1/SEL_230657/pycloudstorage/meadow.jpeg", headers=headers)
    print(res.status_code)
    try:
        got_file = res.content
        with open(save_directory + "/" + path_to_downloading_file.split("/")[-1], "wb") as file:
            file.write(got_file)
    except KeyError:
        raise Exception(f"Failed to download file {path_to_downloading_file}!")


def upload_file(path_to_file_pc: str, selectel_path_to_folder: str):
    file_name = path_to_file_pc.split("/")[-1]
    url = "https://api.selcdn.ru/v1/SEL_230657/pycloudstorage" + selectel_path_to_folder + "/" + file_name
    headers = {"X-Auth-Token": get_auth_token()}
    with open(path_to_file_pc, 'rb') as file:
        try:
            requests.put(url, headers=headers, files={'file': file})
        except KeyError:
            print("Failed uploading file")


def get_all_files_list():
    url = "https://api.selcdn.ru/v1/SEL_230657/pycloudstorage"
    headers = {"X-Auth-Token": get_auth_token()}

    return requests.get(url, headers=headers).text


def upload_directory_selectel(uploading_from: str, uploading_to: str):
    # upload_directory_selectel("/Users/arsenii/Desktop/dsk/pyCourse/pics_for_clouds", "/")
    based_folder = uploading_from[0:len(uploading_from) - len(uploading_from.split("/")[-1]) - 1]
    for address, dirs, files in os.walk(uploading_from):
        current_route = uploading_to + address[len(based_folder)::] + "/"
        files_except_hidden = list(filter(lambda x: x[0] != ".", files))
        for file in files_except_hidden:
            upload_file(address + "/" + file, current_route + file)


# upload_directory_selectel("/Users/arsenii/Desktop/dsk/pyCourse/pics_for_clouds", "/")
