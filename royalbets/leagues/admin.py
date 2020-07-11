# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import League, Team, Subscriber, SubscriptionPlan, UserPlan, Match, AvailableMarket, MatchSet, Country

# Register your models here.
admin.site.register(League)
admin.site.register(Team)
admin.site.register(Subscriber)
#admin.site.register(UserPreference)
admin.site.register(SubscriptionPlan)
admin.site.register(UserPlan)
admin.site.register(Match)
admin.site.register(AvailableMarket)
admin.site.register(MatchSet)
admin.site.register(Country)
