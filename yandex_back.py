import requests

URL = "https://cloud-api.yandex.net/v1/disk"
TOKEN = "y0_AgAAAABkpnbQAADLWwAAAADPHaXMCTSyU3M8TwucAzOBNPZS6nGMg0A"
headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': f'OAuth {TOKEN}'}


def get_file_meta_information(path: str):
    return requests.get(f"{URL}/resources?path={path}", headers=headers).json()


def create_folder(path: str):
    resp = requests.put(f"{URL}/resources?path={path}", headers=headers)
    return resp.status_code  # 201 success


def remove_folder_or_file(path: str, permanently=False):
    return requests.delete(f"{URL}/resources?path={path}&permanently={permanently}", headers=headers)


def move_folder_or_file(path_from: str, path_to: str):
    resp = requests.post(f"{URL}/resources/move?from={path_from}&path={path_to}", headers=headers)
    # "/bears", "/f4/bears/"
    return resp.status_code, resp.url


def get_user_disk_info_bytes() -> dict[str: int]:
    return requests.get(url=URL, headers=headers).json()


def copy_file_or_folder(path_from: str, path_to_create: str):
    # "/f4/Море.jpg", "/f4/Море2.jpg"
    return requests.post(f"{URL}/resources/copy/?from={path_from}&path={path_to_create}", headers=headers)


def get_files_list(limit: int = 20,
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
    return requests.get(f"{URL}/resources/files/?limit={limit}&media_type={media_type}", headers=headers).json()


def get_public_url(path_to_file_or_folder: str) -> str:
    requests.put(f"{URL}/resources/publish?path={path_to_file_or_folder}", headers=headers)
    return get_file_meta_information(path_to_file_or_folder)["public_url"]


def delete_public_url(path_to_file_or_folder: str):
    return requests.put(f"{URL}/resources/unpublish?path={path_to_file_or_folder}", headers=headers)


def __get_url_for_uploading(path_to_upload: str, replace=False) -> str:
    return requests.get(f'{URL}/resources/upload?path={path_to_upload}&overwrite={replace}',
                        headers=headers).json()["href"]


def upload_file(path_to_file: str, path_to_folder_on_yadisk: str, replace=False):
    # upload_file("beach.jpeg", "/f131/пляж")
    res = __get_url_for_uploading(path_to_folder_on_yadisk, replace)
    with open(path_to_file, 'rb') as f:
        try:
            requests.put(res, files={'file': f})
        except KeyError:
            print(res)


def clean_trash():
    return requests.delete(f"{URL}/trash/resources?path=", headers=headers)


def __get_url_for_downloading(path_to_download_from: str) -> str:
    return requests.get(f"{URL}/resources/download?path={path_to_download_from}", headers=headers).json()["href"]


def download_file(file_name: str, save_directory: str):
    # download_file("meadow2213.jpeg", "/Users/arsenii/Desktop/dsk/pyCourse/cloudsrep/clouds/downloaded_pics")
    try:
        got_file = requests.get(__get_url_for_downloading(file_name)).content
        with open(save_directory+"/"+file_name, "wb") as file:
            file.write(got_file)
    except KeyError:
        raise Exception(f"Failed to download file {file_name}!")



