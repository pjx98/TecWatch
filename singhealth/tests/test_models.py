from django.test import TestCase
from singhealth.models import Staff

class YourTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("setUpTestData: Run once to set up non-modified data for all class methods.")
        pass

    def setUp(self):
        print("setUp: Run once for every test method to setup clean data.")
        pass

    def test_false_is_false(self):
        self.assertFalse(False)

    def test_false_is_true(self):
        self.assertTrue(False)

    def test_one_plus_one_equals_two(self):
        self.assertEqual(1 + 1, 2)
        
    # theres assertRedirects/ assertTemplateUsed too
    
class StaffModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Staff.objects.create(first)