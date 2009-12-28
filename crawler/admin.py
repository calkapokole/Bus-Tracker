from django.contrib import admin
from bus_tracker.crawler.models import *

class DirectionInline(admin.TabularInline):
    model = Direction
    extra = 1

class TimetableInline(admin.TabularInline):
    model = Timetable
    extra = 1

class DayInline(admin.TabularInline):
    model = Day
    extra = 1

class TimeInline(admin.TabularInline):
    model = Time
    extra = 3

class CrawlerModelAdmin(admin.ModelAdmin):
    pass

class BusStopAdmin(admin.ModelAdmin):
    inlines = [TimetableInline, ]

class LineAdmin(admin.ModelAdmin):
    inlines = [TimetableInline, DirectionInline]

class DirectionAdmin(admin.ModelAdmin):
    inlines = [TimetableInline, ]

class TimetableAdmin(admin.ModelAdmin):
    inlines = [DayInline, ]

class DayAdmin(admin.ModelAdmin):
    inlines = [TimeInline, ]

class TimeAdmin(admin.ModelAdmin):
    pass

admin.site.register(CrawlerModel, CrawlerModelAdmin)
admin.site.register(BusStop, BusStopAdmin)
admin.site.register(Line, LineAdmin)
admin.site.register(Direction, DirectionAdmin)
admin.site.register(Timetable, TimetableAdmin)
admin.site.register(Day, DayAdmin)
admin.site.register(Time, TimeAdmin)
