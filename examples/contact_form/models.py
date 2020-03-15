from django.db import models


class ContactSubmission(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
