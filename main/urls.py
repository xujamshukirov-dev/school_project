from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('uzbekiston/', views.uzbekiston_maktablari, name='uzbekiston_maktablari'),
    path('viloyat/', views.viloyat_maktablari, name='viloyat_maktablari'),
    path('tuman/', views.tuman_maktablari, name='tuman_maktablari'),
    path('maktabim/', views.mening_maktabim, name='mening_maktabim'),
    path('quiz/', views.quiz_tests, name='quiz_tests'),
    path('post/', views.mening_postim, name='mening_postim'),
    path('reyting/', views.mening_reytingim, name='mening_reytingim'),
    path('davomat/', views.davomat_baho, name='davomat_baho'),
    path('xulq/', views.mening_xulqim, name='mening_xulqim'),
    path('ustoz-reyting/', views.ustoz_reytingi, name='ustoz_reytingi'),
    path('maktab-reyting/', views.maktab_reytingi, name='maktab_reytingi'),
    path('musobaqalar/', views.musobaqalar, name='musobaqalar'),
    path('yozgi-tatil/', views.yozgi_tatil, name='yozgi_tatil'),
    path('post/<int:post_id>/like/', views.post_like, name='post_like'),
]
