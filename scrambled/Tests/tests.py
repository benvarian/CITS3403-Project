from datetime import datetime, timedelta
import unittest

from app import app, db
from app.models import User, Statistics

class StatisticsModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_scores(self):
        now = datetime.utcnow()
        user_admin = User(id='1',username='admin',email='admin@scrambled.com')
        test_admin = Statistics(id='1',score ='400',timeTaken="1:49",game_completed=now,userId='admin')

    def test_average(self):



class UserModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        test_ben = User(username='ben')
        test_ben.set_password('ben')
        test_admin = User(username='admin')
        test_admin.set_password('admin')
        self.assertFalse(test_admin.check_password('test'))
        self.assertTrue(test_admin.check_password('admin'))

        self.assertFalse(test_ben.check_password('dog'))
        self.assertFalse(test_ben.check_password('shayan'))
        self.assertTrue(test_ben.check_password('ben'))

    def test_Statistics_ForeignKey(self):
        
        user_admin = User(id='1',username='admin',email='admin@scrambled.com')
        user_ben = User(id='2',username='ben',email='ben@scrambled.com')
        user_shayan = User(id='3',username='shayan',email='shayan@scrambled.com')
        user_sameer = User(id='4',username='sameer',email='sameer@scrambled.com')
        db.session.add_all([user_admin,user_ben,user_shayan,user_sameer])
        now = datetime.utcnow()

        test_admin = Statistics(id='1',score ='400',timeTaken="1:49",game_completed=now,userId='admin')
        test_ben = Statistics(id='2',score ='450',timeTaken='2:10',game_completed=now ,userId='ben')
        test_shayan = Statistics(id='3',score ='250',timeTaken='1:20',game_completed=now,userId='shayan')
        test_sameer = Statistics(id='4',score ='100',timeTaken='1:00',game_completed=now ,userId='sameer')

        db.session.add_all([test_admin,test_ben,test_shayan,test_sameer])
        db.session.commit()

        self.assertTrue(test_admin.userId==user_admin.username)
        self.assertTrue(test_ben.userId==user_ben.username)
        self.assertTrue(test_shayan.userId==user_shayan.username)
        self.assertTrue(test_sameer.userId==user_sameer.username)

if __name__ == '__main__':
    unittest.main(verbosity=2)
