from unittest import TestCase
from app import app, score_word
from flask import session
from boggle import Boggle
import json


class FlaskTests(TestCase):

    def setUp(self):
        """Stuff to do before every test"""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Test the / route"""

        with self.client:
            response = self.client.get('/')
            self.assertIn('board', session)
            self.assertIn('score', session)
            self.assertIn('guessed_words', session)

    def test_validate_word(self):
        """Test the /validate route"""

        # Set up a session with an initial board, guessed_words, score, and playCount
        initial_board = [["D", "O", "G", "G", "G"],
                         ["D", "O", "G", "G", "G"],
                         ["D", "O", "G", "G", "G"],
                         ["D", "O", "G", "G", "G"],
                         ["D", "O", "G", "G", "G"]]

        initial_guessed_words = []
        initial_score = 0
        initial_playCount = 0

        with self.client.session_transaction() as sess:
            sess['board'] = initial_board
            sess['guessed_words'] = initial_guessed_words
            sess['score'] = initial_score
            sess['playCount'] = initial_playCount

        # Make a GET request to the /validate route with a test word
        test_word = "dog"
        response = self.client.get(f'/validate?word={test_word}')

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the response JSON contains the expected message
        self.assertEqual(response.json['message'], 'ok')

        # Check if the session variables have been updated correctly
        with self.client.session_transaction() as sess:
            self.assertEqual(sess['guessed_words'], [test_word])
            self.assertEqual(sess['score'], len(test_word))
            self.assertEqual(sess['playCount'], initial_playCount + 1)

    def test_score_word(self):
        # Test scoring a word with 0 characters (empty word)
        self.assertEqual(score_word(''), 0)

        # Test scoring a word with 1 character
        self.assertEqual(score_word('A'), 1)

        # Test scoring a word with multiple characters
        self.assertEqual(score_word('Hello'), 5)

    def test_record_playcount(self):
        """Test the /record_playcount route"""

        # Define a playCount value to send in the request
        playCount = 42

        # Send a POST request to the /record_playcount route with playCount data
        response = self.client.post(
            '/record_playcount', json={'playCount': playCount})

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the response JSON contains the expected message
        self.assertEqual(response.json['message'],
                         'Play count recorded successfully')

        # Check if the session variable 'playCount' has been updated correctly
        with self.client.session_transaction() as sess:
            self.assertEqual(sess['playCount'], playCount)
