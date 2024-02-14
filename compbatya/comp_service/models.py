from django.db import models



class Devices(models.Model):
    class Status(models.IntegerChoices):
        FAIL = 0, 'Не выполнен/Выполнен плохо'
        SUCCESS = 1, 'Успешно выполнен'

    TYPE_CHOICES = [
        ('laptop', 'Ноутбук'),
        ('su', 'Компьютер'),
        ('monitor', 'Монитор'),
        ('tablet', 'Планшет'),
        ('smartphone', 'Смартфон'),
    ]
    type = models.CharField(max_length=10,
                            choices=TYPE_CHOICES,
                            verbose_name='Тип устройства')
    model = models.ForeignKey('Models',
                              on_delete=models.SET_NULL,
                              null=True, verbose_name='Модель')
    year = models.PositiveSmallIntegerField(null=True, blank=True,
                                            verbose_name='Год выпуска')
    owner = models.ForeignKey('Owners',
                              on_delete=models.SET_NULL,
                              null=True, verbose_name='Владелец')
    status = models.BooleanField(choices=Status.choices,
                                 null=True, blank=True,
                                 verbose_name='Статус')
    create_time = models.DateTimeField(auto_now_add=True)
    specialists = models.ManyToManyField('Specialists', related_name='devices',
                                         verbose_name='Специалисты')
    services = models.ManyToManyField('Services', related_name='devices',
                                      verbose_name='Услуги')


    class Meta:
        verbose_name = 'устройство'
        verbose_name_plural = 'Устройства в ремонте'


    def __str__(self) -> str:
        return f'{self.type} | {self.model} | {self.year}'
    



class Models(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    brand = models.ForeignKey('Brands', on_delete=models.SET_NULL,
                              null=True, verbose_name='Бренд')


    class Meta:
        verbose_name = 'модель'
        verbose_name_plural = 'Модели'


    def __str__(self):
        return self.name



class Brands(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')


    class Meta:
        verbose_name = 'бренд'
        verbose_name_plural = 'Бренды'


    def __str__(self):
        return self.name
    


class Owners(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя')
    phone_number = models.CharField(max_length=200, verbose_name='Телефон')
    email = models.EmailField(max_length=80,
                              null=True, blank=True,
                              verbose_name='Почта')


    class Meta:
        verbose_name = 'владелец'
        verbose_name_plural = 'Вдадельцы устройств'


    def __str__(self):
        return self.name



class Requests(models.Model):
    manager = models.ForeignKey('Managers',
                                on_delete=models.SET_NULL,
                                null=True, blank=True,
                                related_name='requests',
                                verbose_name='Менеджер')
    client = models.ForeignKey('Owners',
                               on_delete=models.SET_NULL,
                               null=True, blank=True,
                               related_name='requests',
                               verbose_name='Клиент')
    time = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name = 'заявка'
        verbose_name_plural = 'Заявки на обратный звонок'


    def __str__(self):
        return str(self.time)
    


class Managers(models.Model):
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')


    class Meta:
        verbose_name = 'менеджер'
        verbose_name_plural = 'Менеджеры'


    def __str__(self):
        return f'{self.last_name} {self.first_name}'



class Specialists(models.Model):
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')
    PROFILE_CHOICES = {
        'mobile': 'Мобильные устройства',
        'desktop': 'Компьютеры'
    }
    profile = models.CharField(max_length=32, verbose_name='Специализация')
    image = models.ImageField(max_length=300,
                              upload_to='employee_images/',
                              default=None, blank=True, null=True,
                              verbose_name='Фото')


    class Meta:
        verbose_name = 'специалист'
        verbose_name_plural = 'Специалисты'


    def __str__(self):
        return f'{self.last_name} {self.first_name} | {self.profile}'



class Services(models.Model):
    PROFILE_CHOICES = [
        ('mobile', 'Мобильные устройства'),
        ('desktop', 'Компьютеры'),
    ]
    name = models.CharField(max_length=255, verbose_name='Название')
    profile = models.CharField(max_length=7, choices=PROFILE_CHOICES,
                               verbose_name='Профиль')
    price = models.PositiveSmallIntegerField(verbose_name='Цена')


    class Meta:
        verbose_name = 'услуга'
        verbose_name_plural = 'Услуги'


    def __str__(self):
        return f'{self.name} | {Specialists.PROFILE_CHOICES[self.profile]}'