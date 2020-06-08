"""Production testing file for tag model"""

import os
from unittest import TestCase
from app import app, db
from models import User, Tag

app.config.from_object('config.Testing')
db.create_all()

class UserModelTestCase(TestCase):
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
    
    def test_remove_tag(self):
        """test remove tag method"""
        tag = User.add_tag("foo", self.testuser.id)
        self.assertIn(tag, self.testuser.active_tags())

        #now call remove tag
        Tag.remove_tag(tag.id)
        self.assertNotIn(tag, self.testuser.active_tags())

        db.session.delete(tag)
        db.session.commit()

