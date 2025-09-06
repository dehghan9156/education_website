from .models import Category 


def categories_processors(request):
    return {
        'root_category':Category.objects.filter(level=0),
        }
    