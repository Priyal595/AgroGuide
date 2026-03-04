from django.contrib import admin
from .models import VoiceQuery


@admin.register(VoiceQuery)
class VoiceQueryAdmin(admin.ModelAdmin):
    list_display  = ('user', 'query_type', 'language', 'timestamp', 'short_query')
    list_filter   = ('query_type', 'language')
    search_fields = ('user__username', 'query')
    readonly_fields = ('timestamp',)

    def short_query(self, obj):
        return obj.query[:60]
    short_query.short_description = 'Query'
