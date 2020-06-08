"""Production testing file for dashboard views"""

import os
from unittest import TestCase
from app import app

app.config.from_object('config.Testing')
db.create_all()

