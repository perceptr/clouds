import argparse
import yandex_api
import selectel_api
import vk_cloud_api as vk_api

parser = argparse.ArgumentParser(
            'PyClouds',
            description='PyClouds - App for Clouds',
            epilog='Thank you for choosing PyClouds!',
            add_help=True,
            )

parser.add_argument("--upload_file", help="enter the way to file you want to upload: /a/b/file.ext")
parser.add_argument("--upload_directory", help="enter the way to directory you want to upload /a/b/dir")
parser.add_argument("--dir_up", help="enter the way you want to upload your file or directory")

parser.add_argument("--dir_down", help="enter the way you want to download file")
parser.add_argument("--download_file", help="enter the way to file you want to download")
parser.add_argument("-p", "--platform", help="put y (or yandex) / s (or selectel) /"
                                             " or v (vk) when managing files")

parser.add_argument("-i", "--info", action="store_true", help="show all files in cloud")
parser.add_argument("-z", "--zip", help="zip file or directory")

args = parser.parse_args()


def create_yadisk(url="https://cloud-api.yandex.net/v1/disk",
                  token="y0_AgAAAABkpnbQAADLWwAAAADPHaXMCTSyU3M8TwucAzOBNPZS6nGMg0A") -> yandex_api.MyYaDiskAPI:
    """
    Creates yandex disk object
    :param url: url to yandex disk
    :param token: token to yandex disk
    :return: yandex disk object
    """

    return yandex_api.MyYaDiskAPI(url, token)


def upload_file(path_to_file: str, path_to_upload_disk: str, platform: str, zipped=False) -> None:
    """
    Uploads file to cloud
    :param path_to_file: path to file on your pc
    :param path_to_upload_disk:  path to upload file on cloud
    :param platform: cloud platform
    :param zipped: if you want to zip file, just print -z zip
    :return: void
    """
    if platform == "y" or platform == "yandex":
        my_disk = create_yadisk()
        my_disk.upload_file(path_to_file, path_to_upload_disk, zipped)
    elif platform == "s" or platform == "selectel":
        selectel_api.SelectelAPI.upload_file(path_to_file, path_to_upload_disk, zipped)
    elif platform == "v" or platform == "vk":
        vk = vk_api.VkCloudAPI()
        vk.upload_file(path_to_file, path_to_upload_disk, zipped)
    else:
        raise Exception("Wrong input, try again!")


def upload_directory(uploading_from_pc_dir: str, uploading_to_disk_path: str, platform: str, zip_arg: str) -> None:
    """
    Uploads directory to cloud
    :param uploading_from_pc_dir: path to directory on your pc
    :param uploading_to_disk_path: path to upload directory on cloud
    :param platform: cloud platform
    :param zip_arg: if you want to zip directory, just print -z zip
    :return: void
    """
    zipped = zip_arg == "zip"
    if platform == "y" or platform == "yandex":
        my_disk = create_yadisk()
        my_disk.upload_directory(uploading_from_pc_dir, uploading_to_disk_path, zipped)
    elif platform == "s" or platform == "selectel":
        selectel_api.SelectelAPI.upload_directory(uploading_from_pc_dir, uploading_to_disk_path, zipped)
    elif platform == "v" or platform == "vk":
        vk = vk_api.VkCloudAPI()
        vk.upload_directory(uploading_from_pc_dir, uploading_to_disk_path, zipped)
    else:
        raise Exception("Wrong platform, try again!")


def download_file(path_to_downloading_file: str, save_directory: str, platform: str) -> None:
    """
    Downloads file from cloud
    :param path_to_downloading_file: path to file on cloud
    :param save_directory: path to save file on your pc
    :param platform: cloud platform
    :return: void
    """
    if platform == "y" or platform == "yandex":
        my_disk = create_yadisk()
        my_disk.download_file(path_to_downloading_file, save_directory)
    elif platform == "s" or platform == "selectel":
        selectel_api.SelectelAPI.download_file(path_to_downloading_file, save_directory)
    elif platform == "v" or platform == "vk":
        vk = vk_api.VkCloudAPI()
        vk.download_file(path_to_downloading_file, save_directory)
    else:
        raise Exception("Wrong arguments entered!")


def get_files_list(platform: str) -> None:
    """
    Shows all files in cloud
    :param platform: cloud platform
    :return: void
    """
    if platform == "y" or platform == "yandex":
        my_disk = create_yadisk()
        my_disk.get_files_list()
    elif platform == "s" or platform == "selectel":
        selectel_api.SelectelAPI.get_all_files_list()
    elif platform == "v" or platform == "vk":
        vk = vk_api.VkCloudAPI()
        vk.get_all_files_list()


if args.upload_file and args.dir_up and args.platform and args.zip:
    upload_file(args.upload_file, args.dir_up, args.platform, args.zip)
elif args.upload_file and args.dir_up and args.platform:
    upload_file(args.upload_file, args.dir_up, args.platform)
elif args.upload_directory and args.dir_up and args.platform:
    upload_directory(args.upload_directory, args.dir_up, args.platform, args.zip)
elif args.upload_directory and args.dir_up and args.platform and args.zip:
    upload_directory(args.upload_directory, args.dir_up, args.platform, args.zip)
elif args.download_file and args.dir_down and args.platform:
    download_file(args.download_file, args.dir_down, args.platform)
elif args.info and args.platform:
    get_files_list(args.platform)
