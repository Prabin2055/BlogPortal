from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now



class Category(models.Model):
     name = models.CharField(max_length=60)

     @staticmethod
     def get_all_categories():
          return Category.objects.all()


     def __str__(self):
          return self.name


class BlogPost(models.Model):
    sno=models.AutoField(primary_key=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE, default=1)
    title=models.CharField(max_length=255)
    author=models.CharField(max_length=14)
    slug=models.CharField(max_length=130)
    timeStamp=models.DateTimeField(blank=True)
    content=models.TextField()
    thumbnail = models.ImageField(upload_to='blog/images', default="")

    @staticmethod
    def get_post_by_id(ids):
        return BlogPost.objects.filter(id__in=ids)

    @staticmethod
    def get_all_post():
        return BlogPost.objects.all()

    @staticmethod
    def get_all_post_by_categoriesId(category_Id):
        if category_Id:
            return BlogPost.objects.filter(category=category_Id)
        else:
            return BlogPost.get_all_post()


    def __str__(self):
        return self.title + " by " + self.author

class BlogComment(models.Model):
    sno = models.AutoField(primary_key=True)
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return self.comment[0:13] + "..." + "by" + " " + self.user.username
