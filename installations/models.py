from django.db import models

# Notes
# 1) you can add help text for each field using :e.g. help_text='City name!'.
# 2) on_delete= models.CASCADE: When the referenced object is deleted, also delete the objects that have references to it. (When you remove a Country for instance, you might want to delete Cities as well).'''

# Create your models here.

class City(models.Model):
    name = models.CharField(max_length=100, blank=False)
    latitude = models.DecimalField(max_digits=7, decimal_places=5, default=0)
    longitude = models.DecimalField(max_digits=7, decimal_places=5, default=0)

    def __str__(self):
        return self.name

class Citymap(models.Model):
    # map = ... will be defined
    type = models.CharField(max_length=50, blank=False)
    city = models.ForeignKey(City, related_name='citymaps', on_delete=models.CASCADE, blank=True)
    population = models.IntegerField()
    # start_date = ... will be the partitial date
    # end_date = ... will be the partitial date

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
    # year =  ... will be the partitial date

    def __str__(self):
        return self.title

class Person(models.Model):
    last_name = models.CharField(max_length=50, blank=False)
    first_name = models.CharField(max_length=50, blank=True)
    GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    gender = models.CharField(max_length=1, choices=GENDER, default='M')
    # birth = ... will be the partitial dat
    # death = ... will be the partitial dat
    profession = models.CharField(max_length=100, blank=True)
    religion = models.ForeignKey(Religion, on_delete=models.CASCADE, blank=True)
    bibliography = models.ForeignKey(Bibliography, on_delete=models.CASCADE, default='')

    def __str__(self):
        return self.first_name +' '+ self.last_name

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
    # construction_date = ... will be the partitial date
    # characteristic = ... will be defined
    # functioning_region =  ... will be defined
    # start_functioning_year =  .. will be the partitial date
    # end_functioning_year =  .. will be the partitial date

    def __str__(self):
        return self.watersystem.name

class TextualEvidence(models.Model):
    title = models.CharField(max_length=250, blank=False)
    author = models.CharField(max_length=50, blank=False)
    # date =  .. will be the partitial date
    description = models.TextField(max_length=1000, blank=True)
    bibliography = models.ForeignKey(Bibliography, on_delete=models.CASCADE, blank=False, default='')

    def __str__(self):
        return self.title

class MaterialEvidence(models.Model):
    title = models.CharField(max_length=250, blank=False)
    author = models.CharField(max_length=50, blank=False)
    # date =  .. will be the partitial date
    # picture = models.ImageField()
    bibliography = models.ForeignKey(Bibliography, on_delete=models.CASCADE, blank=False)

    def __str__(self):
        return self.title

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
    start_date = models.CharField(max_length=50, blank=True, ) # this field is for test and explaine the partitial dat
    ''''help_text="Date formats:"
                                                                       "Day: yyyy-mm-dd 1999-12-04  "
                                                                       "Month: yyyy-mm 1999-12  "
                                                                       "Year: <integer>y 1999y  "
                                                                       "Decade: <integer>d 200d 1990-2000  "
                                                                       "Century: <integer>c 20c 1900-2000  "
                                                                       "Millennium: <integer>m 2m 1000-2000  "'''
    # start_date = ... will be the partitial dat
    # end_date = ... will be the partitial dat
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

# class PersonInstitutionRelation(models.Model):
#     person = models.ForeignKey(Person, on_delete=models.CASCADE, blank=False)
#     institution = models.ForeignKey(Institution, on_delete=models.CASCADE, blank=True, default='')
#     role = models.CharField(max_length=50, blank=False)

# class PersonInstallationRelation(models.Model):
#     person = models.ForeignKey(Person, on_delete=models.CASCADE, blank=False)
#     installation = models.ForeignKey(Installation, on_delete=models.CASCADE, blank=False, default='')
#     role = models.CharField(max_length=100, blank=False)

class CityInistallationRelation(models.Model):
    installation = models.ForeignKey(Installation, on_delete=models.CASCADE, blank=False)
    city = models.ForeignKey(City, on_delete=models.CASCADE, blank=True)
    capacity_absolute = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    capacity_percentage = models.DecimalField(max_digits=7, decimal_places=2, default=0)