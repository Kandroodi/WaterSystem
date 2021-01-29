from django.db import models
from partial_date import PartialDateField
from django.urls import reverse
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
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)

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
    population = models.IntegerField()  # I think we do nat need population here, as we have it in CityEra
    start_date = PartialDateField()
    end_date = PartialDateField()


class Neighbourhood(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, blank=True, null=True)
    neighbourhood_number = models.PositiveIntegerField(null=True, blank=True)
    extent_shapefile = models.FileField(upload_to='shapefiles/', null=True, blank=True)  # Is it correct way?

    def __str__(self):
        st = self.city.name + ' ' + str(self.neighbourhood_number)
        return st


class Location(models.Model):
    ''''The location used for exact location'''
    gpsargs = {'blank': True, 'null': True, 'max_digits': 8, 'decimal_places': 5}
    latitude = models.DecimalField(**gpsargs)
    longitude = models.DecimalField(**gpsargs)

    def __str__(self):
        st = str(self.latitude) + '  ' + str(self.longitude)
        return st


class Religion(models.Model):
    name = models.CharField(max_length=100, blank=False)
    description = models.TextField(blank=True, default='', null=True)

    def __str__(self):
        return self.name


class SecondaryLiterature(models.Model):
    title = models.CharField(max_length=250, blank=False, default='', null=True)
    author = models.CharField(max_length=100, blank=False, default='', null=True)
    editor = models.CharField(max_length=100, blank=True, default='', null=True)
    book_title = models.CharField(max_length=250, blank=True, default='', null=True)
    journal = models.CharField(max_length=100, blank=True, default='', null=True)
    publisher = models.CharField(max_length=100, blank=True, default='', null=True)
    volume = models.CharField(max_length=25, blank=True, default='', null=True)
    issue = models.CharField(max_length=25, blank=True, default='', null=True)
    page_number = models.CharField(max_length=25, blank=True, default='', null=True)
    place = models.CharField(max_length=25, blank=True, default='', null=True)
    year = PartialDateField(blank=True, null=True, default='')

    def __str__(self):
        return 'Author: ' + self.author + ' | Title: ' + self.title


class Evidence(models.Model):
    title = models.CharField(max_length=250, blank=False)
    author = models.CharField(max_length=50, blank=True, null=True)
    date = PartialDateField(blank=True, null=True)
    secondary_literature = models.ForeignKey(SecondaryLiterature, on_delete=models.CASCADE, blank=True, default='',
                                             null=True)
    description = models.TextField(max_length=1000, blank=True, default='', null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("installations:home", kwargs={'pk': self.pk})


class Person(models.Model):
    name = models.CharField(max_length=50, blank=False)
    GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    gender = models.CharField(max_length=1, choices=GENDER, default='M')
    birth = PartialDateField(blank=True, default='', null=True)
    death = PartialDateField(blank=True, default='', null=True)
    role = models.CharField(max_length=100,
                            blank=True)  # Role field for person and type of envolvement feild for person-installation relation
    religion = models.ForeignKey(Religion, on_delete=models.CASCADE, blank=True, default='', null=True)
    secondary_literature = models.ManyToManyField(SecondaryLiterature, blank=True)
    evidence = models.ForeignKey(Evidence, on_delete=models.CASCADE, blank=True, default='', null=True)
    comment = models.TextField(max_length=1000, blank=True, default='', null=True)

    def __str__(self):
        return self.name


class Watersystem(models.Model):
    original_term = models.CharField(max_length=100, blank=False)
    type = models.CharField(max_length=100, blank=True, null=True)
    inventor = models.ForeignKey(Person, on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField(max_length=1000, blank=True, null=True)
    secondary_literature = models.ForeignKey(SecondaryLiterature, on_delete=models.CASCADE, blank=True, default='',
                                             null=True)

    def __str__(self):
        return self.original_term


class Purpose(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000, blank=True)

    def __str__(self):
        return self.name


class Installation(models.Model):
    name = models.CharField(max_length=250, blank=True, default='')
    watersystem = models.ForeignKey(Watersystem, on_delete=models.CASCADE, blank=True, null=True)
    construction_date_lower = PartialDateField(blank=True, null=True)
    construction_date_upper = PartialDateField(blank=True, null=True)
    first_reference_lower = PartialDateField(blank=True, null=True)
    first_reference_upper = PartialDateField(blank=True, null=True)
    end_functioning_year_lower = PartialDateField(blank=True, null=True)
    end_functioning_year_upper = PartialDateField(blank=True, null=True)
    purpose = models.ManyToManyField(Purpose, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, blank=True, null=True)
    neighbourhood = models.ManyToManyField(Neighbourhood, blank=True)
    exact_location = models.ForeignKey(Location, on_delete=models.CASCADE, blank=True, null=True)
    secondary_literature = models.ManyToManyField(SecondaryLiterature, blank=True)
    evidence = models.ManyToManyField(Evidence, blank=True)
    comment = models.TextField(max_length=1000, blank=True, default='', null=True)

    def __str__(self):
        return self.name


class InstitutionType(models.Model):
    name = models.CharField(max_length=100, blank=False)
    description = models.TextField(max_length=1000, blank=True)

    def __str__(self):
        return self.name


class Institution(models.Model):
    name = models.CharField(max_length=100, blank=False)
    type = models.ForeignKey(InstitutionType, on_delete=models.CASCADE, blank=True, null=True)
    purpose = models.ManyToManyField(Purpose, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, blank=True, null=True)
    neighbourhood = models.ManyToManyField(Neighbourhood, blank=True)
    exact_location = models.ForeignKey(Location, on_delete=models.CASCADE, blank=True, null=True)
    policy = models.CharField(max_length=100, blank=True)
    start_date = PartialDateField(blank=True, null=True)  # this field is for test and explaine the partitial dat
    ''''help_text="Date formats:"
                                                                       "Day: yyyy-mm-dd 1999-12-04  "
                                                                       "Month: yyyy-mm 1999-12  "
                                                                       "Year: <integer>y 1999y  "
                                                                       "Decade: <integer>d 200d 1990-2000  "
                                                                       "Century: <integer>c 20c 1900-2000  "
                                                                       "Millennium: <integer>m 2m 1000-2000  "'''
    # start_date = ... will be the partitial dat
    end_date = PartialDateField(blank=True, null=True)
    religion = models.ForeignKey(Religion, on_delete=models.CASCADE, blank=True, null=True)
    secondary_literature = models.ManyToManyField(SecondaryLiterature, blank=True)
    evidence = models.ForeignKey(Evidence, on_delete=models.CASCADE, blank=False, default='', null=True)
    comment = models.TextField(max_length=1000, blank=True, default='', null=True)

    def __str__(self):
        return self.name


# Relations
class CityPersonRelation(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, blank=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, blank=True)
    type_of_involvement = models.CharField(max_length=100, blank=False)

    def __str__(self):
        message = "relation is " + self.type_of_involvement
        return message


class NeighbourhoodPersonRelation(models.Model):
    neighbourhood = models.ForeignKey(Neighbourhood, on_delete=models.CASCADE, blank=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, blank=True)
    type_of_involvement = models.CharField(max_length=100, blank=False)

    def __str__(self):
        # message = "neighbourhood: " + str(self.neighbourhood) + " & " + "person: " + str(self.person) + " relation is " + self.type_of_involvement
        message = "relation is " + self.type_of_involvement
        return message


class PersonInstitutionRelation(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, blank=False)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, blank=True, default='')
    type_of_involvement = models.CharField(max_length=50, blank=False)

    def __str__(self):
        message = "relation is " + self.type_of_involvement
        return message


class PersonInstallationRelation(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, blank=False)
    installation = models.ForeignKey(Installation, on_delete=models.CASCADE, blank=False, default='')
    type_of_involvement = models.CharField(max_length=100, blank=False)

    def __str__(self):
        message = "relation is " + self.type_of_involvement
        return message


class CityInstallationRelation(models.Model):
    installation = models.ForeignKey(Installation, on_delete=models.CASCADE, blank=False)
    city = models.ForeignKey(City, on_delete=models.CASCADE, blank=True)
    capacity_absolute = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    capacity_percentage = models.DecimalField(max_digits=7, decimal_places=2, default=0)


class InstitutionInstallationRelation(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, blank=True, default='')
    installation = models.ForeignKey(Installation, on_delete=models.CASCADE, blank=False)
    type_of_involvement = models.CharField(max_length=100, blank=False)

    def __str__(self):
        message = "relation is " + self.type_of_involvement
        return message


class EvidencePersonRelation(models.Model):
    evidence = models.ForeignKey(Evidence, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, blank=False)
    page_number = models.CharField(max_length=100,
                                   blank=False)  # I think maybe it's better if we had letter as page numbers also
    description = models.TextField(max_length=1000, blank=True, default=0)

    def __str__(self):
        message = "relation is " + self.page_number + " " + self.description
        return message


class EvidenceInstitutionRelation(models.Model):
    evidence = models.ForeignKey(Evidence, on_delete=models.CASCADE)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, blank=True, default='')
    page_number = models.CharField(max_length=100,
                                   blank=False)  # I think maybe it's better if we had letter as page numbers also
    description = models.TextField(max_length=1000, blank=True)

    def __str__(self):
        message = "relation is " + self.page_number + " " + self.description
        return message


class EvidenceInstallationRelation(models.Model):
    evidence = models.ForeignKey(Evidence, on_delete=models.CASCADE)
    installation = models.ForeignKey(Installation, on_delete=models.CASCADE, blank=False, default='')
    page_number = models.CharField(max_length=100,
                                   blank=False)  # I think maybe it's better if we had letter as page numbers also
    description = models.TextField(max_length=1000, blank=True)

    def __str__(self):
        message = "relation is " + self.page_number + " " + self.description
        return message
