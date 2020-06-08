"""Production testing file for user model"""

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

    def test_searches(self):
        # """test for searches method"""
        search_item = User.add_search("foo", self.testuser.id)
        active_searches = self.testuser.searches()
        self.assertEqual(search_item, active_searches[0])

        db.session.delete(search_item)
        db.session.commit()
    
    def test_active_tags(self):
        """test for active_tags()"""

        #does tag display
        tag_item = User.add_tag("foo", self.testuser.id)
        active_tags = self.testuser.active_tags()
        self.assertEqual(tag_item, active_tags[0])

        # does second tag display
        tag_item_2 = User.add_tag("bar", self.testuser.id)
        active_tags = self.testuser.active_tags()
        self.assertEqual(tag_item, active_tags[1])
        self.assertEqual(tag_item_2, active_tags[0]) #--> tag_item_2 becomes 0th index because active_tags() queries w/ order_by date desc statement.

        # #does second tag disapear once display is set to false
        tag_item_2.display = False
        db.session.commit()
        active_tags = self.testuser.active_tags()
        self.assertEqual(len(active_tags), 1)
        self.assertEqual(tag_item, active_tags[0])

        db.session.delete(tag_item)
        db.session.commit()

        db.session.delete(tag_item_2)
        db.session.commit()
    
    def test_get_started(self):
        """test for get_started()"""
        # if we pass a given email into get_started, can we then query the database 
        # for that email?
        email = "newuser@test.com"
        self.getting_started_user = User.get_started(email)
        queried_user = User.query.filter(User.email==email).first()
        self.assertEqual(queried_user.email, email)

        #does the queried user have a password or first name yet?
        self.assertIsNone(queried_user.first_name)
        self.assertIsNone(queried_user.last_name)
        self.assertIsNone(queried_user.password)

        #is the queried user activated yet?
        self.assertFalse(queried_user.is_active())

    
    def test_sign_up(self):
        """test for sign_up"""
        email = "newuser@test.com"
        first_name = "Foo"
        last_name = "Bar"
        password = "foobar"

        queried_user = User.query.filter(User.email==email).first()
        queried_user.first_name = first_name
        queried_user.last_name = last_name
        queried_user.password = password
        db.session.commit()
        User.sign_up(queried_user)

        #does the queried user have a password or first/last name now?
        self.assertEqual(queried_user.first_name, first_name)
        self.assertEqual(queried_user.last_name, last_name)

        #is the queried user activated yet?
        self.assertTrue(queried_user.is_active())

        #is the queried user authenticated yet?
        self.assertFalse(queried_user.authenticated)

        db.session.delete(queried_user)
        db.session.commit()
    

    def test_add_tag(self):
        """test for add_tag"""
        tag = User.add_tag("foo", self.testuser.id)
        users_tags = self.testuser.active_tags()
        self.assertEqual(users_tags[0], tag)

        db.session.delete(tag)
        db.session.commit()
    
    def test_add_search(self):
        """test for add_search()"""
        search_item = User.add_search("foo", self.testuser.id)
        users_searches = self.testuser.searches()
        self.assertEqual(users_searches[0], search_item)
        
        db.session.delete(search_item)
        db.session.commit()
    
    def test_remove_search(self):
        """test for remove_search"""
        search_item = User.add_search("foo", self.testuser.id)
        users_searches = self.testuser.searches()
        self.assertEqual(users_searches[0], search_item)

        User.remove_search(search_item.id)
        users_searches = self.testuser.searches()
        self.assertNotIn(search_item, users_searches)
        
        db.session.delete(search_item)
        db.session.commit()
    
    