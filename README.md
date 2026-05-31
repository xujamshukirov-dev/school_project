# EduNet - Maktab Platformasi

## O'rnatish va ishga tushirish

### 1. Python va Django o'rnatish
```bash
pip install django pillow
```

### 2. Migratsiyalarni bajarish
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Demo ma'lumotlar yaratish (ixtiyoriy)
```bash
python manage.py shell
# Yoki quyidagi skriptni bajaring:
```

### 4. Serverni ishga tushirish
```bash
python manage.py runserver
```

### 5. Brauzerda ochish
http://127.0.0.1:8000

---

## Tayyor hisob ma'lumotlari (demo)

| Login      | Parol     | Rol      |
|-----------|-----------|----------|
| admin     | admin123  | Superuser|
| oquvchi1  | test1234  | O'quvchi |
| ustoz1    | test1234  | Ustoz    |

---

## Loyiha tuzilmasi

```
maktab_loyiha/
├── config/          # Django sozlamalari
├── accounts/        # Foydalanuvchilar
├── main/            # Asosiy ilovalar
├── templates/       # HTML shablonlar
│   ├── base.html
│   ├── dashboard_base.html
│   ├── accounts/
│   └── main/
├── static/
│   └── css/style.css
└── manage.py
```

## Xususiyatlar

### Chap panel (Sidebar):
- 🇺🇿 O'zbekiston maktablari reytingi
- 🏙️ Viloyat maktablari
- 🏘️ Tuman maktablari
- 🏫 Mening maktabim
- 📝 Quiz Tests (inline test modali)
- ☀️ Yozgi tatil vazifalari
- 🏆 Musobaqalar

### Yuqori panel (Topbar):
- 📋 Davomat va baho (elektron jurnal)
- ✍️ Mening postim
- ⭐ Mening reytingim
- 😊 Mening xulqim
- 👨‍🏫 Ustoz reytingi
- 🏫 Maktab reytingi (tuman/viloyat/respublika)

### Ranglar:
- Asosiy: #2ecc71 (yashil)
- To'q: #1a9b52
- Fon: #f8fffe (juda och yashil-oq)
