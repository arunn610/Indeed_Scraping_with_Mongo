from django.db import models

class Candidate(models.Model):
    Job_Title = models.CharField(max_length=255)
    Company = models.CharField(max_length=255)
    Location = models.CharField(max_length=255)
    Salary = models.CharField(max_length=255)
    employment_type = models.CharField(max_length=255)

    def __str__(self):
        return self.Job_Title
