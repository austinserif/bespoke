"""Production testing file for user model"""

import os
from unittest import TestCase
from app import app, db
from models import User

app.config.from_object('config.Testing')

class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUpClass(self):
        """Create test client, add sample data."""
        db.create_all()
        self.client = app.test_client()

    def tearDownClass(self):
        """tear down db"""
        db.drop_all()

    def test_searches(self):
        """test for searches method"""
        User.authenticate(self.testuser, "testuser")
        search_item = User.add_search("foo", self.testuser.id)
        active_searches = self.testuser.searches()
        self.assertEqual(search_item, active_searches[0])
    
    
    
    # def test_active_tags():
    #     """test for active_tags()"""
    #     return
    
    # def test_get_started():
    #     """test for get_started()"""
    #     return
    
    # def test_sign_up():
    #     """test for sign_up"""
    #     return
    
    # def test_authenticate():
    #     """test for authenticated"""
    #     return
    
    # def test_add_test():
    #     """test for add_tag"""
    #     return
    
    # def test_add_search():
    #     """test for add_search()"""
    #     return
    
    # def test_remove_search():
    #     """test for remove_search"""
    #     return
    
    