import yandex_back
import os


def __get_newest_folder(based: str, way: str) -> str:
    return way[len(based)::] + "/"


def upload_directory(uploading_from: str, uploading_to: str):
    # upload_directory("/Users/arsenii/Desktop/dsk/pyCourse/pics_for_clouds", "/f7")
    based_folder = uploading_from[0:len(uploading_from) - len(uploading_from.split("/")[-1]) - 1]
    for address, dirs, files in os.walk(uploading_from):
        current_route = uploading_to + __get_newest_folder(based_folder, address)
        yandex_back.create_folder(current_route)
        files_except_hidden = list(filter(lambda x: x[0] != ".", files))
        for file in files_except_hidden:
            yandex_back.upload_file(address + "/" + file, current_route + file)

