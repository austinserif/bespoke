"""Production testing file for view functions, including login and sign up"""

import os
from unittest import TestCase
from app import app, db, current_user
from models import User, Tag

app.config.from_object('config.Testing')
db.create_all()

class UserViewTestCase(TestCase):
    """Test views for messages."""
    
    def setUp(self):
        """set up test client and seed sample authenticated user"""
        self.client = app.test_client()
        self.testuser = User(email="test@test.com", first_name="Test", last_name="User", password="password", authenticated=True)
        db.session.add(self.testuser)
        db.session.commit()
    
    def tearDown(self):
        """remove test user"""
        db.session.delete(self.testuser)
        db.session.commit()
    
    def test_homepage(self):
        """test for homepate view function"""
        with self.client as client:
            #for no current_user
            response = client.get('/')
            data = response.get_data(as_text=True)
            self.assertEqual(response.status_code, 200)
            html_string = '''<nav class="mdl-navigation">
    <a class="mdl-navigation__link" href="">Docs</a>
    <a class="mdl-navigation__link" href="">About</a>
    <a class="mdl-navigation__link" href="">Contact</a>
    <a class="mdl-navigation__link" href="/login">Sign-in</a>
  </nav>'''
            #is home header in rendered html
            self.assertIn(html_string, data)
        
            getting_started_html = '''<div class="row d-flex justify-content-center">
    <form action="/get-started" method="POST" id="get-started-form">'''

            #is getting started form in rendered html
            self.assertIn(getting_started_html, data)
    

    def test_get_started(self):
        """test get_started view function"""
        with self.client as client:
            response = client.post('/get-started', data={'email': 'test1@test.com'}, follow_redirects=True)
            data = response.get_data(as_text=True)  
             
            expected_html = "test1@test.com"
            self.assertIn(expected_html, data)
            self.assertEqual(response.status_code, 200)
    
    def test_sign_up(self):
        """test sign_up view function"""
        user = User.query.filter(User.email=="test1@test.com").first()
        with self.client as client:
            response = client.post(f'/sign-up?u={user.id}', data={'email': 'test1@test.com', 'first_name': 'Test', 'last_name': 'User', 'password': 'password'}, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            data = response.get_data(as_text=True)

            # does html content indicate a successful sign-up, redirected to the dashboard?
            expected_html = '<a class="mdl-navigation__link" href="/logout">Sign-out</a>'
            self.assertIn(expected_html, data)

        db.session.delete(user)
        db.session.commit()


    def test_login(self):
        """test login view function"""
        with self.client as client:
            response = client.get('/login')
            self.assertIn('<form action="/login" method="POST" id="user-sign-in-form">', response.get_data(as_text=True))




            