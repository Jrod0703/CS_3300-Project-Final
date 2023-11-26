from django.contrib import admin
from .models import Golfer, Notebook, GolfRound

class GolfRoundInline(admin.TabularInline):
    model = GolfRound
    extra = 1

class NotebookAdmin(admin.ModelAdmin):
    inlines = [GolfRoundInline]
    list_display = ('golfer', 'average_score')
    list_filter = ['golfer']
    # searches now by the User model's username field
    search_fields = ['golfer__user__username']  

class GolferAdmin(admin.ModelAdmin):
     # Changed 'name' to 'user_username'
    list_display = ('user_username', 'gender') 
    # Changed 'name' to 'user__username'
    search_fields = ['user__username']  
    list_filter = ['gender']

    def user_username(self, obj):
        return obj.user.username
    # Allows column order sorting
    user_username.admin_order_field = 'user__username'  
    #Renames the column head in admin list view
    user_username.short_description = 'Username'  


# registers the models with their respective admin views.
admin.site.register(Golfer, GolferAdmin)
admin.site.register(Notebook, NotebookAdmin)
admin.site.register(GolfRound)

