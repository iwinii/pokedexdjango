from django.db import models
from django.contrib.auth.models import AbstractUser

class Pokemon(models.Model):
    # id = models.PositiveIntegerField()
    poke_id = models.PositiveIntegerField()
    name = models.CharField(max_length=150)
    type_1 = models.CharField(max_length=150)
    type_2 = models.CharField(max_length=150)
    total = models.IntegerField()
    hp = models.IntegerField()
    attack = models.IntegerField()
    defence = models.IntegerField()
    sp_attack = models.IntegerField()
    sp_defence = models.IntegerField()
    speed = models.IntegerField()
    generation = models.SmallIntegerField()
    legendary = models.CharField(max_length=150)

#

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    class Meta:
        db_table = 'auth_user'
    legendary = models.CharField(max_length=150, null=True, blank=True)
    favourite_pokemon = models.ManyToManyField(Pokemon)




