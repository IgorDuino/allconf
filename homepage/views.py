from django.shortcuts import render
from django.views.generic import View
from manager.models import Category, Lecture, Conference
from fuzzywuzzy import process


class HomeView(View):
    template_name = 'homepage/home.html'
    
    @staticmethod
    def get_queryset(request):
        pass

    def get(self, request):
        categories = Category.objects.all()
        
        context = {
            'categories': categories
        }

        return render(request, template_name=self.template_name, context=context)
    
    def post(self, request):
        categories = Category.objects.all()
        some_var = request.POST.getlist('checks')
        print(some_var)
        for category in categories:
            if request.POST.get(category.slug):
                pass
        
        lectures = Lecture.objects.all()
        conference = Conference.objects.all()
        
        search_text = request.POST.get('search')
        
        search_list = list(lectures) + list(conference)
        search_list = process.extract(search_text, search_list, limit=len(categories))
        search_list.sort(key=lambda x: x[1], reverse=True)
        search_list = list(map(lambda x: x[0], search_list))
                
        context = {
            'categories': categories,
            'search_list': search_list
        }

        return render(request, template_name=self.template_name, context=context)
