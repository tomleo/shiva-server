# -*- coding: utf-8 -*-
import os
import tempfile
import unittest

from shiva import app, settings, auth


class TestBasicApp(unittest.TestCase):

    def setUp(self):
        self.PROJECT_NAME = 'Shiva'
        settings.PROJECT_NAME = self.PROJECT_NAME

    def test_new_app(self):
        shiva = app.Shiva()
        shiva.configure(settings)
        self.assertEqual(shiva.config['PROJECT_NAME'], self.PROJECT_NAME)

    def test_new_app_with_config_param(self):
        shiva = app.Shiva(settings)
        shiva.config.PROJECT_NAME = self.PROJECT_NAME
        self.assertEqual(shiva.config['PROJECT_NAME'], self.PROJECT_NAME)


class TestAuth(unittest.TestCase):

    def setUp(self):
        self.db_path = tempfile.mkstemp()[1]
        settings.SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % self.db_path
        self.app = app.Shiva(settings)

        self.app.init_db()
        self.app.db['session'].rollback()

    def tearDown(self):
        os.unlink(self.db_path)

    def test_user_creation(self):
        user = self.app.new_user(name=u'Alvaro Mouriño',
                                 email='alvaro@mourino.net')

        self.assertEqual(user.name, u'Alvaro Mouriño')
        self.assertEqual(user.pk, None)

        user.save()

        self.assertEqual(self.app.query(auth.User).count(), 1)
        self.assertNotEqual(user.pk, None)
        self.assertTrue(isinstance(user.pk, int))

        user.delete()

        self.assertEqual(self.app.query(auth.User).count(), 0)

    def test_user_login(self):
        self.assertEqual(self.app.authenticate(email='alvaro@mourino.net',
                                               password='abc123'), None)
        user = self.app.new_user(name=u'Alvaro Mouriño',
                                 email='alvaro@mourino.net')
        user.save()

        user = self.app.authenticate(email='alvaro@mourino.net',
                                     password='abc123')
        self.assertTrue(isinstance(user, auth.User))


if __name__ == '__main__':
    unittest.main()
