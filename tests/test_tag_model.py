"""Production testing file for tag model"""

import os
from unittest import TestCase
from app import app
from models import Tag

app.config.from_object('config.Testing')
db.create_all()