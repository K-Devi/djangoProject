from django.contrib.auth.models import User
from django.db import models


# Create your models here

class Subject(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subject = models.ManyToManyField(Subject)


class Chapter(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)
    subjectid = models.ForeignKey(Subject, models.CASCADE)
    name = models.TextField(db_column='Name', blank=True, null=True)

    def __str__(self):
        return self.name


class QuestionTheme(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(blank=True, null=True)
    chapterid = models.ForeignKey(Chapter, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Grade(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)
    gradenumber = models.IntegerField(db_column='GradeNumber')
    description = models.TextField(db_column='Description', blank=True, null=True)

    def __str__(self):
        return self.description


class QuestionType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class ImageCatalog(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(max_length=100)

    def __str__(self):
        return self.name


class Question(models.Model):
    id = models.AutoField(primary_key=True)
    questiontypeid = models.ForeignKey(QuestionType, models.DO_NOTHING,
                                       db_column='QuestionTypeId')
    questionthemeid = models.ForeignKey(QuestionTheme, models.DO_NOTHING,
                                        db_column='QuestionThemeId')
    body = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)
    catalog = models.ForeignKey(ImageCatalog, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return self.body


class GradeQuestion(models.Model):
    gradesid = models.OneToOneField(Grade, models.CASCADE,
                                    primary_key=True)
    questiontypeid = models.ForeignKey(QuestionType, models.CASCADE,
                                   default=1 )

    def __str__(self):
        return self.gradesid.description


class Image(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='1',blank=True, null=True)
    catalog = models.ManyToManyField(ImageCatalog)
    advanced = models.BooleanField(default=False)

    def __str__(self):
        return self.name



class Topic(models.Model):
    id = models.AutoField(primary_key=True)
    chapterid = models.ForeignKey(Chapter, models.DO_NOTHING, db_column='ChapterId')
    name = models.TextField(blank=True, null=True)
    timelimit = models.DurationField()

    def __str__(self):
        return self.name


class TopicRule(models.Model):
    id = models.AutoField(primary_key=True)
    topicid = models.ForeignKey(Topic, models.DO_NOTHING)
    questiontypeid = models.ForeignKey(QuestionType, models.DO_NOTHING,
                                       )
    questionthemeid = models.ForeignKey(QuestionTheme, models.DO_NOTHING,
                                        )
    questionscount = models.IntegerField()



