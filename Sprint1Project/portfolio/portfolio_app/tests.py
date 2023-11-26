
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from portfolio_app.models import Golfer, Notebook

class GolfClubTestCase(TestCase):

    #check to see if homepage works, if so response code is 200 meaning bingo
    def test_home_page_status_code(self):
        response = self.client.get(reverse('index')) 
        self.assertEquals(response.status_code, 200)

    def test_home_page_template(self):
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'portfolio_app/index.html')

    def setUp(self):
        # simulates a user, golfer, and a notebook
            self.user = User.objects.create_user(username='testuser', password='12345')
            self.golfer = Golfer.objects.create(user=self.user, gender='M')
            self.notebook = Notebook.objects.create(golfer=self.golfer)

    def test_notebook_list_view(self):
        # seeing the notebook_list view if it works 200 again if not fails
        response = self.client.get(reverse('notebook_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'portfolio_app/notebook_list.html')
        self.assertTrue('notebooks' in response.context)

    def test_notebook_detail_view(self):
        # test to see if we can the detail of the correct notebook we are using. 
        response = self.client.get(reverse('notebook_detail', kwargs={'pk': self.notebook.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'portfolio_app/notebook_detail.html')
        #
        self.assertEqual(response.context['notebook'], self.notebook)  