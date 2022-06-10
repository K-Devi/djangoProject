import random
import pdfkit
# from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.http import HttpResponse, JsonResponse

# from django.shortcuts import render
from django.template.loader import get_template
from django.views import View
from rest_framework import viewsets
# from rest_framework.response import Response

# from .models import *

from .serializers import *

# Create your views here.

class Login(View):
    def post(self, request):
        user = request.POST.get('username')
        password = request.POST.get('password')
        obj = auth.authenticate(request, username=user, password=password)
        if obj:
            return HttpResponse('Ok')


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

    def get_queryset(self):
        return self.queryset.filter(profile__subject__id=self.request.user.id)


class ChaptersViewSet(viewsets.ModelViewSet):

    # http://127.0.0.1:8000/chapters/ Get список разделов Post создание новой ТОЛЬКО название раздела текстовое поле

    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer

    def list(self, request, *args, **kwargs):
        if request.method == 'GET':
            subjectid = request.GET.get('subjectid')
            data = self.queryset.filter(subjectid=1).values()
            return JsonResponse({"models_to_return": list(data)})


class QuestionThemeViewSet(viewsets.ModelViewSet):
    queryset = QuestionTheme.objects.all()
    serializer_class = QuestionThemeSerializer

    def list(self, request, *args, **kwargs):
        if request.method == 'GET':
            chapterid = request.GET.get('chapterid')
            data = self.queryset.filter(chapterid=chapterid).values()
            return JsonResponse({"models_to_return": list(data)})


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def list(self, request, *args, **kwargs):
        if request.method == 'GET':
            questionthemeid = request.GET.get('questionthemeid')
            data = self.queryset.filter(questionthemeid=questionthemeid).values()
            return JsonResponse({"models_to_return": list(data)})

class CatalogViewSet(viewsets.ModelViewSet):
    queryset = ImageCatalog.objects.all()
    serializer_class = ImageCatalogSerializer



class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    def list(self, request, *args, **kwargs):
        if request.method == 'GET':
            catalogid = request.GET.get('catalogid')
            data = self.queryset.filter(catalog__id=catalogid).values()
            return JsonResponse({"models_to_return": list(data)})


class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer


class TopicRuleViewSet(viewsets.ModelViewSet):
    queryset = TopicRule.objects.all()
    serializer_class = TopicRuleSerializer

    def list(self, request, *args, **kwargs):
        if request.method == 'GET':
            topicid = request.GET.get('topicid')
            return HttpResponse(self.queryset.filter(topicid=topicid), content_type="application/json")


# @login_required
def topic_generator(request):
    if request.method == 'POST':
        variants = request.POST.get('variants')
        topic = request.POST.get('topicid')
        rules = TopicRule.objects.filter(topicid=topic)
        tasks = []

        for variant in variants:
            qnumber = 0
            for rule in rules:
                count = rule.questionscount
                theme = rule.questionthemeid
                type = rule.questiontypeid
                questions = list(Question.objects.filter(questionthemeid=theme, questiontypeid=type))
                questions = random.sample(questions, count)
                tasks += questions
                qnumber += count
            return tasks, qnumber

        context = {
            "name": topic.name,
            "subject": topic.chapterid.subjectid.name,
            "chapter": topic.chapterid.name,
            "variants": variants,
            "list": tasks,
        }

        template = get_template('pdf.html')
        html = template.render(context=context)
        pdf = pdfkit.from_string(html, False, options={})

        response = HttpResponse(pdf, content_type='topic/pdf')
        response['Content-Disposition'] = 'attachment; filename="test.pdf"'

        return response






