from django.test import TestCase
from lists.models import Item, List
from django.utils.html import escape
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

    def test_can_save_a_POST_request(self):
        self.client.post('/', data={'item_text':'A new list item'})
        self.assertEqual(Item.objects.count(),1)

        new_item = Item.objects.first()
        self.assertEqual(new_item.text,'A new list item' )

    def test_redirects_after_post(self):
        response = self.client.post('/', data={'item_text': 'A new list item'})
        self.assertEqual(response.status_code,302)
        self.assertEqual(response['location'], '/lists/the-only-list-in-the-world/')

        #self.assertIn('A new list item', response.content.decode())
        #self.assertTemplateUsed(response, 'home.html')

    def test_only_saves_items_when_necessary(self):
        initial_count = Item.objects.count()
        self.client.get('/')
        self.assertEqual(Item.objects.count(), initial_count)


class ListViewTest(TestCase):

    def test_use_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'list.html')

    def test_display_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text = 'itemey 1', list = correct_list)
        Item.objects.create(text='itemey 2', list = correct_list)

        other_list = List.objects.create()
        Item.objects.create(text='other list item 1', list=other_list)
        Item.objects.create(text='other list item 2', list=other_list)

        response = self.client.get(f'/lists/{correct_list.id}/')

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other list item 1')
        self.assertNotContains(response, 'other list item 2')

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.get(f'/lists/{correct_list.id}/')
        # response.context represent the context that django will pass to the rendering function
        # the django test client just put it in the response for testing purposes
        self.assertEqual(response.context['list'], correct_list)

    def test_validation_errors_end_up_on_lists_page(self):
        list_ = List.objects.create()
        response = self.client.post(f'/lists/{list_.id}/', data={'item_text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)




class NewListTest(TestCase):

    def test_can_save_a_POST_request(self):
        self.client.post('/lists/new', data={'item_text':'A new list item'})
        self.assertEqual(Item.objects.count(),1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text,'A new list item' )

    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', data={'item_text':'A new list item'})
        list_ = List.objects.first()
        self.assertRedirects(response, f'/lists/{list_.id}/')

    def test_validation_errors_are_sent_back_to_home_page_template(self):
        response = self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)

    def test_invalid_list_item_arent_saved(self):
        self.client.post('/lists/new', data={'item_text':''})
        self.assertEqual(List.objects.count(),0)
        self.assertEqual(Item.objects.count(), 0)

