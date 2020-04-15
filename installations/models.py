from django.db import models

# Notes
# 1) you can add help text for each field using :e.g. help_text='City name!'.


# Create your models here.

class Country(models.Model):
    name = models.CharField(max_length=50, blank=False)
    # map = ... Will be defined

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=100, blank=False)
    country = models.ForeignKey(Country, on_delete= models.CASCADE, blank=True)
    latitude = models.DecimalField(max_digits=7, decimal_places=5, default=0)
    longitude = models.DecimalField(max_digits=7, decimal_places=5, default=0)

    def __str__(self):
        return self.name

''' on_delete= models.CASCADE: When the referenced object is deleted,
    also delete the objects that have references to it
    (When you remove a Country for instance, you might want to delete Cities as well).'''

class Citymap(models.Model):
    # map = ... will be defined
    type = models.CharField(max_length=50, blank=False)
    city = models.ForeignKey(City, related_name='citymaps', on_delete=models.CASCADE, blank=True)
    population = models.IntegerField()
    # start_date = ... will be the partitial date
    # end_date = ... will be the partitial date

class Politicalorientation(models.Model):
    name = models.CharField(max_length=100, blank=False)
    description = models.TextField()

    def __str__(self):
        return self.name

class Religiousorientation(models.Model):
    name = models.CharField(max_length=100, blank=False)
    description = models.TextField()

    def __str__(self):
        return self.name

class Person(models.Model):
    last_name = models.CharField(max_length=50, blank=False)
    first_name = models.CharField(max_length=50, blank=True)
    nationality = models.ForeignKey(Country, on_delete=models.CASCADE, blank=True)
    # gender = models.IntegerField(choices=GENDER_CHOICES, default=2) # find a way for choice!
    # birth = ... will be the partitial dat
    # death = ... will be the partitial dat
    profession = models.CharField(max_length=100, blank=True)
    political_orientation = models.ForeignKey(Politicalorientation, on_delete=models.CASCADE, blank=True)
    religious_orientation = models.ForeignKey(Religiousorientation, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return self.first_name +' '+ self.last_name

class CityPersonRelation(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, blank=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, blank=True)
    role = models.CharField(max_length=100, blank=False)

class Watersystem(models.Model):
    name = models.CharField(max_length=100, blank=False)
    type = models.CharField(max_length=100, blank=True)
    inventor = models.ForeignKey(Person, on_delete=models.CASCADE, blank=True)
    description = models.TextField(max_length=1000, blank=True)

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

class PersonInstallationRelation(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, blank=False)
    installation = models.ForeignKey(Installation, on_delete=models.CASCADE, blank=False)
    role = models.CharField(max_length=100, blank=False)

class CityInistallationRelation(models.Model):
    installation = models.ForeignKey(Installation, on_delete=models.CASCADE, blank=False)
    city = models.ForeignKey(City, on_delete=models.CASCADE, blank=True)
    capacity_absolute = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    capacity_percentage = models.DecimalField(max_digits=7, decimal_places=2, default=0)

class Organizationtype(models.Model):
    name = models.CharField(max_length=100, blank=False)
    description = models.TextField(max_length=1000, blank=True)

class Organization(models.Model):
    name = models.CharField(max_length=100, blank=False)
    type = models.ForeignKey(Organizationtype, on_delete=models.CASCADE, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, blank=True)
    policy = models.CharField(max_length=100, blank=True)
    start_date = models.CharField(max_length=50, blank=True, help_text="Date formats:"
                                                                       "Day: yyyy-mm-dd 1999-12-04  "
                                                                       "Month: yyyy-mm 1999-12  "
                                                                       "Year: <integer>y 1999y  "
                                                                       "Decade: <integer>d 200d 1990-2000  "
                                                                       "Century: <integer>c 20c 1900-2000  "
                                                                       "Millennium: <integer>m 2m 1000-2000  ") # this field is for test and explaine the partitial dat
    # start_date = ... will be the partitial dat
    # end_date = ... will be the partitial dat
    political_orientation = models.ForeignKey(Politicalorientation, on_delete=models.CASCADE, blank=True)
    religious_orientation = models.ForeignKey(Religiousorientation, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return self.name

class PersonOrganizationRelation(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, blank=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, blank=True)
    role = models.CharField(max_length=50, blank=False)
