
from django.test import TestCase
from django.urls import reverse
from .models import StickyNote


class StickyNoteModelTest(TestCase):

    def setUp(self):
        self.note = StickyNote.objects.create(
            title="Test Note",
            content="This is my test sticky note."
        )

    def test_note_creation(self):
        self.assertEqual(StickyNote.objects.count(), 1)

    def test_note_title(self):
        self.assertEqual(self.note.title, "Test Note")

    def test_note_content(self):
        self.assertEqual(
            self.note.content,
            "This is my test sticky note."
        )

    def test_note_string_representation(self):
        self.assertEqual(str(self.note), "Test Note")


class StickyNoteViewTest(TestCase):

    def setUp(self):
        self.note = StickyNote.objects.create(
            title="Test Note",
            content="This is my test sticky note."
        )

    def test_note_list_view(self):
        response = self.client.get(
            reverse('notes:note_list')
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Note")

    def test_note_detail_view(self):
        response = self.client.get(
            reverse('notes:note_detail', args=[self.note.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Note")
        self.assertContains(
            response, "This is my test sticky note."
        )

    def test_create_note_view(self):
        response = self.client.get(
            reverse('notes:note_create')
        )
        self.assertEqual(response.status_code, 200)

    def test_create_note(self):
        response = self.client.post(
            reverse('notes:note_create'),
            {
                'title': 'New Note',
                'content': 'New note content'
            }
        )
        self.assertRedirects(
            response,
            reverse('notes:note_list')
        )
        self.assertTrue(
            StickyNote.objects.filter(title='New Note').exists()
        )

    def test_update_note(self):
        response = self.client.post(
            reverse('notes:note_update', args=[self.note.pk]),
            {
                'title': 'Updated Note',
                'content': 'Updated content'
            }
        )
        self.assertRedirects(
            response,
            reverse('notes:note_list')
        )
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, 'Updated Note')

    def test_delete_note(self):
        response = self.client.post(
            reverse('notes:note_delete', args=[self.note.pk])
        )
        self.assertRedirects(
            response,
            reverse('notes:note_list')
        )
        self.assertFalse(
            StickyNote.objects.filter(pk=self.note.pk).exists()
        )

    def test_delete_confirmation_page(self):
        response = self.client.get(
            reverse('notes:note_delete', args=[self.note.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Note')
