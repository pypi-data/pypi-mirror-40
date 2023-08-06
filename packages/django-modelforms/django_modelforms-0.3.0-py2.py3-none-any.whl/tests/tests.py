from django import forms
from django.apps import apps
from django.db.utils import IntegrityError
from django.forms.models import modelform_factory
from test_plus import TestCase

from modelforms.forms import ModelForm


class UniqueTogether(TestCase):

    def setUp(self):
        # obtain the model classes from application registry
        Author = apps.get_model('tests', 'Author')
        Book = apps.get_model('tests', 'Book')

        # dynamically define our BookForm class, firstly without the mixin and
        # secondly with it to test we solve a problem.
        self.original_form_class = modelform_factory(
            Book, forms.ModelForm, ('title', 'rrp'))
        self.form_class = modelform_factory(
            Book, ModelForm, ('title', 'rrp'))

        # create some instances to use in tests
        author = Author.objects.create(name='Robert Ludlum')
        self.book1 = author.books.create(
            title='The Bourne Identity',
            rrp='9.20',
        )
        self.book2 = author.books.create(
            title='The Bourne Supremacy',
            rrp='10.50',
        )

    def test_invalid_rrp(self):
        data = {
            'title': self.book2.title,
            'rrp': "1000",
        }

        # the title is still unique, but the rrp is invalid
        form = self.original_form_class(data=data, instance=self.book2)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors,
            {
                'rrp': [u'Ensure that there are no more than 3 digits before '
                        u'the decimal point.'],
            },
        )

        # our mixin has not changed default behaviour on this field
        form = self.form_class(data=data, instance=self.book2)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors,
            {
                'rrp': [u'Ensure that there are no more than 3 digits before '
                        u'the decimal point.'],
            },
        )

    def test_title_clash(self):
        data = {
            'title': self.book1.title,
            'rrp': "15.95",
        }

        # title must be unique_together with author, title should not be valid
        form = self.original_form_class(data=data, instance=self.book2)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.errors, {})

        # applying mixin proves we're fixing it
        form = self.form_class(data=data, instance=self.book2)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors,
            {
                'title': [u'Book with this title already exists.'],
            },
        )

    def test_invalid_rrp_and_title_clash(self):
        data = {
            'title': self.book1.title,
            'rrp': "1000",
        }

        # title must be unique_together with author, title should not be valid
        form = self.original_form_class(data=data, instance=self.book2)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors,
            {
                'rrp': [u'Ensure that there are no more than 3 digits before '
                        u'the decimal point.'],
            },
        )

        # applying mixin proves we're fixing it
        form = self.form_class(data=data, instance=self.book2)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors,
            {
                'title': [u'Book with this title already exists.'],
                'rrp': [u'Ensure that there are no more than 3 digits before '
                        u'the decimal point.'],
            },
        )

    def test_update_view(self):
        data = {
            'title': self.book1.title,
        }
        with self.assertRaises(IntegrityError):
            self.post('update-book', self.book2.pk, data=data)

    def test_unique_update_view(self):
        data = {
            'title': self.book1.title,
        }
        self.post('unique-update-book', self.book2.pk, data=data)
        self.assertFormError(
            self.last_response,
            'form',
            'title',
            [u'Book with this title already exists.'],
        )
