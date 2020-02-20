from django.db import models

class Level(models.Model):
    name = models.CharField(max_length = 255)
    image = models.CharField(max_length = 255)
    world = models.ForeignKey('World' ,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Player(models.Model):
    login = models.CharField(max_length = 125)
    nb_stars = models.IntegerField(default=0)            #min & max
    time = models.IntegerField(default=0)
    id_level = models.ForeignKey('Level' ,on_delete=models.CASCADE)
    detail1 = models.BooleanField(default=False)
    detail2 = models.BooleanField(default=False)
    detail3 = models.BooleanField(default=False)
    detail4 = models.BooleanField(default=False)
    detail5 = models.BooleanField(default=False)


class Detail(models.Model):
    image = models.CharField(max_length = 255)
    position_x = models.IntegerField()
    position_y = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()
    id_level = models.ForeignKey('Level' ,on_delete=models.CASCADE)

class World(models.Model):
    name = models.CharField(max_length = 255)

    def __str__(self):
        return self.name
