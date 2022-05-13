from datetime import datetime, timedelta
import unittest

from app import app, db
from app.models import User, Post, Statistics


class UserModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        test_susan = User(username='susan')
        test_susan.set_password('cat')
        test_admin = User(username='admin')
        test_admin.set_password('admin')
        self.assertFalse(test_admin.check_password('test'))
        self.assertTrue(test_admin.check_password('admin'))
        self.assertFalse(test_susan.check_password('dog'))
        self.assertTrue(test_susan.check_password('cat'))

    def test_avatar(self):
        test_john = User(username='john', email='john@example.com')
        self.assertEqual(test_john.avatar(128), ('https://www.gravatar.com/avatar/'
                                                 'd4c74594d841139328695756648b6bd6'
                                                 '?d=identicon&s=128'))
        test_admin = User(username='admin', email='admin@scrambled.com')
        self.assertEqual(test_admin.avatar(128), ('https://www.gravatar.com/avatar/'
                                                  'db44cefdcf33f2717b02b4cc584af78d'
                                                  '?d=identicon&s=128'))
        test_ben = User(username='ben', email='ben@icloud.com')
        self.assertEqual(test_ben.avatar(128), ('https://www.gravatar.com/avatar/'
                                                '8ce6075d423d3f2cc06eb43005f844db'
                                                '?d=identicon&s=128'))
        test_shayan = User(username='shayan', email='shayan@scrambled.com')
        self.assertEqual(test_shayan.avatar(128), ('https://www.gravatar.com/avatar/'
                                                '77ab2873f69830814f41c4a673df1579'
                                                '?d=identicon&s=128'))
        test_sameer = User(username='sameer', email='sameer@scrambled.com')
        self.assertEqual(test_sameer.avatar(128), ('https://www.gravatar.com/avatar/'
                                                'a07ed19dcbd9ea5d88451b3a821278dc'
                                                '?d=identicon&s=128'))
        test_lilburne = User(username='lilbrune', email='lilbrune@scrambled.com')
        self.assertEqual(test_lilburne.avatar(128), ('https://www.gravatar.com/avatar/'
                                                '73d091c5db3b1b4b1da42cee31c2530a'
                                                '?d=identicon&s=128'))

    def test_follow(self):
        u1 = User(username='john', email='john@scrambled.com')
        u2 = User(username='susan', email='susan@scrambled.com')
        u3 = User(username='admin', email='admin@scrambled.com')
        u4 = User(username='shayan', email='shayan@scrambled.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.add(u3)
        db.session.add(u4)
        db.session.commit()
        self.assertEqual(u1.followed.all(), [])
        self.assertEqual(u1.followers.all(), [])

        u1.follow(u2)
        db.session.commit()
        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 1)
        self.assertEqual(u1.followed.first().username, 'susan')
        self.assertEqual(u2.followers.count(), 1)
        self.assertEqual(u2.followers.first().username, 'john')

        u1.unfollow(u2)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 0)
        self.assertEqual(u2.followers.count(), 0)

        u2.follow(u3)
        db.session.commit()
        self.assertTrue(u2.is_following(u3))
        self.assertEqual(u3.followers.first().username,'susan')

        u4.follow(u3)
        db.session.commit()
        self.assertTrue(u4.is_following(u3))
        self.assertEqual(u3.followers.count(),2)

    def test_follow_posts(self):
        # create four users
        u1 = User(username='john', email='john@example.com')
        u2 = User(username='susan', email='susan@example.com')
        u3 = User(username='mary', email='mary@example.com')
        u4 = User(username='david', email='david@example.com')
        db.session.add_all([u1, u2, u3, u4])

        # create four posts
        now = datetime.utcnow()
        p1 = Post(body="post from john", author=u1,
                  timestamp=now + timedelta(seconds=1))
        p2 = Post(body="post from susan", author=u2,
                  timestamp=now + timedelta(seconds=4))
        p3 = Post(body="post from mary", author=u3,
                  timestamp=now + timedelta(seconds=3))
        p4 = Post(body="post from david", author=u4,
                  timestamp=now + timedelta(seconds=2))
        db.session.add_all([p1, p2, p3, p4])
        db.session.commit()

        # setup the followers
        u1.follow(u2)  # john follows susan
        u1.follow(u4)  # john follows david
        u2.follow(u3)  # susan follows mary
        u3.follow(u4)  # mary follows david
        db.session.commit()

        # check the followed posts of each user
        f1 = u1.followed_posts().all()
        f2 = u2.followed_posts().all()
        f3 = u3.followed_posts().all()
        f4 = u4.followed_posts().all()
        self.assertEqual(f1, [p2, p4, p1])
        self.assertEqual(f2, [p2, p3])
        self.assertEqual(f3, [p3, p4])
        self.assertEqual(f4, [p4])

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
