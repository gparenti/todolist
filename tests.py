#tests.py

from datetime import datetime, timedelta
import unittest
from app import app, db
from app.models import User, Todo

class UserModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        self.app_context = app.app_context() #diese und nächste Zeile aus offiziellem tutorial wegen shell Fehlermeldung
        self.app_context.push()
        db.create_all()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
    
    #testet, ob man  mit einem falschen und ob man mit dem richtigen Passwort anmelden kann
    def test_password_hasing(self):
        u = User(username ='susan')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

    def test_avatar(self):
        u = User(username='john', email='john@example.com')
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/d4c74594d841139328695756648b6bd6?d=identicon&s=128'))


    def test_create_users(self):
        #create four users
        u1 = User(username='john', email='john@example.com')
        u2 = User(username='susan', email='susan@example.com')
        u3 = User(username='mary', email='mary@example.com')
        u4 = User(username='david', email='david@example.com')
        db.session.add_all([u1, u2, u3, u4])


        #Kontrolliert, ob Tasks erstellt werden können
        now = datetime.utcnow()
        t1 = Todo(body="Erster Task", Complete=False, user_id=9999)
        t2 = Todo(body="Zweiter Task", Complete=True, user_id=9999)
        t3 = Todo(body="Dritter Task", Complete=True, user_id=9998)
        t4 = Todo(body="Vierter Task", Complete=False, user_id=9998)
        db.session.add_all([t1, t2, t3, t4])
        db.session.commit()

        #Kontrolliert, ob Tasks gelöscht werden können
        now = datetime.utcnow()
        t1 = Todo(body="Erster Task", Complete=False, user_id=9999)
        t2 = Todo(body="Zweiter Task", Complete=True, user_id=9999)
        t3 = Todo(body="Dritter Task", Complete=True, user_id=9998)
        t4 = Todo(body="Vierter Task", Complete=False, user_id=9998)
        db.session.delete_all([t1, t2, t3, t4])
        db.session.commit()

if __name__ == '__main__':
    unittest.main(verbosity=2)