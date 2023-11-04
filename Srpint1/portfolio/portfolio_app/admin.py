from django.contrib import admin
from .models import Golfer, Notebook, GolfRound

class GolfRoundInline(admin.TabularInline):
    model = GolfRound
    extra = 1  # This will provide 1 extra blank form for adding new GolfRound entries directly from a Notebook.

class NotebookAdmin(admin.ModelAdmin):
    inlines = [GolfRoundInline]
    list_display = ('golfer', 'average_score')  # Display the golfer and their average score in the admin list view.
    list_filter = ['golfer']  # Allow filtering notebooks by golfer.
    search_fields = ['golfer__name']  # Allow searching notebooks by golfer name.

class GolferAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'gender')
    search_fields = ['name', 'email']
    list_filter = ['gender']

# Register the models with their respective admin views.
admin.site.register(Golfer, GolferAdmin)
admin.site.register(Notebook, NotebookAdmin)
admin.site.register(GolfRound)  # Using default admin view for GolfRound since it's simple.