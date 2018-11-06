from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from django.http import HttpRequest
# Create your tests here.
class HomePageTest(TestCase):
    #def test_root_url_resolve_to_home_page(self):
    #    found = resolve('/')
    #    self.assertEqual(found.func, home_page)

    def test_home_page_return_correct_html(self):
        response = self.client.get('/')
        html = response.content.decode('utf8')
        self.assertTemplateUsed(response, 'home.html')
        #request = HttpRequest()
        #response = home_page(request)
        #self.assertTrue(html.startswith('<html>'))
        #self.assertIn('<title>To-Do lists</title>', html)
        #self.assertTrue(html.endswith('</html>'))

