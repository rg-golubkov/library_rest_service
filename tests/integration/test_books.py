import json
import unittest

from rest_service import create_app


class BooksTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app({
            'TESTING': True,
            'DATABASE_URI': 'sqlite:///:memory:',
            'DB_DEFAULT_VALUES': True
        })
        self.client = self.app.test_client()

    def test_update_book_author(self):
        # Create author
        author_info = {'fullname': 'Author Fullname'}
        response = self.client.post('/api/authors/', json=author_info)
        author = json.loads(response.data)

        self.assertEqual(response.status_code, 201, msg=response.data)
        self.assertIsInstance(author, dict)
        self.assertEqual(author['fullname'], author_info['fullname'])

        # Get Books
        response = self.client.get('/api/books/')
        books = json.loads(response.data).get('books')
        book = books[0]

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(books, list)
        self.assertIsInstance(book, dict)

        # Change book author
        book['author_id'] = author['author_id']
        response = self.client.put(f'/api/books/{book["book_id"]}', json=book)
        changed_book = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(changed_book['author_id'], author['author_id'])
        self.assertEqual(changed_book['fullname'], author['fullname'])
