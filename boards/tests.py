from django.urls import resolve
from django.urls import reverse
from django.test import TestCase

from .views import home, board_topics
from .models import Board


class HomeTests(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Django', description='Django board.')
        url = reverse('home')
        self.response = self.client.get(url)

    def test_home_view_status_code(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_home_url_resoves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, home)

    def test_home_view_contains_link_to_topics_page(self):
        board_topics_url = reverse('board_topics', kwargs={'pk': self.board.pk})
        self.assertContains(self.response, 'href="{0}"'.format(board_topics_url))


class BoardTopicTest(TestCase):
    def setUp(self):
        Board.objects.create(name='Django', description='Django discuss forum')

    def test_board_topics_view_sucess_status_code(self):
        url = reverse('board_topics', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_board_topics_view_not_found_status_code(self):
        response = self.client.get(reverse('board_topics',kwargs={'pk': 89}))
        self.assertEquals(response.status_code, 404)

    def test_board_topic_url_resolves_topic_view(self):
        view = resolve('/boards/1/')
        self.assertEquals(view.func,board_topics)