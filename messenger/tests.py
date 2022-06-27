from concurrent.futures import thread
from email import message
from django.test import TestCase
from django.conf import settings
from cuentas.models import Account
from .models import Thread, Message

class ThreadTestCase(TestCase):
    def setUp(self):
        self.user1 = Account.objects.create_user('Sergio', 'Lopez', '1112341234', 'f@f.com', 'test1234')
        self.user2 = Account.objects.create_user('martin', 'pepe', '112222333', 'g@g.com', 'test1235')
        self.user3 = Account.objects.create_user('Ana', 'Soler', '1133334444', 'as@as.com', 'test1233')

        self.thread = Thread.objects.create()

    def test_add_user_to_thread(self):
        self.thread.users.add(self.user1, self.user2)
        self.assertEqual(len(self.thread.users.all()),2)

    def test_filter_thread_by_users(self):
        self.thread.users.add(self.user1, self.user2)
        threads = Thread.objects.filter(users=self.user1).filter(users=self.user2)
        self.assertEqual(self.thread, threads[0])
    
    def test_filter_non_existent_thread(self):
        threads = Thread.objects.filter(users=self.user1).filter(users=self.user2)
        self.assertEqual(len(threads),0)
    
    def test_add_messages_to_thread(self):
        self.thread.users.add(self.user1, self.user2)
        message1 = Message.objects.create(user=self.user1, content="Hola como estas?")
        message2 = Message.objects.create(user=self.user2, content="todo bien, vos?")
        message3 = Message.objects.create(user=self.user3, content="Este mensaje no es de este hilo")
        self.thread.messages.add(message1,message2, message3)
        self.assertEqual(len(self.thread.messages.all()),2)

        for message in self.thread.messages.all():
            print("({}): {}".format(message.user, message.content))
    
    def test_find_thread_with_custom_manager(self):
        self.thread.users.add(self.user1, self.user2)
        thread = Thread.objects.find(self.user1, self.user2)
        self.assertEqual(self.thread, thread)
    
    def test_find_or_create_thread_with_custom_manager(self):
        self.thread.users.add(self.user1, self.user2)
        thread = Thread.objects.find_or_create(self.user1, self.user2)
        self.assertEqual(self.thread, thread)
        thread = Thread.objects.find_or_create(self.user1, self.user3)
        self.assertIsNotNone(thread)