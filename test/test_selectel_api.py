import unittest
import responses
from api.selectel_api import SelectelAPI
import requests
import zipfile
import os


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.sel_api = SelectelAPI
        self.token = SelectelAPI.get_auth_token()

    @responses.activate
    def test_upload_file(self, zipped=False):
        responses.add(responses.PUT, "https://api.selcdn.ru/v1/SEL_230657/pycloudstorage/f4/beach.jpeg",
                      status=200)
        file_name = "beach.jpeg".split("/")[-1]
        url = "https://api.selcdn.ru/v1/SEL_230657/pycloudstorage" + "/f4" + "/" + file_name
        headers = {"X-Auth-Token": "SelectelAPI.get_auth_token()"}
        with open("beach.jpeg", 'rb') as file:
            try:
                if zipped:
                    with zipfile.ZipFile(file_name + ".zip", "w") as zip_file:
                        zip_file.write(file_name)
                    with open(file_name + ".zip", 'rb') as zip_file:
                        resp = requests.put(url, headers=headers, files={'file': zip_file})
                    os.remove(file_name + ".zip")
                else:
                    resp = requests.put(url, headers=headers, files={'file': file})
            except KeyError:
                print("Failed uploading file")
                return 418

        self.assertEqual(resp.status_code, 200)
        return resp.status_code == 200

    @responses.activate
    def test_upload_file_with_zip(self):
        self.assertEqual(self.test_upload_file(True), True)

    @responses.activate
    def test_get_all_files_list(self):
        responses.add(responses.GET, "https://api.selcdn.ru/v1/SEL_230657/pycloudstorage",
                      status=200)
        url = "https://api.selcdn.ru/v1/SEL_230657/pycloudstorage"
        headers = {"X-Auth-Token": "SelectelAPI.get_auth_token()"}
        resp = requests.get(url, headers=headers)
        self.assertEqual(resp.status_code, 200)
        return resp.status_code == 200


if __name__ == '__main__':
    unittest.main()
