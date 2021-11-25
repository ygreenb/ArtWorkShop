from django.shortcuts import render
from artwork.models import Work

# Create your views here.
def langing(request):
    #recent_posts = Work.objects.order_by('-pk')[:3] # 최신 포스트
    return render(request, 'single_pages/landing.html')
                #  {'recent_posts' : recent_posts})

def about_us(request):
    return render(request, 'single_pages/about_us.html')