from djongo import models
from django.core.validators import FileExtensionValidator
from datetime import datetime
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


# def user_directory_path(instance,filename):
#    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Analysis(models.Model):
    fastq_files = models.FileField(upload_to='data/', blank=True, null=False,
                                   validators=[FileExtensionValidator(allowed_extensions=['gz','zip', '7z'])])
    mapping_file = models.FileField(upload_to='data/', validators=[FileExtensionValidator(allowed_extensions=['txt'])])
    sample_size = models.IntegerField(default=50000)
    min_otu_freq = models.FloatField(default=0.001)
    p_perc_identity = models.FloatField(default=0.97)
    dateDebut = models.DateField()
    dateFin = models.DateField()
    user = models.TextField()
    number = models.IntegerField()


class Profile(models.Model):
    user = models.TextField()
    nbr_of_analysis = models.IntegerField()

