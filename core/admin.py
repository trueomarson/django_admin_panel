from django import forms

from django.contrib import admin
from django.db.models import Avg
from django.utils.html import format_html
from django.urls import reverse
from django.utils.http import urlencode

from core.models import Person, Course, Grade


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "show_average")

    def show_average(self, obj):
        from django.db.models import Avg 
        from django.utlis import format_html

    def show_average(self, obj):
        result = Grade.objects.filter(person=obj).aggregate(Avg("grade"))
        return format_html("<b><i>{}</i></b>", result["grade__avg"])
        return result["grade__avg"]

    show_average.short_description = "Average Grade"

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "year", "view_student_link")
    list_filter = ("year", )

    def view_student_link(self, obj):
        count = obj.person_set.count()
        url = (
            reverse("admin:core_person_changelist")
            + "?"
            + urlencode({"course_id": f"{obj.id}"})
        )
        return format_html('<a href="{}">{} Students</a>', url, count)

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_filter = ("course__year", )