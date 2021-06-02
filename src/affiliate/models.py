from django.contrib.auth.signals import user_logged_in
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.db.models.signals import post_save
from datetime import datetime, date, time, timedelta
from django.contrib.gis.geoip2 import GeoIP2
from django.template.defaultfilters import slugify
from urllib.parse import urlencode
import random


def AIDGenerator():
	'''
	Creates a random AID reference number (6 int's)
	'''
	first = random.randint(1,9)
	first = str(first)
	n = 6
	nrs = [str(random.randrange(10)) for i in range(n-1)]
	for i in range(len(nrs)):
		first += str(nrs[i])
	return str(first)



class Label(models.Model):

	class Meta:
		verbose_name_plural = "Labels"
		ordering = ["-timestamp"]

	timestamp = models.DateTimeField(blank=True, null=True)
	updated = models.DateTimeField(blank=True, null=True)

	name = models.CharField(verbose_name="Label name", max_length=100)
	description = models.CharField(verbose_name="Label description", max_length=1000, blank=True, null=True)

	label = models.CharField(verbose_name="Label ID", max_length=6, unique=True, blank=True, null=True)

	def save(self, *args, **kwargs):
		'''
		Updates timestamp, updated & aid on creation. Updated updated on updated
		'''
		if not self.id:
			#save dates and aid on creation
			self.timestamp = timezone.now()
			self.updated = timezone.now()
			self.label = AIDGenerator()
		else:
			#save update on update
			self.updated = timezone.now()
		super(Label, self).save(*args, **kwargs)

	is_active = models.BooleanField(default=True)

	def __str__(self):
		return f'{self.label}'



class Affiliate(models.Model):

	class Meta:
		verbose_name_plural = "Affiliates"
		ordering = ["-timestamp"]

	timestamp = models.DateTimeField(blank=True, null=True)
	updated = models.DateTimeField(blank=True, null=True)

	name = models.CharField(verbose_name="Affiliate name", max_length=100)
	description = models.CharField(verbose_name="Affiliate description", max_length=1000, blank=True, null=True)
	
	aid = models.CharField(verbose_name="Affiliate ID", max_length=6, unique=True, blank=True, null=True)
	label = models.ManyToManyField(Label, blank=True)

	is_active = models.BooleanField(default=True)

	@property
	def get_params(self):
		'''
		create a dict of all query strings
		'''
		params = {}
		for l in self.labels.all():
			p = {
				'aid': self.aid,
				'label': l.label
			}
			query_string = urlencode(params)
			params[str(l.id)] = "?" + query_string
		return params

	def save(self, *args, **kwargs):
		'''
		Updates timestamp, updated & aid on creation. Updated updated on updated
		'''
		if not self.id:
			#save dates and aid on creation
			self.timestamp = timezone.now()
			self.updated = timezone.now()
			self.aid = AIDGenerator()
		else:
			#save update on update
			self.updated = timezone.now()
		super(Affiliate, self).save(*args, **kwargs)

	def __str__(self):
		return f'{self.aid}'



class AffiliateTracker(models.Model):

	class Meta:
		verbose_name_plural = "Affiliate Tracker"
		ordering = ["-timestamp"]

	timestamp = models.DateTimeField()
	updated = models.DateTimeField()

	session_key = models.CharField(verbose_name="Session key", max_length=250, null=True, blank=True)
	affiliate = models.ForeignKey(Affiliate, related_name="affiliate_fk", on_delete=models.SET_NULL, null=True)
	label = models.ForeignKey(Label, related_name="label_fk", on_delete=models.SET_NULL, null=True)
	user = models.ForeignKey(User, related_name="user_fk",  on_delete=models.SET_NULL, null=True)

	log_in_count = models.IntegerField(default = 0)

	ip_address = models.CharField(max_length=250, null=True, blank=True)
	user_agent = models.CharField(max_length=1000, null=True, blank=True)
	device = models.CharField(max_length=200, null=True, blank=True, default = "")

	@property	
	def Location(self):
		try:
			g = GeoIP2()
			country = g.country(self.ip_address)["country_name"]
			city = g.city(self.ip_address)["city"]

			addy = f'{country}, {city}'
		except:
			addy = ""

		return addy

	is_active = models.BooleanField(default=True)


	def save(self, *args, **kwargs):
		'''
		Updates timestamp, updated & aid on creation. Updated updated on updated
		'''
		if not self.id:
			#save dates and aid on creation
			self.timestamp = timezone.now()
			self.updated = timezone.now()
		else:
			#save update on update
			self.updated = timezone.now()
		super(AffiliateTracker, self).save(*args, **kwargs)

	def __str__(self):
		return f'{self.user}'



def log_in_handler(sender, request, user, **kwargs):
	
	try:
		at = AffiliateTracker.objects.get(user = user)
		count = at.log_in_count + 1
		at.log_in_count = count
		at.save()

	except AffiliateTracker.DoesNotExist:
		pass

user_logged_in.connect(log_in_handler)