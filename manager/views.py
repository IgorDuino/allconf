from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from django.views.generic import View
from manager.models import Category, Lecture, Conference
from django.shortcuts import get_object_or_404
from manager.forms import ConferenceCreateForm, LectureCreateForm, ConferenceChangeForm
from users.models import ConferenceOrganizer, ConferenceModerator, Speaker, Listener
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import Http404


class ConfView(View):
    template_name = 'manager/conf-detail.html'

    def get(self, request, conf_slug):
        conference = get_object_or_404(Conference.objects.get_conference_with_lectures_and_category(), 
                                       slug=conf_slug)
        
        context = {
            'conf': conference
        }

        return render(request, template_name=self.template_name, context=context)
    
    
    @method_decorator(login_required)
    def post(self, request, conf_slug):
        conference = get_object_or_404(Conference.objects.get_conference_with_lectures_and_category(), 
                                       slug=conf_slug)

        if request.POST.get('speaker'):
            return HttpResponseRedirect(reverse('manager:lecture-create'))
        if request.POST.get('listener'):
            listener = Listener.objects.filter(user=request.user, conference=conference)
            if len(listener) == 0:
                Listener.objects.create(
                    conference=conference,
                    user=request.user
                )
                
                return HttpResponseRedirect(reverse('users:profile'))
        
        context = {
            'conf': conference
        }

        return render(request, template_name=self.template_name, context=context)
    

@method_decorator(login_required, name='dispatch')
class ConfAdminView(View):
    template_name = 'manager/conf-admin.html'
    form_class = ConferenceChangeForm
    
    @staticmethod
    def check_permission(request, conference):
        user = request.user
        
        orginizer_permission = len(ConferenceOrganizer.objects.filter(user=user, conference=conference)) != 0
        moderator_permission = len(ConferenceModerator.objects.filter(user=user, conference=conference)) != 0
        
        return orginizer_permission or moderator_permission

    def get(self, request, conf_slug):
        conference = get_object_or_404(Conference.objects.get_conference_with_all_lectures_and_category(), 
                                       slug=conf_slug)
        
        if self.check_permission(request, conference):
            form = self.form_class()
            
            context = {
                'form': form,
                'conf': conference
            }
            
            return render(request, template_name=self.template_name, context=context)
        else:
            raise Http404("You haven't enough permissions")
    
    
    def post(self, request, conf_slug):
        conference = get_object_or_404(Conference.objects.get_conference_with_all_lectures_and_category(),
                                       slug=conf_slug)

        
        if self.check_permission(request, conference):
            form = self.form_class(request.POST, request.FILES)
            
            if form.is_valid():
                description = form.cleaned_data['description']
                category = form.cleaned_data['category']
                date = form.cleaned_data['date']
                image = form.cleaned_data['upload']
                conference.description = description
                conference.category = category
                conference.upload = image
                conference.date = date
                conference.save(update_fields=['description', 'category', 'date', 'upload'])
            
            if request.POST.get('time_manager'):
                for lecture in conference.lectures.all():
                    if request.POST.get(lecture.slug + '_active'):
                        if request.POST.get(lecture.slug):
                            time = request.POST.get(lecture.slug)
                            lecture.time = time
                        lecture.confirmed = True
                        lecture.save(update_fields=['time', 'confirmed'])
                    else:
                        lecture.confirmed = False
                        lecture.save(update_fields=['confirmed'])
            
            context = {
                'form': form,
                'conf': conference
            }

            return render(request, template_name=self.template_name, context=context)
        else:
            raise Http404("You haven't enough permissions")
            

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
        form = self.form_class(request.POST, request.FILES)
        
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            slug = form.cleaned_data['slug']
            category = form.cleaned_data['category']
            date = form.cleaned_data['date']
            image = form.cleaned_data['upload']
            
            conf = Conference.objects.filter(title=title)
            
            if len(conf) == 0:
                conf = Conference.objects.create(
                    title=title,
                    description=description,
                    slug=slug,
                    category=category,
                    date=date,
                    upload=image,
                    is_active=True,
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
            
                return HttpResponseRedirect(reverse('manager:lecture-detail', kwargs={'conf_slug': conference.slug, 'lecture_slug': slug}))
        
        context = {
            'form': form
        }

        return render(request, template_name=self.template_name, context=context)