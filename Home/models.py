from django.db import models

class Category(models.Model):
     name = models.CharField(max_length=60)

     @staticmethod
     def get_all_categories():
          return Category.objects.all()


     def __str__(self):
          return self.name

class Contact(models.Model):
     sno= models.AutoField(primary_key=True)
     name= models.CharField(max_length=255)
     phone= models.CharField(max_length=13)
     email= models.CharField(max_length=100)
     content= models.TextField()
     timeStamp=models.DateTimeField(auto_now_add=True, blank=True)

     def __str__(self):
         return "Message from " + self.name+"-"+ self.email

class FeaturePost(models.Model):
     sno = models.AutoField(primary_key=True)
     title = models.CharField(max_length=255)
     author = models.CharField(max_length=50)
     category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
     sub_category = models.CharField(max_length=300)
     caption = models.CharField(max_length=500)
     slug = models.CharField(max_length=130)
     timeStamp = models.DateTimeField(blank=True)
     content = models.TextField()
     thumbnail = models.ImageField(upload_to='blog/news', default="")

     @staticmethod
     def get_post_by_id(ids):
          return FeaturePost.objects.filter(id__in=ids)

     @staticmethod
     def get_all_post():
          return FeaturePost.objects.all()

     @staticmethod
     def get_all_post_by_catrgoriesid(category_id):

          if category_id:
               return FeaturePost.objects.filter(category=category_id)
          else:
               return FeaturePost.get_all_post()

     def __str__(self):
          return self.title