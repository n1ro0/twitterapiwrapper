from rest_framework.test import APITestCase


from ... import models


class HashtagModelAPITestCase(APITestCase):
    def setUp(self):
        self.text = "test_hashtag"
        self.hashtag = models.Hashtag(text=self.text)

    def test_model_can_create_a_hashtag(self):
        initial_count = models.Hashtag.objects.count()
        self.hashtag.save()
        new_count = models.Hashtag.objects.count()
        self.assertNotEqual(initial_count, new_count)

    def test_model_can_get_a_hashtag(self):
        self.hashtag.save()
        hashtag = models.Hashtag.objects.get()
        self.assertEqual(self.hashtag, hashtag)
        self.assertEqual(self.hashtag.id, hashtag.id)
