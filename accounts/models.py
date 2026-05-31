from django.contrib.auth.models import AbstractUser
from django.db import models

VILOYATLAR = [
    ('toshkent_sh', 'Toshkent shahri'),
    ('toshkent_v', 'Toshkent viloyati'),
    ('samarqand', 'Samarqand'),
    ('buxoro', 'Buxoro'),
    ('andijon', 'Andijon'),
    ('fargona', 'Farg\'ona'),
    ('namangan', 'Namangan'),
    ('qashqadaryo', 'Qashqadaryo'),
    ('surxondaryo', 'Surxondaryo'),
    ('jizzax', 'Jizzax'),
    ('sirdaryo', 'Sirdaryo'),
    ('xorazm', 'Xorazm'),
    ('navoiy', 'Navoiy'),
    ('qoraqalpogiston', 'Qoraqalpog\'iston'),
]

ROL_CHOICES = [
    ('oquvchi', 'O\'quvchi'),
    ('ustoz', 'Ustoz'),
    ('ota_ona', 'Ota-ona'),
    ('fuqaro', 'Fuqaro'),
]

class CustomUser(AbstractUser):
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default='oquvchi')
    viloyat = models.CharField(max_length=50, choices=VILOYATLAR, blank=True)
    tuman = models.CharField(max_length=100, blank=True)
    maktab_raqam = models.CharField(max_length=20, blank=True)
    sinf = models.IntegerField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    reyting = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_rol_display()})"


class Maktab(models.Model):
    raqam = models.CharField(max_length=20)
    viloyat = models.CharField(max_length=50, choices=VILOYATLAR)
    tuman = models.CharField(max_length=100)
    manzil = models.TextField(blank=True)
    reyting = models.FloatField(default=0.0)
    oquvchilar_soni = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.tuman} - {self.raqam}-maktab"

    class Meta:
        verbose_name = 'Maktab'
        verbose_name_plural = 'Maktablar'
