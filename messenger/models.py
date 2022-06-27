from django.db import models
from django.conf import settings
from django.db.models.signals import m2m_changed

#apunto el modelo de User al modelo configurado en settings en AUTH_USER_MODEL
class Message(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering =['created']
        verbose_name = "mensaje"
        verbose_name_plural = "mensajes"

class ThreadManager(models.Manager):
    def find(self, user1, user2):
        queryset = self.filter(users=user1).filter(users=user2)
        if len(queryset)>0:
            return queryset[0]
        return None

    def find_or_create(self, user1, user2):
        thread = self.find(user1, user2)
        if thread is None:
            thread = Thread.objects.create()
            thread.users.add(user1, user2)
        return thread

class Thread(models.Model):
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='threads')
    messages = models.ManyToManyField(Message)
    updated = models.DateTimeField(auto_now=True)

    objects = ThreadManager()

    class Meta:
        ordering =['-updated']
        verbose_name = "hilo"
        verbose_name_plural = "hilos"

def messages_changed(sender, **kwargs):
    instance = kwargs.pop("instance", None)
    action = kwargs.pop("action", None)
    pk_set = kwargs.pop("pk_set", None)
    print (instance, action, pk_set)

    false_pk_set = set()
    if action is "pre_add":
        for msg_pk in pk_set:
            msg = Message.objects.get(pk=msg_pk)
            if msg.user not in instance.users.all():
                print("Ups, ({}) no forma parte del hillo".format(msg.user))
                false_pk_set.add(msg_pk)
    
    #Busco los mensajes de false_pk_set que estan en el pk_set y los borramos del hilo original
    pk_set.difference_update(false_pk_set)

    #Fuerzo la actualización para que se guarde la hora del mensaje
    instance.save()
    
#conecto la señal messages_changed con cualquier cosa que pase en el ManyToMany de messages en clase Thread
m2m_changed.connect(messages_changed, sender=Thread.messages.through)