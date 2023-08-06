from django.test import TestCase
from django.core.files import File
from rest_framework.test import APIRequestFactory, APIClient, force_authenticate
from .models import *
from django.contrib.auth import get_user_model

# Create your tests here.

UM = get_user_model()


class MediaImageTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = UM.objects.create(username='user1', password="user1pass")
        self.user2 = UM.objects.create(username='user2', password="user2pass")
        self.images = []
        with open('rest_mediabrowser/testfiles/1.png', 'rb') as infile:
            img1 = MediaImage.objects.create(
                owner=self.user1, height=0, width=0)
            img1.image.save('1.png', File(infile))
            self.images.append(img1)
            img2 = MediaImage.objects.create(
                owner=self.user1, height=0, width=0)
            img2.image.save('1.png', File(infile))
            self.images.append(img2)
            img3 = MediaImage.objects.create(
                owner=self.user2, height=0, width=0)
            img3.image.save('1.png', File(infile))
            self.images.append(img3)

    def test_authentication_restriction(self):
        # Check if user can access without login
        resp = self.client.get('/mediabrowser/images/')
        self.assertNotEqual(resp.status_code, 200)

        # Check if user can access with login
        self.client.force_authenticate(user=self.user1)
        resp2 = self.client.get('/mediabrowser/images/')
        self.assertEqual(resp2.status_code, 200)
        self.client.logout()

    def test_ownership_restrictions_in_listview(self):
        self.client.force_authenticate(user=self.user1)
        resp = self.client.get('/mediabrowser/images/')
        data = resp.json()
        self.assertEqual(2, len(data))

        self.client.force_authenticate(user=self.user2)
        resp = self.client.get('/mediabrowser/images/')
        data = resp.json()
        self.assertEqual(1, len(data))

    def tearDown(self):
        for img in self.images:
            img.image.delete(False)


class MediaFileTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = UM.objects.create(username='user1', password="user1pass")
        self.user2 = UM.objects.create(username='user2', password="user2pass")
        self.files = []
        with open('rest_mediabrowser/testfiles/1.png', 'rb') as infile:
            file1 = MediaFile.objects.create(
                owner=self.user1)
            file1.file.save('1.png', File(infile))
            self.files.append(file1)
            file2 = MediaFile.objects.create(
                owner=self.user1)
            file2.file.save('1.png', File(infile))
            self.files.append(file2)
            file3 = MediaFile.objects.create(
                owner=self.user2)
            file3.file.save('1.png', File(infile))
            self.files.append(file3)

    def test_authentication_restriction(self):
        # Check if user can access without login
        resp = self.client.get('/mediabrowser/files/')
        self.assertNotEqual(resp.status_code, 200)

        # Check if user can access with login
        self.client.force_authenticate(user=self.user1)
        resp2 = self.client.get('/mediabrowser/files/')
        self.assertEqual(resp2.status_code, 200)
        self.client.logout()

    def test_ownership_restrictions_in_listview(self):
        self.client.force_authenticate(user=self.user1)
        resp = self.client.get('/mediabrowser/files/')
        data = resp.json()
        self.assertEqual(2, len(data))

        self.client.force_authenticate(user=self.user2)
        resp = self.client.get('/mediabrowser/files/')
        data = resp.json()
        self.assertEqual(1, len(data))

    def tearDown(self):
        for f in self.files:
            f.file.delete(False)
