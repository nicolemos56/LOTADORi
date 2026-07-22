import unittest

from fastapi.testclient import TestClient

from app.backend.main import app


class KalawendaBackendTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_find_guide_intent(self):
        response = self.client.post(
            "/intent",
            json={"message": "Quero um guia para visitar a cidade"},
        )
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["intent"], "find_guide")
        self.assertGreaterEqual(len(body["recommendations"]), 1)

    def test_find_place_intent(self):
        response = self.client.post(
            "/intent",
            json={"message": "Me mostre lugares turísticos perto do centro"},
        )
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["intent"], "find_place")
        self.assertGreaterEqual(len(body["recommendations"]), 1)

    def test_places_endpoint(self):
        response = self.client.get("/places")
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertGreaterEqual(len(body["places"]), 1)
        self.assertIn("lat", body["places"][0])

    def test_kalandula_flow(self):
        response = self.client.post(
            "/intent",
            json={"message": "Quero saber sobre Kalandula"},
        )
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["intent"], "show_place")
        self.assertEqual(body["next_action"], "offer_guides")
        self.assertTrue(body["image_url"])

    def test_guide_selection_flow(self):
        response = self.client.post(
            "/intent",
            json={"message": "Quero um guia"},
        )
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["intent"], "find_guide")
        self.assertEqual(body["next_action"], "show_guides")
        self.assertGreaterEqual(len(body["recommendations"]), 1)


if __name__ == "__main__":
    unittest.main()
