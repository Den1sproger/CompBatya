from django.db import models



class Devices(models.Model):
    TYPE_CHOICES = {
        'laptop': 'Ноутбук',
        'su': 'компьютер',
        'monitor': 'Монитор',
        'tablet': 'Планшет',
        'smartphone': 'смартфон',
    }
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    model = models.ForeignKey('Models',
                              on_delete=models.SET_NULL,
                              null=True)
    age = models.PositiveSmallIntegerField(null=True, blank=True)
    owner = models.ForeignKey('Owners',
                              on_delete=models.SET_NULL,
                              null=True)
    specialists = models.ManyToManyField('Specialists', related_name='devices')
    services = models.ManyToManyField('Services', related_name='services')



class Models(models.Model):
    name = models.CharField(max_length=255)
    brand = models.ForeignKey('Brands', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name



class Brands(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    


class Owners(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=200)
    email = models.EmailField(max_length=80, null=True, blank=True)


    def __str__(self):
        return self.name



class Requests(models.Model):
    manager = models.ForeignKey('Managers',
                                on_delete=models.SET_NULL,
                                null=True)
    client = models.ForeignKey('Owners',
                               on_delete=models.SET_NULL,
                               null=True, blank=True)
    time = models.DateTimeField(auto_now_add=True)
    


class Managers(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)


    def __str__(self):
        return f'{self.last_name} {self.first_name}'



class Specialists(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    PROFILE_CHOICES = {
        'mobile': 'Мобильные устройства',
        'desktop': 'Компьютеры'
    }
    profile = models.CharField(max_length=32)


    def __str__(self):
        return f'{self.last_name} {self.first_name}'



class Services(models.Model):
    PROFILE_CHOICES = {
        'mobile': 'Мобильные устройства',
        'desktop': 'Компьютеры'
    }
    name = models.CharField(max_length=255)
    profile = models.CharField(max_length=7, choices=PROFILE_CHOICES)
    price = models.PositiveSmallIntegerField()


    def __str__(self):
        return self.name