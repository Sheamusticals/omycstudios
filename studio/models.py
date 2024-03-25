from django.db import models

# Create your models here.




class brand(models.Model):
    image = models.ImageField(blank=True,null=True)
    name = models.CharField(max_length = 50)


    def __str__(self):
        return self.name
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url =''
        return url





class service_type(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(blank=True,null=True)
    description = models.TextField(max_length=255,blank=True,null=True)

    def __str__(self):
        return self.name
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url =''
        return url

    class Meta:
        verbose_name_plural = "Service Type"

class service(models.Model):
    name = models.ForeignKey(service_type,on_delete = models.CASCADE)
    image = models.ImageField(blank=True,null=True)

    def __str__(self):
        return str(self.name.name)

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url =''
        return url

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phoneNumber = models.CharField(max_length=15)
    message = models.TextField()
    
    def __str__(self):
        return self.name
    
class Type(models.Model):
    name = models.CharField(max_length=255)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Blog Type"
    

class Blog(models.Model):
    type = models.ForeignKey(Type,on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField(max_length=10000)
    date = models.DateTimeField(blank=True,null=True)
    image = models.ImageField(blank=True,null=True)   
    author = models.CharField(max_length=50) 


    def __str__(self):
        return self.title
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url =''
        return url
    
    class Meta:
        ordering = ['date']
        verbose_name_plural = "Blogs"
    

class Tutorial(models.Model):
    title = models.CharField(max_length=255)
    upload = models.FileField(upload_to='files/')
    link = models.CharField(max_length = 255)
    date = models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return self.title
    
    @property
    def fileURL(self):
        try:
            url = self.upload.url
        except:
            url =''
        return url


    class Meta:
        ordering = ['date']

class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    commenter_name = models.CharField(max_length=100)
    commenter_email = models.EmailField(blank=True)
    comment = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.commenter_name} on {self.blog.title}"