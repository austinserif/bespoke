"""Production testing file for search item model"""

import os
from unittest import TestCase
from app import app
from models import SearchItem

app.config.from_object('config.Testing')
db.create_all()