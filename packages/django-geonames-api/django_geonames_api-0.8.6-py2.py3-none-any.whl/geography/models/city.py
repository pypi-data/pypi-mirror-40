# Django imports
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.gis.geos import Point

# ElasticSearch imports
from haystack.query import SearchQuerySet


class City(models.Model):

    name = models.CharField(_('Place name'), max_length=180, db_index=True)
    shortname = models.CharField(_('Shortname'), max_length=180, null=True)
    code = models.CharField(_('Postal code'), max_length=20, db_index=True)
    latitude = models.FloatField(_('Latitude'), db_index=True)
    longitude = models.FloatField(_('Longitude'), db_index=True)
    precision = models.IntegerField(
        _('Precision'),
        blank=True,
        null=True
    )
    country = models.ForeignKey('geography.Country', on_delete=models.PROTECT)
    region = models.ForeignKey(
        'geography.Region',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name=_('state')
    )
    department = models.ForeignKey(
        'geography.Department',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name=_('department')
    )
    conurbation = models.ForeignKey(
        'geography.Conurbation',
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        verbose_name=_('conurbation')
    )
    timezone = models.ForeignKey(
        'geography.Timezone',
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        verbose_name=_('timezone')
    )

    def get_name_length(self):
        return len(self.name)

    def shortname_or_name(self):
        return self.shortname if self.shortname else self.name

    def get_location(self):
        r"""" City location returned as a point (used by the search_indexes)
        """

        if self.latitude and self.longitude:
            return Point(self.longitude, self.latitude)
        return None

    def __str__(self):
        return "%s (%s)" % (self.name, self.code)

    @classmethod
    def nearest(cls, latitude, longitude):
        r""" Find in the database the city the nearest to the given latitude
        and longitude
        """

        point = Point(longitude, latitude)
        sqs = (
            SearchQuerySet()
            .models(City)
            .distance('location_city', point)
            .order_by('distance')
        )

        # If no city found in the coordinate plus delta degrees around
        # raise exception
        if not len(sqs):
            raise cls.DoesNotExist

        return sqs[0].object

    class Meta:
        verbose_name = _("city")
        verbose_name_plural = _("cities")
