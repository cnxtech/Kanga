from django.test import TestCase
from help.models import Category, Command, Field
from help import init_data

class CategoryTestCase(TestCase):
    def setUp(self):
        init_data.delete_everything()
        init_data.create_category()
        init_data.create_command()

    def test_categories_match_description_text(self):
        """Description of categories are correctly matched"""
        input_streaming = Category.objects.get(category="input_streaming")
        transformation = Category.objects.get(category="transformation")
        self.assertEqual(input_streaming.category_text, 'Input Streaming')
        self.assertEqual(transformation.category_text, 'Transformation')

    def test_commands_lookup(self):
        """commands are correctly looked up"""
        commands = Command.objects.filter(category_id="filter")
        empty = Command.objects.filter(category_id="dummy")
        self.assertNotEqual(len(commands), 0)
        self.assertEqual(len(empty), 0)
