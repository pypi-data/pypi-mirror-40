from unittest import TestCase

from tests.app.app import create_app

from json import dumps
from ySanic import MyEncoder

class Tests(TestCase):
  def setUp(self):
    self.app = create_app()

  def testPrettyRoutes(self):
    self.app.log.info(dumps(self.app.router.routes_all, indent = 2, cls = MyEncoder))

  def testRoutes(self):
    self.app.log.info(self.app.router.routes_all)
