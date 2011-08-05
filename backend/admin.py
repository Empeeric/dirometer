from django.contrib.admin import ModelAdmin,site

class UserInfoAdmin(ModelAdmin):
    list_display = ('user','FB_ID')
