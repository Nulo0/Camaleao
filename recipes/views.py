from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.http.response import Http404
from django.db.models import Q

from . import models


def home(request):
    recipes = models.Recipe.objects.filter(is_published=True).order_by('-id')
    return render(request, 'recipes/pages/home.html', context={
        'recipes': recipes,
    })


def category(request, category_id):
    recipes = get_list_or_404(
        models.Recipe.objects.filter(
            category__id=category_id, is_published=True)
        .order_by('-id')
    )

    return render(request, 'recipes/pages/category.html', context={
        'recipes': recipes,
        'title': f'{recipes[0].category.name} - Category | '
    })


def recipe(request, id):

    recipe = get_object_or_404(
        models.Recipe.objects.filter(
            id=id, is_published=True)
    )

    return render(request, 'recipes/pages/recipeView.html', context={
        'recipe': recipe,
        'isDetailPage': True,
    })
    
def search(request):
    search_term = request.GET.get('q', '').strip()
    
    if not search_term:
        raise Http404()
    
    recipes = models.Recipe.objects.filter(
        Q(
            Q(title__icontains = search_term) |
            Q(description__icontains = search_term)
        ),
        is_published = True
    ).order_by('-id')
    
    return render(request, 'recipes/pages/search.html', context={
        'page_title': f'Search for "{search_term}" |',
        'search_term': search_term,
        'recipes': recipes
    })
