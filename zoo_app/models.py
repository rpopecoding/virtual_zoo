from django.db import models
import re	# the regex module
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your models here.

class Aniclass(models.Model):
    name = models.CharField(max_length=40)
    desc = models.CharField(max_length=500)
    img = models.ImageField(upload_to ='images/')


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
#    objects = UserManager()
    def __str__(self):
        return f"{self.name}"

class Family(models.Model):
    name = models.CharField(max_length=40)
    aniclass = models.ForeignKey(Aniclass, related_name="families", on_delete = models.CASCADE)
    desc = models.CharField(max_length=500)
    img = models.ImageField(upload_to ='images/')


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
#    objects = UserManager()
    def __str__(self):
        return f"{self.name}"

class Animal(models.Model):
    name = models.CharField(max_length=40)
    family = models.ForeignKey(Family, related_name="animals", on_delete = models.CASCADE)
    aniclass = models.ForeignKey(Aniclass, related_name="animals", on_delete = models.CASCADE)
    desc = models.CharField(max_length=500)
    face_img = models.ImageField(upload_to ='images/')
    wide_img = models.ImageField(upload_to ='images/')


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
#    objects = UserManager()
    def __str__(self):
        return f"{self.name}"






class Biome(models.Model):
    name = models.CharField(max_length=40)
    animals = models.ManyToManyField(Animal, related_name="biome")
    desc = models.TextField(max_length=500)
    img = models.ImageField(upload_to ='images/')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
#    objects = UserManager()
    def __str__(self):
        return f"{self.name}"



    
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        users = self.filter(email=postData['email'])
        handle = self.filter(handle=postData['handle'])
        if users:
            errors["email"] = "Email already in use"
        if handle:
            errors["handle"] = "Handle already in use"
        if postData['pwd'] != postData['confirm']:
            errors["password"] = "Passwords do not match"
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name must be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name must be at least 2 characters"
        if len(postData['handle']) < 2:
            errors["handle"] = "Handle must be at least 2 characters"
        

        if not EMAIL_REGEX.match(postData['email']): 
            errors['email'] = "Invalid email address!"
        
        return errors
    def authenticate(self, email, password):
        users = self.filter(email=email)
        if not users:
            return False
        user = users[0]
        return bcrypt.checkpw(password.encode(), user.pwdhash.encode())

    def update_validator(self, first_name, last_name, old_handle, new_handle, old_email, new_email):
        errors = {}
        if old_handle != new_handle:
            handle_check = self.filter(handle= new_handle)
        else:
            handle_check = {}
        if old_email != new_email:
            email_check = self.filter(email= new_email)
        else:
            email_check = {}
        
        
        if email_check:
            errors["email"] = "New email already in use"
        if handle_check:
            errors["handle"] = "New handle already in use"
        if len(first_name) < 2:
            errors["first_name"] = "First name must be at least 2 characters"
        if len(last_name) < 2:
            errors["last_name"] = "Last name must be at least 2 characters"
        if len(new_handle) < 2:
            errors["handle"] = "Handle must be at least 2 characters"
        

        if not EMAIL_REGEX.match(new_email): 
            errors['email'] = "Invalid email address!"
        
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    handle = models.CharField(max_length=40)
    email = models.CharField(max_length=255)
    pwdhash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    def __str__(self):
        return f"{self.first_name}"

class Edit(models.Model):
    text = models.TextField(max_length=50)
    editor = models.ForeignKey(User, related_name="edits", on_delete = models.CASCADE)
    bedit = models.ForeignKey(Biome, related_name="edits", null=True, on_delete = models.CASCADE)
    cedit = models.ForeignKey(Aniclass, related_name="edits", null=True, on_delete = models.CASCADE)
    fedit = models.ForeignKey(Family, related_name="edits", null=True, on_delete = models.CASCADE)
    aedit = models.ForeignKey(Animal, related_name="edits", null=True, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Edit: {self.editor} {self.created_at}"

class Comment(models.Model):
    text = models.TextField(max_length=50)
    commentor = models.ForeignKey(User, related_name="comments", on_delete = models.CASCADE)
    bcomment = models.ForeignKey(Biome, related_name="comments", null=True, on_delete = models.CASCADE)
    ccomment = models.ForeignKey(Aniclass, related_name="comments", null=True, on_delete = models.CASCADE)
    fcomment = models.ForeignKey(Family, related_name="comments", null=True, on_delete = models.CASCADE)
    acomment = models.ForeignKey(Animal, related_name="comments", null=True, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Comment: {self.commentor} {self.created_at}"