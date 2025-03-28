from django.db import models

# Create your models here.

class Organ(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='organs/', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Doctor(models.Model):
    name = models.CharField(max_length=200)
    specialization = models.ForeignKey(Organ, on_delete=models.CASCADE, related_name='doctors')
    clinic_address = models.TextField()
    photo = models.ImageField(upload_to='doctors/')
    experience = models.IntegerField(help_text="Years of experience")
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Dr. {self.name} - {self.specialization.name}"

    class Meta:
        ordering = ['name']
