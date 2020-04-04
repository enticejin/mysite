from django.contrib import admin
from .models import Question, Choice


# 添加选项
class ChoiceInline(admin.StackedInline):
    # Choice对象将在Question管理页面进行编辑
    model = Choice
    # 提供3个Choice对象
    extra = 3


# 自定义后台表单
class QuestionAdmin(admin.ModelAdmin):
    # fields = ['pub_date', 'question_text']
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date_information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    #展示内容
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    #过滤指定内容
    list_filter = ['pub_date']
    #搜索内容
    search_fields = ['question_text']

admin.site.register(Question, QuestionAdmin)
# admin.site.register(Choice)
# Register your models here.
