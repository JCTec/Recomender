import uuid
from django.db import models


class Subject(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=200)


class Tag(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    subjects = models.ManyToManyField(Subject)
    name = models.CharField(max_length=200)


class Question(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    tag = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True, blank=True)
    value = models.CharField(max_length=500)


class History(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    value = models.CharField(max_length=1500)
    result = models.ForeignKey(Subject, on_delete=models.CASCADE)
