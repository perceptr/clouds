import argparse
import yandex_api
import selectel_api

parser = argparse.ArgumentParser(
            'PyClouds',
            description='PyClouds - App for Clouds',
            epilog='Thank you for choosing PyClouds!',
            add_help=False,
            )

parser.add_argument("--upload_file", help="enter the way to file you want to upload: /a/b/file.ext")
parser.add_argument("--upload_directory", help="enter the way to directory you want to upload /a/b/dir")
parser.add_argument("--dir_up", help="enter the way you want to upload your file or directory")

parser.add_argument("--dir_down", help="enter the way you want to download file")
parser.add_argument("--download_file", help="enter the way to file you want to download")

parser.add_argument("-p", "--platform", help="put y (or yandex) / s (or selectel) when managing files")

parser.add_argument("-i", "--info", help="enter this tp get files list")
args = parser.parse_args()


def create_yadisk(url="https://cloud-api.yandex.net/v1/disk",
                  token="y0_AgAAAABkpnbQAADLWwAAAADPHaXMCTSyU3M8TwucAzOBNPZS6nGMg0A") -> yandex_api.MyYaDiskAPI:

    return yandex_api.MyYaDiskAPI(url, token)


def upload_file(path_to_file: str, path_to_upload_disk: str, platform: str):
    if platform == "y" or platform == "yandex":
        my_disk = create_yadisk()
        my_disk.upload_file(path_to_file, path_to_upload_disk)
    elif platform == "s" or platform == "selectel":
        selectel_api.SelectelAPI.upload_file(path_to_file, path_to_upload_disk)
    else:
        raise Exception("Wrong platform, try again!")


def upload_directory(uploading_from_pc_dir: str, uploading_to_disk_path: str, platform: str):
    if platform == "y" or platform == "yandex":
        my_disk = create_yadisk()
        my_disk.upload_directory(uploading_from_pc_dir, uploading_to_disk_path)
    elif platform == "s" or platform == "selectel":
        selectel_api.SelectelAPI.upload_directory(uploading_from_pc_dir, uploading_to_disk_path)
    else:
        raise Exception("Wrong platform, try again!")


def download_file(path_to_downloading_file: str, save_directory: str, platform: str):
    if platform == "y" or platform == "yandex":
        my_disk = create_yadisk()
        my_disk.download_file(path_to_downloading_file, save_directory)
    elif platform == "s" or platform == "selectel":
        selectel_api.SelectelAPI.download_file(path_to_downloading_file, save_directory)
    else:
        raise Exception("Wrong arguments entered!")


def get_files_list(platform: str, info: str):
    if (platform == "y" or platform == "yandex") and info == "get":
        my_disk = create_yadisk()
        my_disk.get_files_list()
    elif (platform == "s" or platform == "selectel") and info == "get":
        selectel_api.SelectelAPI.get_all_files_list()


if args.upload_file and args.dir_up and args.platform:
    upload_file(args.upload_file, args.dir_up, args.platform)
elif args.upload_directory and args.dir_up and args.platform:
    upload_directory(args.upload_directory, args.dir_up, args.platform)
elif args.download_file and args.dir_down and args.platform:
    download_file(args.download_file, args.dir_down, args.platform)
elif args.info and args.platform:
    get_files_list(args.platform, args.info)


# download_file("meadow2213.jpeg", "/Users/arsenii/Desktop/dsk/pyCourse/cloudsrep/clouds/downloaded_pics")

# upload_file("/Users/arsenii/Desktop/dsk/pyCourse/pics_for_clouds/test_folder/too/mustang.jpeg",
# "/f4/f7/mustang_a.jpeg")

# upload_directory("/Users/arsenii/Desktop/dsk/pyCourse/pics_for_clouds", "/f4/f7/f8")

