from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Avg, Count
import json
from .models import Post, Davomat, TestNatija, Musobaqa, XulqBaho, FAN_CHOICES
from accounts.models import CustomUser, Maktab, VILOYATLAR


@login_required
def dashboard(request):
    user = request.user
    postlar = Post.objects.select_related('muallif').all()[:20]
    context = {
        'user': user,
        'postlar': postlar,
        'fanlar': FAN_CHOICES,
    }
    return render(request, 'main/dashboard.html', context)


@login_required
def uzbekiston_maktablari(request):
    maktablar = Maktab.objects.order_by('-reyting')
    # Demo data
    if not maktablar.exists():
        demo = [
            ('1', 'Toshkent shahri', 'Yunusobod', 95.5),
            ('23', 'Samarqand', 'Samarqand shahri', 92.3),
            ('7', 'Andijon', 'Andijon shahri', 91.0),
            ('15', 'Namangan', 'Namangan shahri', 89.7),
            ('4', 'Farg\'ona', 'Farg\'ona shahri', 88.2),
            ('11', 'Buxoro', 'Buxoro shahri', 87.9),
            ('9', 'Qashqadaryo', 'Qarshi', 86.5),
            ('3', 'Toshkent viloyati', 'Chirchiq', 85.0),
            ('18', 'Surxondaryo', 'Termiz', 84.3),
            ('6', 'Xorazm', 'Urganch', 83.7),
        ]
        maktablar_list = [{'raqam': r, 'viloyat': v, 'tuman': t, 'reyting': b} for r, v, t, b in demo]
        return render(request, 'main/uzbekiston_maktablari.html', {'maktablar': maktablar_list})
    return render(request, 'main/uzbekiston_maktablari.html', {'maktablar': maktablar})


@login_required
def viloyat_maktablari(request):
    user = request.user
    viloyat = user.viloyat
    maktablar = Maktab.objects.filter(viloyat=viloyat).order_by('-reyting')
    demo_data = [
        {'raqam': '1', 'tuman': 'Yunusobod', 'reyting': 95.5},
        {'raqam': '5', 'tuman': 'Mirzo Ulug\'bek', 'reyting': 93.2},
        {'raqam': '12', 'tuman': 'Chilonzor', 'reyting': 90.1},
        {'raqam': '3', 'tuman': 'Shayxontohur', 'reyting': 88.4},
        {'raqam': '7', 'tuman': 'Uchtepa', 'reyting': 85.0},
    ]
    return render(request, 'main/viloyat_maktablari.html', {
        'maktablar': maktablar if maktablar.exists() else demo_data,
        'viloyat': dict(VILOYATLAR).get(viloyat, viloyat)
    })


@login_required
def tuman_maktablari(request):
    user = request.user
    demo_data = [
        {'raqam': '1', 'reyting': 95.5},
        {'raqam': '4', 'reyting': 88.3},
        {'raqam': '9', 'reyting': 85.0},
        {'raqam': '12', 'reyting': 82.7},
        {'raqam': '15', 'reyting': 79.4},
    ]
    return render(request, 'main/tuman_maktablari.html', {
        'maktablar': demo_data,
        'tuman': user.tuman,
    })


@login_required
def mening_maktabim(request):
    user = request.user
    maktab_oquvchilari = CustomUser.objects.filter(
        maktab_raqam=user.maktab_raqam,
        viloyat=user.viloyat,
        tuman=user.tuman,
        rol='oquvchi'
    ).order_by('-reyting')[:20]
    return render(request, 'main/mening_maktabim.html', {
        'oquvchilar': maktab_oquvchilari,
        'maktab_raqam': user.maktab_raqam,
    })


@login_required
def quiz_tests(request):
    fan = request.GET.get('fan', '')
    context = {'fanlar': FAN_CHOICES, 'tanlangan_fan': fan}
    if fan:
        # Demo tests
        context['testlar'] = [
            {'id': 1, 'mavzu': 'Kvadrat tenglamalar', 'savollar': 10, 'vaqt': 15},
            {'id': 2, 'mavzu': 'Trigonometriya asoslari', 'savollar': 10, 'vaqt': 15},
            {'id': 3, 'mavzu': 'Logarifm', 'savollar': 8, 'vaqt': 12},
            {'id': 4, 'mavzu': 'Chiziqli tenglamalar', 'savollar': 10, 'vaqt': 15},
            {'id': 5, 'mavzu': 'Geometriya', 'savollar': 12, 'vaqt': 20},
        ]
    return render(request, 'main/quiz_tests.html', context)


@login_required
def mening_postim(request):
    if request.method == 'POST':
        matn = request.POST.get('matn', '').strip()
        if matn:
            Post.objects.create(muallif=request.user, matn=matn)
            return redirect('dashboard')
    return render(request, 'main/mening_postim.html')


@login_required
def mening_reytingim(request):
    user = request.user
    test_natijalari = TestNatija.objects.filter(oquvchi=user).order_by('-vaqt')[:10]
    davomatlar = Davomat.objects.filter(oquvchi=user).order_by('-sana')[:20]
    avg_baho = davomatlar.aggregate(Avg('baho'))['baho__avg'] or 0
    context = {
        'test_natijalari': test_natijalari,
        'davomatlar': davomatlar,
        'avg_baho': round(avg_baho, 1),
        'reyting': user.reyting,
    }
    return render(request, 'main/mening_reytingim.html', context)


@login_required
def davomat_baho(request):
    user = request.user
    davomatlar = Davomat.objects.filter(oquvchi=user).order_by('-sana')[:30]
    # Demo data
    demo = []
    from datetime import date, timedelta
    fanlar = ['matematika', 'fizika', 'ona_tili', 'ingliz_tili', 'tarix']
    holat_list = ['keldi', 'keldi', 'keldi', 'kech_keldi', 'keldi']
    for i, (f, h) in enumerate(zip(fanlar, holat_list)):
        demo.append({
            'sana': date.today() - timedelta(days=i),
            'fan': dict(FAN_CHOICES).get(f, f),
            'holat': h,
            'baho': [5, 4, 5, 3, 4][i],
        })
    return render(request, 'main/davomat_baho.html', {
        'davomatlar': davomatlar if davomatlar.exists() else demo
    })


@login_required
def mening_xulqim(request):
    user = request.user
    baholar = XulqBaho.objects.filter(oquvchi=user).order_by('-sana')
    avg_ball = baholar.aggregate(Avg('ball'))['ball__avg'] or 0
    demo = [
        {'rol': 'Ustoz', 'fikr': 'Juda faol va intizomli o\'quvchi', 'ball': 9},
        {'rol': 'Sinfdosh', 'fikr': 'Darsda doim yaxshi javob beradi', 'ball': 8},
        {'rol': 'Ustoz', 'fikr': 'Uyga vazifalarini muntazam bajaradi', 'ball': 10},
        {'rol': 'Sinfdosh', 'fikr': 'Do\'stona va mehribon', 'ball': 9},
        {'rol': 'Ustoz', 'fikr': 'Matematika fanida a\'lo o\'qiydi', 'ball': 10},
    ]
    return render(request, 'main/mening_xulqim.html', {
        'baholar': baholar if baholar.exists() else demo,
        'avg_ball': round(avg_ball, 1) if avg_ball else 9.2,
    })


@login_required
def ustoz_reytingi(request):
    ustozlar = CustomUser.objects.filter(rol='ustoz').order_by('-reyting')[:20]
    demo = [
        {'ismi': 'Abdullayev Akbar', 'fan': 'Matematika', 'reyting': 9.8, 'maktab': '1-maktab'},
        {'ismi': 'Xoliqova Nilufar', 'fan': 'Ingliz tili', 'reyting': 9.6, 'maktab': '5-maktab'},
        {'ismi': 'Toshmatov Sherzod', 'fan': 'Fizika', 'reyting': 9.4, 'maktab': '12-maktab'},
        {'ismi': 'Yusupova Dilorom', 'fan': 'Kimyo', 'reyting': 9.2, 'maktab': '7-maktab'},
        {'ismi': 'Karimov Jasur', 'fan': 'Tarix', 'reyting': 9.0, 'maktab': '3-maktab'},
    ]
    return render(request, 'main/ustoz_reytingi.html', {
        'ustozlar': ustozlar if ustozlar.exists() else demo
    })


@login_required
def maktab_reytingi(request):
    user = request.user
    context = {
        'tuman_reyting': 3,
        'viloyat_reyting': 12,
        'respublika_reyting': 87,
        'maktab_raqam': user.maktab_raqam,
        'tuman': user.tuman,
        'viloyat': dict(VILOYATLAR).get(user.viloyat, user.viloyat),
    }
    return render(request, 'main/maktab_reytingi.html', context)


@login_required
def musobaqalar(request):
    musobaqalar = Musobaqa.objects.all().order_by('-boshlanish')
    demo = [
        {'nomi': 'Eng Yaxshi Insho Musobaqasi', 'fan': 'Adabiyot', 'tavsif': 'Chorak yakunida eng yaxshi insho', 'boshlanish': '2024-12-01', 'tugash': '2024-12-31'},
        {'nomi': 'Matematika Olimpiadasi', 'fan': 'Matematika', 'tavsif': 'Maktablar orasidagi matematika bellashuvi', 'boshlanish': '2024-12-05', 'tugash': '2024-12-20'},
        {'nomi': 'She\'r Musobaqasi', 'fan': 'Adabiyot', 'tavsif': 'O\'zbek tili va adabiyotida she\'r yozish', 'boshlanish': '2024-12-10', 'tugash': '2024-12-25'},
        {'nomi': 'Fizika Musobaqasi', 'fan': 'Fizika', 'tavsif': 'Viloyat bo\'yicha fizika olimpiadasi', 'boshlanish': '2024-12-15', 'tugash': '2024-12-30'},
        {'nomi': 'Eng Yaxshi Post Musobaqasi', 'fan': 'Ona tili', 'tavsif': 'Oyning eng yaxshi post muallifi', 'boshlanish': '2024-12-01', 'tugash': '2024-12-31'},
    ]
    return render(request, 'main/musobaqalar.html', {
        'musobaqalar': musobaqalar if musobaqalar.exists() else demo
    })


@login_required
def yozgi_tatil(request):
    vazifalar = [
        {'nomi': 'Matematika Tahlil Testi', 'tavsif': '11-sinf matematika testlari to\'plami', 'ball': 50, 'tur': 'test'},
        {'nomi': 'Ingliz Tili Lug\'at', 'tavsif': '500 ta yangi so\'zni o\'rganing', 'ball': 30, 'tur': 'vazifa'},
        {'nomi': 'Online Dars - Fizika', 'tavsif': 'Yozda fizika bo\'yicha online meet', 'ball': 40, 'tur': 'online'},
        {'nomi': 'Kimyo Laboratoriya', 'tavsif': 'Virtual laboratoriya mashqlari', 'ball': 35, 'tur': 'amaliy'},
        {'nomi': 'Tarix Esse Yozish', 'tavsif': 'O\'zbekiston tarixi bo\'yicha esse', 'ball': 25, 'tur': 'ijodiy'},
    ]
    return render(request, 'main/yozgi_tatil.html', {'vazifalar': vazifalar})


@require_POST
@login_required
def post_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.liked_by.all():
        post.liked_by.remove(request.user)
        liked = False
    else:
        post.liked_by.add(request.user)
        liked = True
    return JsonResponse({'liked': liked, 'count': post.liked_by.count()})
