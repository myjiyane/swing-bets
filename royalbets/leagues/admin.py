# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import League, Team, UserPreferences, Subscriber, SubscriptionPlan, UserPlan, Match, AvailableMarkets, MatchSets

# Register your models here.
admin.site.register(League)
admin.site.register(Team)
admin.site.register(Subscriber)
admin.site.register(UserPreferences)
admin.site.register(SubscriptionPlan)
admin.site.register(UserPlan)
admin.site.register(Match)
admin.site.register(AvailableMarkets)
admin.site.register(MatchSets)
