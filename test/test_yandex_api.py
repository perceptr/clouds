import unittest
from api.yandex_api import YandexAPI
import responses


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.ya_api = YandexAPI("https://cloud-api.yandex.net/v1/disk",
                                "y0_AgAAAABkpnbQAADLWwAAAADPHaXMCTSyU3M8TwucAzOBNPZS6nGMg0A")

    @responses.activate
    def test_yandex_create_folder(self):
        responses.add(responses.PUT,
                      'https://cloud-api.yandex.net/v1/disk/resources',
                      json={
                          "href": "string",
                          "method": "string",
                          "templated": True},
                      status=201)

        response = self.ya_api.create_folder("/f45")
        self.assertEqual(response, 201)

    @responses.activate
    def test_yandex_create_folder_unauth(self):
        responses.add(responses.PUT,
                      'https://cloud-api.yandex.net/v1/disk/resources',
                      json={
                          "message": "string",
                          "description": "string",
                          "error": "string"},
                      status=401)

        response = self.ya_api.create_folder("/f45")
        self.assertEqual(response, 401)

    @responses.activate
    def test_yandex_clean_trash(self):
        responses.add(responses.DELETE,
                      'https://cloud-api.yandex.net/v1/disk/trash/resources',
                      json={
                          "href": "string",
                          "method": "string",
                          "templated": True},
                      status=202)

        response = self.ya_api.clean_trash()
        self.assertEqual(response, 202)

    @responses.activate
    def test_yandex_clean_trash_unauth(self):
        responses.add(responses.DELETE,
                      'https://cloud-api.yandex.net/v1/disk/trash/resources',
                      json={
                          "message": "string",
                          "description": "string",
                          "error": "string"},
                      status=401)

        response = self.ya_api.clean_trash()
        self.assertEqual(response, 401)

    @responses.activate
    def test_yandex_move_folder_or_file(self):
        responses.add(responses.POST,
                      'https://cloud-api.yandex.net/v1/disk/resources/move',
                      json={
                          "href": "string",
                          "method": "string",
                          "templated": True},
                      status=202)

        response = self.ya_api.move_folder_or_file("/f45", "/f45")

        self.assertEqual(response, 202)

    @responses.activate
    def test_yandex_move_folder_or_file_unauth(self):
        responses.add(responses.POST,
                      'https://cloud-api.yandex.net/v1/disk/resources/move',
                      json={
                          "message": "string",
                          "description": "string",
                          "error": "string"},
                      status=401)

        response = self.ya_api.move_folder_or_file("/f45", "/f45")

        self.assertEqual(response, 401)

    @responses.activate
    def test_yandex_copy_file_or_folder(self):
        responses.add(responses.POST,
                      f"{self.ya_api.URL}/resources/copy/?from=/basic_pics&path=/f45",
                      json={
                          "href": "string",
                          "method": "string",
                          "templated": True},
                      status=201)

        response = self.ya_api.copy_file_or_folder("/basic_pics", "/f45")

        self.assertEqual(response.status_code, 201)

    @responses.activate
    def test_yandex_copy_file_or_folder_unauth(self):
        responses.add(responses.POST,
                      f"{self.ya_api.URL}/resources/copy/?from=/basic_pics&path=/f45",
                      json={
                          "message": "string",
                          "description": "string",
                          "error": "string"},
                      status=401)

        response = self.ya_api.copy_file_or_folder("/basic_pics", "/f45")

        self.assertEqual(response.status_code, 401)

    @responses.activate
    def test_yandex_remove_folder_or_file(self):
        responses.add(responses.DELETE,
                      f"{self.ya_api.URL}/resources?path=/f45&permanently={False}",
                      json={
                          "href": "string",
                          "method": "string",
                          "templated": True},
                      status=204)

        response = self.ya_api.remove_folder_or_file("/f45")

        self.assertEqual(response.status_code, 204)

    @responses.activate
    def test_yandex_remove_folder_or_file_unauth(self):
        responses.add(responses.DELETE,
                      f"{self.ya_api.URL}/resources?path=/f45&permanently={False}",
                      json={
                          "message": "string",
                          "description": "string",
                          "error": "string"},
                      status=401)

        response = self.ya_api.remove_folder_or_file("/f45")

        self.assertEqual(response.status_code, 401)

    @responses.activate
    def test_yandex_remove_folder_or_file_permanently(self):
        responses.add(responses.DELETE,
                      f"{self.ya_api.URL}/resources?path=/f45&permanently={True}",
                      json={
                          "href": "string",
                          "method": "string",
                          "templated": True},
                      status=204)

        response = self.ya_api.remove_folder_or_file("/f45", True)

        self.assertEqual(response.status_code, 204)

    @responses.activate
    def test_yandex_remove_folder_or_file_permanently_unauth(self):
        responses.add(responses.DELETE,
                      f"{self.ya_api.URL}/resources?path=/f45&permanently={True}",
                      json={
                          "message": "string",
                          "description": "string",
                          "error": "string"},
                      status=401)

        response = self.ya_api.remove_folder_or_file("/f45", True)

        self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    unittest.main()
