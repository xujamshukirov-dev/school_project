from django.db import models
from accounts.models import CustomUser

FAN_CHOICES = [
    ('matematika', 'Matematika'),
    ('fizika', 'Fizika'),
    ('kimyo', 'Kimyo'),
    ('biologiya', 'Biologiya'),
    ('tarix', 'Tarix'),
    ('geografiya', 'Geografiya'),
    ('adabiyot', 'Adabiyot'),
    ('ona_tili', 'Ona tili'),
    ('ingliz_tili', 'Ingliz tili'),
    ('informatika', 'Informatika'),
    ('chizmachilik', 'Chizmachilik'),
    ('jismoniy', 'Jismoniy tarbiya'),
]


class Post(models.Model):
    muallif = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='postlar')
    matn = models.TextField()
    rasm = models.ImageField(upload_to='posts/', blank=True, null=True)
    reyting = models.FloatField(default=0.0)
    liked_by = models.ManyToManyField(CustomUser, related_name='liked_posts', blank=True)
    yaratilgan = models.DateTimeField(auto_now_add=True)
    tasdiqlangan = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.muallif.username}: {self.matn[:50]}"

    class Meta:
        ordering = ['-reyting', '-yaratilgan']


class Davomat(models.Model):
    oquvchi = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='davomatlar')
    sana = models.DateField()
    fan = models.CharField(max_length=50, choices=FAN_CHOICES)
    holat = models.CharField(max_length=20, choices=[
        ('keldi', 'Keldi'),
        ('kelmadi', 'Kelmadi'),
        ('kech_keldi', 'Kech keldi'),
        ('sababli', 'Sababli'),
    ])
    baho = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.oquvchi.username} - {self.sana} - {self.fan}"

    class Meta:
        ordering = ['-sana']


class TestNatija(models.Model):
    oquvchi = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='test_natijalari')
    fan = models.CharField(max_length=50, choices=FAN_CHOICES)
    mavzu = models.CharField(max_length=200)
    ball = models.IntegerField()
    max_ball = models.IntegerField(default=10)
    vaqt = models.DateTimeField(auto_now_add=True)

    def foiz(self):
        return round((self.ball / self.max_ball) * 100)

    def __str__(self):
        return f"{self.oquvchi.username} - {self.fan} - {self.ball}/{self.max_ball}"


class Musobaqa(models.Model):
    nomi = models.CharField(max_length=200)
    fan = models.CharField(max_length=50, choices=FAN_CHOICES)
    tavsif = models.TextField()
    boshlanish = models.DateField()
    tugash = models.DateField()
    ishtirokchilar = models.ManyToManyField(CustomUser, related_name='musobaqalar', blank=True)
    rasm = models.ImageField(upload_to='musobaqalar/', blank=True, null=True)

    def __str__(self):
        return self.nomi


class XulqBaho(models.Model):
    oquvchi = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='xulq_baholar')
    baho_beruvchi = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='bergan_baholar')
    rol = models.CharField(max_length=20)
    fikr = models.TextField()
    ball = models.IntegerField(default=5)
    sana = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.oquvchi.username} - {self.ball}/10"
