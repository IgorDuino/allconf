from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from django.views.generic import View, FormView
from manager.models import Category, Lecture, Conference
from django.shortcuts import get_object_or_404
from manager.forms import ConferenceCreateForm, LectureCreateForm
from users.models import ConferenceOrganizer, Speaker
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class ConfView(View):
    template_name = 'manager/conf-detail.html'

    def get(self, request, conf_slug):
        conference = get_object_or_404(Conference.objects.get_conference_with_lectures_and_category(), 
                                       slug=conf_slug)
        
        context = {
            'conf': conference
        }

        return render(request, template_name=self.template_name, context=context)


class LectureView(View):
    template_name = 'manager/lecture-detail.html'

    def get(self, request, conf_slug, lecture_slug):
        conference = get_object_or_404(Conference.objects.get_conference_with_lectures(), 
                                       slug=conf_slug)
        lecture = get_object_or_404(conference.lectures.all().prefetch_related('category'),
                                    slug=lecture_slug)
        
        context = {
            'lecture': lecture
        }

        return render(request, template_name=self.template_name, context=context)
    

class CreateConferenceView(View):
    template_name = 'manager/conf-create.html'
    form_class = ConferenceCreateForm
    
    def get(self, request):
        form = self.form_class()

        context = {
            'form': form
        }

        return render(request, template_name=self.template_name, context=context)
    
    @method_decorator(login_required)
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            slug = form.cleaned_data['slug']
            category = form.cleaned_data['category']
            date = form.cleaned_data['date']
            
            conf = Conference.objects.filter(title=title)
            
            if len(conf) == 0:
                conf = Conference.objects.create(
                    title=title,
                    description=description,
                    slug=slug,
                    category=category,
                    date=date,
                    is_active=True
                )
                
                ConferenceOrganizer.objects.create(
                    user=request.user,
                    conference=conf
                )
            
                return HttpResponseRedirect(reverse('manager:conf-detail', kwargs={'conf_slug': slug}))

        context = {
            'form': form
        }

        return render(request, template_name=self.template_name, context=context)

class CreateLectureView(View):
    template_name = 'manager/lecture-create.html'
    form_class = LectureCreateForm
    
    def get(self, request):
        form = self.form_class()

        context = {
            'form': form
        }

        return render(request, template_name=self.template_name, context=context)
        
    @method_decorator(login_required)
    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            slug = form.cleaned_data['slug']
            category = form.cleaned_data['category']
            conference = form.cleaned_data['conference']
            file = form.cleaned_data['file']
            
            lecture = Lecture.objects.filter(title=title)
            
            if len(lecture) == 0:
                lecture = Lecture.objects.create(
                    title=title,
                    description=description,
                    slug=slug,
                    category=category,
                    conference=conference,
                    file=file,
                    is_active=True
                )
                
                Speaker.objects.create(
                    user=request.user,
                    lecture=lecture
                )
            
                return HttpResponseRedirect(reverse('manager:lecture-detail', kwargs={'conf_slug': slug, 'lecture_slug': slug}))
        
        context = {
            'form': form
        }

        return render(request, template_name=self.template_name, context=context)