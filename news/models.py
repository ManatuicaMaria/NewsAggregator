from django.db import models

# Create your models here.

class Feed(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField(unique=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Article(models.Model):
    feed = models.ForeignKey(Feed)
    title = models.CharField(max_length=200)
    url = models.URLField(unique=True)
    description = models.TextField()
    publication_date = models.DateTimeField()
    full_text = models.TextField()
    real_degree = models.IntegerField(default=97)
    fake_or_real_tf_idf = models.CharField(default="REAL", max_length=10)
    fake_or_real_word_count = models.CharField(default="REAL", max_length=10)


    def __str__(self):
        return self.title
