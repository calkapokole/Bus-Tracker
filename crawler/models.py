#!/usr/bin/python
# -*- coding: utf8 -*-

from django.db import models

class CrawlerModel(models.Model):

    def __unicode__(self):
        return Meta.verbose_name

    class Meta:
        verbose_name = 'ZTM crawler'
        verbose_name_plural = 'ZTM crawler'

class BusStop(models.Model):
    code = models.CharField('kod', max_length = 4)
    name = models.CharField('nazwa', max_length = 200, help_text = u'nazwa linii')

    def __unicode__(self):
        return '{0} {1}'.format(self.name, self.code)

    class Meta:
        verbose_name = 'przystanek'
        verbose_name_plural = 'przystanki'

class Line(models.Model):
    code = models.CharField('kod', max_length = 4)
    name = models.CharField('nazwa', max_length = 200, help_text = u'nazwa linii')

    def __unicode__(self):
        return '{0} {1}'.format(self.name, self.code)

    class Meta:
        verbose_name = 'linia'
        verbose_name_plural = 'linie'

class Direction(models.Model):
    code = models.CharField('kod', max_length = 4)
    name = models.CharField('nazwa', max_length = 200, help_text = u'nazwa kierunku')
    line = models.ForeignKey(Line, verbose_name = 'linia')

    def __unicode__(self):
        return '{0}'.format(self.name)

    class Meta:
        verbose_name = 'kierunek'
        verbose_name_plural = 'kierunki'

class Timetable(models.Model):
    code = models.CharField('kod', max_length = 4)
    name = models.CharField('nazwa', max_length = 200, help_text = u'nazwa przystanku')
    line = models.ForeignKey(Line)
    direction = models.ForeignKey(Direction)
    bus_stop = models.ForeignKey(BusStop)
    validity_text = models.CharField(u'ważność', max_length = 300)
    contact_text = models.CharField(u'kontakt', max_length = 300)
    emblems_text = models.TextField(u'symbole')

    def __unicode__(self):
        return '{0} {1} {2}'.format(self.name, self.direction, self.code)

    class Meta:
        verbose_name = 'rozkład'
        verbose_name_plural = 'rozkłady'

class Day(models.Model):
    DAY_CHOICES = (('weekday', u'dzień powszedni'),
                   ('saturday', u'sobota'),
                   ('sunday', u'niedziela'))
    day = models.CharField(u'dzień', max_length = 20, choices = DAY_CHOICES, unique = True)
    timetable = models.ForeignKey(Timetable)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'dzień'
        verbose_name_plural = 'dni'

class Time(models.Model):
    time = models.TimeField(u'czas')
    emblems = models.CharField(u'sybmole', max_length = 5)
    day = models.ForeignKey(Day)

    def __unicode__(self):
        return '{0} {1}'.format(self.time, self.emblems)

    class Meta:
        verbose_name = 'czas'
        verbose_name_plural = 'czasy'

