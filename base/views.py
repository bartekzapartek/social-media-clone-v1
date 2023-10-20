from django.shortcuts import render


def home_view(request):

    context = {}
    return render(request, 'base/home.html', context)


def explore_view(request):

    context = {}
    return render(request, 'base/home.html', context)

def post_view(request, pk):
    
    context = {}
    return render(request, 'base/post.html', context)


def user_profile_view(request, pk):

    context = {}
    return render(request, 'base/home.html', context)