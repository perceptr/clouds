import yandex_back
import os


def upload_directory(uploading_from: str, uploading_to: str):
    # upload_directory("/Users/arsenii/Desktop/dsk/pyCourse/pics_for_clouds/", "f4/f6/")
    all_files_from_directory = \
        list(filter(lambda x: x[0] != ".", os.listdir(uploading_from)))
    for file in all_files_from_directory:
        yandex_back.upload_file(uploading_from+"/"+file, uploading_to+file)



