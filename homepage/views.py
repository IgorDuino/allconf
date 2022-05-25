from django.shortcuts import render
from django.views.generic import View, TemplateView
from manager.models import Category, Lecture, Conference
from fuzzywuzzy import process


class HomeView(TemplateView):
    template_name = 'homepage/home.html'


class SearchView(View):
    template_name = 'homepage/search.html'
    
    def get(self, request):
        conference = Conference.objects.filter(is_active=True).select_related('category')
        
        search_text = request.GET.get('search', '')
        
        search_list = list(conference)
        search_list = process.extract(search_text, search_list, limit=len(search_list))
        search_list.sort(key=lambda x: x[1], reverse=True)
        search_list = list(map(lambda x: x[0], search_list))

        context = {
            'search_list': search_list,
            'search_phrase': search_text
        }

        return render(request, template_name=self.template_name, context=context)
