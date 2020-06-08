"""Production testing file for homepage views: including sign up and sign in"""

import os
from unittest import TestCase
from app import app

app.config.from_object('config.Testing')
db.create_all()