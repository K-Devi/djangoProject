from rest_framework import serializers

from .models import *


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ('id', 'name', 'description')


class ChapterSerializer(serializers.ModelSerializer):
    subjectid = SubjectSerializer

    class Meta:
        model = Chapter
        fields = ('id', 'name', 'subjectid')


class QuestionThemeSerializer(serializers.ModelSerializer):
    chapterid = ChapterSerializer

    class Meta:
        model = QuestionTheme
        fields = ('id', 'name', 'chapterid')


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class ImageCatalogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageCatalog
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'


class TopicRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopicRule
        fields = '__all__'
