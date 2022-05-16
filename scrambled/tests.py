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
        test_susan = User(username='ben')
        test_susan.set_password('shayan')
        test_admin = User(username='admin')
        test_admin.set_password('admin')
        self.assertFalse(test_admin.check_password('test'))
        self.assertTrue(test_admin.check_password('admin'))
        self.assertFalse(test_susan.check_password('dog'))
        self.assertTrue(test_susan.check_password('shayan'))

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
        user_ben = User(username='ben', email='ben@scrambled.com')
        user_sameer = User(username='sameer', email='sameer@scrambled.com')
        user_admin = User(username='admin', email='admin@scrambled.com')
        user_shayan = User(username='shayan', email='shayan@scrambled.com')
        db.session.add(user_ben)
        db.session.add(user_sameer)
        db.session.add(user_admin)
        db.session.add(user_shayan)
        db.session.commit()
        self.assertEqual(user_ben.followed.all(), [])
        self.assertEqual(user_ben.followers.all(), [])

        user_ben.follow(user_sameer)
        db.session.commit()
        self.assertTrue(user_ben.is_following(user_sameer))
        self.assertEqual(user_ben.followed.count(), 1)
        self.assertEqual(user_ben.followed.first().username, 'sameer')
        self.assertEqual(user_sameer.followers.count(), 1)
        self.assertEqual(user_sameer.followers.first().username, 'ben')

        user_ben.unfollow(user_sameer)
        db.session.commit()
        self.assertFalse(user_ben.is_following(user_sameer))
        self.assertEqual(user_ben.followed.count(), 0)
        self.assertEqual(user_sameer.followers.count(), 0)

        user_sameer.follow(user_admin)
        db.session.commit()
        self.assertTrue(user_sameer.is_following(user_admin))
        self.assertEqual(user_admin.followers.first().username,'sameer')

        user_shayan.follow(user_admin)
        db.session.commit()
        self.assertTrue(user_shayan.is_following(user_admin))
        self.assertEqual(user_admin.followers.count(),2)

    def test_follow_posts(self):
        # create four users
        user_admin = User(username='admin', email='admin@scrambled.com')
        user_ben = User(username='ben', email='ben@scrambled.com')
        user_shayan = User(username='shayan', email='shayan@scrambled.com')
        user_sameer = User(username='sameer', email='sameer@scrambled.com')
        db.session.add_all([user_admin, user_ben, user_shayan, user_sameer])

        # create four posts
        now = datetime.utcnow()
        post_admin = Post(body="post from admin", author=user_admin,
                  timestamp=now + timedelta(minutes=1))
        post_ben = Post(body="post from ben", author=user_ben,
                  timestamp=now + timedelta(minutes=20))
        post_shayan = Post(body="post form shayan", author=user_shayan,
                  timestamp=now + timedelta(hours=3))
        post_sameer = Post(body="post from sameer", author=user_sameer,
                  timestamp=now + timedelta(hours=2))
        db.session.add_all([post_admin, post_ben, post_shayan, post_sameer])
        db.session.commit()

        # setup the followers
        user_admin.follow(user_ben)  
        user_admin.follow(user_sameer) 
        user_ben.follow(user_shayan) 
        user_shayan.follow(user_sameer)  
        db.session.commit()

        # check the followed posts of each user
        check_1 = user_admin.followed_posts().all()
        check_2 = user_ben.followed_posts().all()
        check_3 = user_shayan.followed_posts().all()
        check_4 = user_sameer.followed_posts().all()
        self.assertEqual(check_1, [post_sameer, post_ben,post_admin])
        self.assertEqual(check_2, [post_shayan,post_ben ])
        self.assertEqual(check_3, [post_shayan, post_sameer])
        self.assertEqual(check_4, [post_sameer])

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
