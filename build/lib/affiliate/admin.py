from django.contrib import admin
from . models import Label, AffiliateTracker, Affiliate

# Register your models here.

class LabelAdmin(admin.ModelAdmin):
	list_display = ('id', 'label', 'name')
	readonly_fields = ["timestamp", "updated", "label"]

class AffiliateAdmin(admin.ModelAdmin):
	list_display = ('id', 'aid', 'name')
	readonly_fields = ["timestamp", "updated", "aid"]


class AffiliateTrackerAdmin(admin.ModelAdmin):
	list_display = ('id', 'affiliate', 'label')
	readonly_fields = ["timestamp", "updated", "log_in_count", "ip_address", "user_agent", "device", "affiliate", "label", "user", "session_key"]


admin.site.register(Label, LabelAdmin)
admin.site.register(Affiliate, AffiliateAdmin)
admin.site.register(AffiliateTracker, AffiliateTrackerAdmin)
