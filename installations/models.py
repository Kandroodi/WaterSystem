from django.db import models
from partial_date import PartialDateField
# from django.contrib.gis.db import models as gismodels
from django.contrib.auth.models import User

# Notes
# 1) you can add help text for each field using :e.g. help_text='City name!'.
# 2) on_delete= models.CASCADE: When the referenced object is deleted, also delete the objects that have references
#    to it. (When you remove a Country for instance, you might want to delete Cities as well).

# Create your models here.

# User model
class UserProfileInfo(models.Model):

    # Create relationship (don't inherit from User!)
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)

    # Add any additional attributes you want
    # portfolio_site = models.URLField(blank=True)
    # pip install pillow to use this!
    # Optional: pip install pillow --global-option=”build_ext” --global-option=”--disable-jpeg”
    profile_pic = models.ImageField(upload_to='profile_pics',blank=True)

    def __str__(self):
        # Built-in attribute of django.contrib.auth.models.User!
        return self.user.username


# class Station(gismodels.Model):
#     name = models.CharField(max_length=256)
#     geom = gismodels.PointField()
#
#     def __unicode__(self):
#         return self.name


class City(models.Model):
    name = models.CharField(max_length=100, blank=False)
    latitude = models.DecimalField(max_digits=7, decimal_places=5, default=0)
    longitude = models.DecimalField(max_digits=7, decimal_places=5, default=0)

    def __str__(self):
        return self.name


class CityEra(models.Model):
    name = models.CharField(max_length=100, blank=False)
    city = models.ForeignKey(City, on_delete=models.CASCADE, blank=True)
    start_date = PartialDateField()
    end_date = PartialDateField()
    population = models.IntegerField()

    def __str__(self):
        return self.name


class Citymap(models.Model):
    # map = models.ImageField()
    type = models.CharField(max_length=50, blank=False)
    city = models.ForeignKey(City, related_name='citymaps', on_delete=models.CASCADE, blank=True)
    population = models.IntegerField()
    start_date = PartialDateField()
    end_date = PartialDateField()


class Religion(models.Model):
    name = models.CharField(max_length=100, blank=False)
    description = models.TextField()

    def __str__(self):
        return self.name


class Bibliography(models.Model):
    title = models.CharField(max_length=250, blank=False)
    author = models.CharField(max_length=50, blank=False)
    journal = models.CharField(max_length=50)
    publisher = models.CharField(max_length=50)
    year = PartialDateField(default=None)

    def __str__(self):
        return self.title


class SourceType(models.Model):
    name = models.CharField(max_length=50, blank=False)
    description = models.CharField(max_length=500, blank=False)

    def __str__(self):
        return self.name


class TextualEvidence(models.Model):
    source_type = models.ForeignKey(SourceType, on_delete=models.CASCADE)
    title = models.CharField(max_length=250, blank=False)
    author = models.CharField(max_length=50, blank=False)
    date = PartialDateField()
    description = models.TextField(max_length=1000, blank=True)
    bibliography = models.ForeignKey(Bibliography, on_delete=models.CASCADE, blank=False, default='')

    def __str__(self):
        return self.title


class MaterialEvidence(models.Model):
    source_type = models.ForeignKey(SourceType, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, blank=False)
    author = models.CharField(max_length=50, blank=False)
    date = PartialDateField()
    # picture = models.ImageField()
    description = models.TextField(max_length=1000, blank=True)
    bibliography = models.ForeignKey(Bibliography, on_delete=models.CASCADE, blank=False)

    def __str__(self):
        return self.name


class Person(models.Model):
    name = models.CharField(max_length=50, blank=False)
    GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    gender = models.CharField(max_length=1, choices=GENDER, default='M')
    birth = PartialDateField()
    death = PartialDateField()
    role = models.CharField(max_length=100, blank=True)  # I think it's not necessary
    religion = models.ForeignKey(Religion, on_delete=models.CASCADE, blank=True)
    bibliography = models.ForeignKey(Bibliography, on_delete=models.CASCADE, default='')
    textual_evidence = models.ForeignKey(TextualEvidence, on_delete=models.CASCADE)
    material_evidence = models.ForeignKey(MaterialEvidence, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Watersystem(models.Model):
    name = models.CharField(max_length=100, blank=False)
    type = models.CharField(max_length=100, blank=True)
    inventor = models.ForeignKey(Person, on_delete=models.CASCADE, blank=True)
    description = models.TextField(max_length=1000, blank=True)
    bibliography = models.ForeignKey(Bibliography, on_delete=models.CASCADE, blank=False, default='')

    def __str__(self):
        return self.name


class Installation(models.Model):
    watersystem = models.ForeignKey(Watersystem, on_delete=models.CASCADE, blank=False)
    construction_date = PartialDateField()
    characteristic = models.CharField(max_length=50)  # space holder, ...  will be defined
    functioning_region = models.CharField(max_length=50)  # space holder, ... will be defined
    start_functioning_year = PartialDateField()
    end_functioning_year = PartialDateField()
    bibliography = models.ForeignKey(Bibliography, on_delete=models.CASCADE, default='')
    textual_evidence = models.ForeignKey(TextualEvidence, on_delete=models.CASCADE)
    material_evidence = models.ForeignKey(MaterialEvidence, on_delete=models.CASCADE)

    def __str__(self):
        return self.watersystem.name


class Purpose(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000, blank=True)

    def __str__(self):
        return self.name


class InstitutionnType(models.Model):
    name = models.CharField(max_length=100, blank=False)
    description = models.TextField(max_length=1000, blank=True)

    def __str__(self):
        return self.name


class Institution(models.Model):
    name = models.CharField(max_length=100, blank=False)
    type = models.ForeignKey(InstitutionnType, on_delete=models.CASCADE, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, blank=True)
    policy = models.CharField(max_length=100, blank=True)
    start_date = models.CharField(max_length=50, blank=True, )  # this field is for test and explaine the partitial dat
    ''''help_text="Date formats:"
                                                                       "Day: yyyy-mm-dd 1999-12-04  "
                                                                       "Month: yyyy-mm 1999-12  "
                                                                       "Year: <integer>y 1999y  "
                                                                       "Decade: <integer>d 200d 1990-2000  "
                                                                       "Century: <integer>c 20c 1900-2000  "
                                                                       "Millennium: <integer>m 2m 1000-2000  "'''
    # start_date = ... will be the partitial dat
    end_date = PartialDateField()
    religion = models.ForeignKey(Religion, on_delete=models.CASCADE, blank=True)
    bibliography = models.ForeignKey(Bibliography, on_delete=models.CASCADE, blank=False)
    textual_evidence = models.ForeignKey(TextualEvidence, on_delete=models.CASCADE, blank=False)
    material_evidence = models.ForeignKey(MaterialEvidence, on_delete=models.CASCADE, blank=False)

    def __str__(self):
        return self.name


# Relations
class CityPersonRelation(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, blank=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, blank=True)
    role = models.CharField(max_length=100, blank=False)


class PersonInstitutionRelation(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, blank=False)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, blank=True, default='')
    role = models.CharField(max_length=50, blank=False)
    start_date = PartialDateField()
    end_date = PartialDateField()


class PersonInstallationRelation(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, blank=False)
    installation = models.ForeignKey(Installation, on_delete=models.CASCADE, blank=False, default='')
    role = models.CharField(max_length=100, blank=False)


class CityInistallationRelation(models.Model):
    installation = models.ForeignKey(Installation, on_delete=models.CASCADE, blank=False)
    city = models.ForeignKey(City, on_delete=models.CASCADE, blank=True)
    capacity_absolute = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    capacity_percentage = models.DecimalField(max_digits=7, decimal_places=2, default=0)


class InstallationPurposeRelation(models.Model):
    installation = models.ForeignKey(Installation, on_delete=models.CASCADE, blank=False)
    purpose = models.ForeignKey(Purpose, on_delete=models.CASCADE, blank=True)
    percentage = models.DecimalField(max_digits=7, decimal_places=2)


class InstitutionInstallationRelation(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, blank=True, default='')
    installation = models.ForeignKey(Installation, on_delete=models.CASCADE, blank=False)
    role = models.CharField(max_length=100, blank=False)


class TextPersonRelation(models.Model):
    textual_evidence = models.ForeignKey(TextualEvidence, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, blank=False)
    page_number = models.CharField(max_length=100,
                                   blank=False)  # I think maybe it's better if we had letter as page numbers also
    description = models.TextField(max_length=1000, blank=True, default=0)


class TextInstitutionRelation(models.Model):
    textual_evidence = models.ForeignKey(TextualEvidence, on_delete=models.CASCADE)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, blank=True, default='')
    page_number = models.CharField(max_length=100,
                                   blank=False)  # I think maybe it's better if we had letter as page numbers also
    description = models.TextField(max_length=1000, blank=True)


class TextInstallationRelation(models.Model):
    textual_evidence = models.ForeignKey(TextualEvidence, on_delete=models.CASCADE)
    installation = models.ForeignKey(Installation, on_delete=models.CASCADE, blank=False, default='')
    page_number = models.CharField(max_length=100,
                                   blank=False)  # I think maybe it's better if we had letter as page numbers also
    description = models.TextField(max_length=1000, blank=True)


class MaterialInstallationRelation(models.Model):
    material_evidence = models.ForeignKey(MaterialEvidence, on_delete=models.CASCADE)
    installation = models.ForeignKey(Installation, on_delete=models.CASCADE, blank=False, default='')
    page_number = models.CharField(max_length=100,
                                   blank=False)  # I think maybe it's better if we had letter as page numbers also
    description = models.TextField(max_length=1000, blank=True)
