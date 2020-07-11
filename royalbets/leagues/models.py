# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from django.utils import timezone

from django.contrib.postgres.fields import JSONField
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

CANCELLED = 'CANC'
PENDING = 'PEND'
POSTPONED = 'POST'
CORRECT = 'CORR'
INCORRECT = 'INCO'
NO_RESULTS = 'NRES'
ABANDONED = 'ABAN'
FREE = 'Free Plan'
BASIC = 'Basic Plan'
PROF = 'Professional Plan'
EXPERT = 'Expert Advisor'

MOBI = 'M'
DESKTOP = 'DESKTOP'
APP = 'APP'

WIN = '1'
DRAW = 'X'
AWAY = '2'
LOST = '0'

YES= 'Y'
NO = 'N'


# Create your models here.
class Country(models.Model):
    name = models.CharField(max_length=40, null=False, blank=False)
    iso = models.CharField(max_length=12, null=True, blank=True)
    federation_name = models.CharField(max_length=50, null=True, blank=True)
    
    class Meta:
        db_table = 'countries'
        ordering = ('name',)
    
    def __str__(self):
        return self.name
    
    
class League(models.Model):
    leag_id = models.BigAutoField(primary_key=True, editable=False)
    league_name = models.CharField(max_length=40, null=False, blank=False)
    league_cd = models.CharField(max_length=24, blank=False, default='')
    country = models.OneToOneField(Country, related_name = '+' ,null=True, blank=True, on_delete=models.CASCADE)
    league_api_id = models.PositiveIntegerField(null=True, unique=True)
    league_type = models.CharField(max_length=12, null=True)
    logo_path = models.CharField(max_length=70, null=True)
    is_cup = models.BooleanField(null=False, default=False)
    last_updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'leagues'
        ordering = ('league_name',)
      
    def __str__(self):
      	return "%s - %s" % (self.league_name, self.country)


class Team(models.Model):
    team_id = models.BigAutoField(primary_key=True, editable=False)    
    name = models.CharField(max_length=32)
    team_cd = models.CharField(max_length=8, null=False)    
    league = models.ForeignKey(League, related_name='teams', on_delete=models.CASCADE)
    played = models.PositiveSmallIntegerField(null=False, blank=False, default = 0)
    won = models.PositiveSmallIntegerField(null=False, blank=False, default = 0)
    draw = models.PositiveSmallIntegerField(null=False, blank=False, default = 0)
    lost = models.PositiveSmallIntegerField(null=False, blank=False, default = 0)
    points = models.PositiveSmallIntegerField(null=False, blank=False, default = 0)
    goal_diff = models.PositiveSmallIntegerField(null=False, blank=False, default = 12)
    position = models.PositiveSmallIntegerField(editable=True, null=False, blank=False, default = 0)
    season = models.CharField(max_length=16, null=False, blank=False, default='2018-19')
    
    class Meta:
      	db_table = 'team'
      	ordering = ('-points', 'name',)
      
    def __str__(self):
        return "%s (%s)" %(self.team_name, self.league)


class TeamStat(models.Model):
    team = models.ForeignKey(Team, related_name='statitics', on_delete=models.CASCADE)
    lst_five_games = JSONField()
    lst_five_home = JSONField()
    lst_five_away = JSONField()

    class Meta:
      	db_table = 'team_stats'
    
    def __str__(self):
        return self.team.name


class MatchSet(models.Model):
    TICKET_OUTCOME = [(WIN, 'Won'), (LOST, 'Lost'), (PENDING, 'Pending')]
    
    set_id = models.BigAutoField(primary_key=True, editable=False)
    ticket_outcome = models.CharField(max_length=4, choices=TICKET_OUTCOME, default=PENDING)
    time_created = models.DateTimeField(auto_now_add=True)
    sms_sent = models.CharField(max_length=1, default='N')
    last_updated = models.DateTimeField(auto_now_add=True)
    
    class Meta:
      db_table = 'match_sets'

    def __str__(self):
        return "Set id: %d" % (self.set_id)

    
class Match(models.Model):

    GAME_RESULTS = [(CORRECT, 'Correct prediction'), (INCORRECT, 'Incorrect prediction'),
                    (PENDING, 'Results pending'), (NO_RESULTS, 'No results')]
    
    match_id = models.BigAutoField(primary_key=True, editable=False) 
    home_team = models.OneToOneField(Team, related_name = '+' ,null=False, blank=False, on_delete=models.CASCADE)
    away_team = models.OneToOneField(Team, related_name = '+', null=False, blank=False, on_delete=models.CASCADE)
    start_time = models.DateField(null=True)
    finish_time = models.DateField(null=True)
    venue = models.CharField(max_length=50, null=True)
    league = models.ForeignKey(League, related_name = 'matches', on_delete=models.CASCADE)
    match_set = models.ForeignKey(MatchSet, related_name='matches', on_delete=models.CASCADE)
    source_api = models.CharField(max_length=25, null=True)
    results = models.CharField(max_length=6, choices=GAME_RESULTS, default=PENDING)
    score = models.CharField(max_length=5, null=True, blank=True, default = '0-0')
    last_updated = models.DateTimeField(auto_now_add=True)
    
    class Meta:
      ordering = ('start_time', 'last_updated',)
      db_table = 'match'
      
    def __str__(self):
     return "%d - %s vs %s" %(self.match_id, self.home_team, self.away_team)
    

class MarketCode(models.Model):
     type = models.CharField(max_length=16, null=True)
     code =  models.PositiveSmallIntegerField(null=False)   
     market = models.CharField(max_length=16, null=False, default = '')
     descr = models.CharField(max_length=25, null=False, default = '')

     class Meta:
      db_table = 'marketcodes'


class AvailableMarket(models.Model):
    
    PREDICTION_OPTIONS = [(WIN, 'Home win'), (AWAY, 'Away win'), (DRAW, 'Draw'),
                          (CANCELLED, 'Match cancelled'), (PENDING, 'Pending'),
                          (POSTPONED, 'Match postponed')]

    avail_id = models.BigAutoField(primary_key=True, editable=False)
    match = models.ForeignKey(Match, related_name='available_markets', on_delete = models.CASCADE)
    applicable_subscr_plans = JSONField()
    league = models.ForeignKey(League, related_name = 'available_markets', on_delete=models.CASCADE)
    market_type = models.ForeignKey(MarketCode, related_name='+', on_delete = models.CASCADE)
    markets = JSONField()
    prediction = models.CharField(max_length=6, choices=PREDICTION_OPTIONS, default=PENDING)
    date_created = models.DateTimeField(blank=False)
    last_updated = models.DateTimeField(auto_now_add=True)
        
    class Meta:
      db_table = 'avail_markets'
      ordering = ('last_updated',)
      
    def __str__(self):
      return "%d - %s" %(self.avail_id, self.prediction)

    
class Subscriber(models.Model):
    CHANNEL_IDS = [(MOBI, 'Mobi'), (APP, 'App'), (DESKTOP,'Desktop')]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = models.CharField(max_length=25, null=True, blank=True , editable=True)
    cell_num = models.CharField(max_length=12, null=True, blank=True, editable=True)
    reg_date = models.DateField(auto_now_add=True)
    channel_id = models.CharField(max_length=8, null=True, blank=True, choices=CHANNEL_IDS)

    @receiver(post_save, sender=User)
    def create_subscriber(sender, instance, created, **kwargs):
        if created:
           Subscriber.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_subscriber(sender, instance, **kwargs):
        instance.subscriber.save()


    class Meta:
      db_table = 'subscriber'
      ordering = ('-reg_date',)

    def __str__(self):
        return self.user.username
    
    def getUser(self):
        return self.user.username
    
    
class SubscriptionPlan(models.Model): 
    PLAN_TYPES = [(FREE, 'Free Plan'), (BASIC, 'Basic Plan'), (PROF, 'Professional Plan'),(EXPERT, 'Expert Advisor')]
    
    plan_descr = models.CharField(max_length=20, choices=PLAN_TYPES, default=FREE)
    price = models.DecimalField(max_digits=4, decimal_places=2, editable=True, default=0.0)
    max_alloc_sets = models.PositiveSmallIntegerField(editable=True, default=8)
    max_allowed_notif = models.PositiveSmallIntegerField(editable=True, default=8)
    #risk = models.CharField(max_length=5, null=True, blank=True, editable=True, default='Total')
    #summary_level = models.CharField(max_length=22, null=True, blank=True, editable=True, default='Limited Statistics')

    class Meta:
      db_table = 'subscr_plan'

    def __str__(self):
        return self.plan_descr
    
    def getAllocSets(self):
        return self.alloc_sets

    
class UserPlan(models.Model):
    user = models.OneToOneField(Subscriber, related_name='userplan', on_delete=models.CASCADE)    
    plan = models.OneToOneField(SubscriptionPlan, related_name='+',on_delete=models.CASCADE, null=True)
    curr_num_sets = models.IntegerField(editable=False, default=1)
    eff_from = models.DateTimeField(auto_now_add=True)
    eff_to = models.DateTimeField(default=timezone.now() + datetime.timedelta(days=364, hours=23, minutes=59, seconds=59))

    class Meta:
      db_table= 'userplan'
      ordering= ('-eff_from',)

    def __str__(self):
        return "User: %s, plan: %s" % (self.user, self.plan)

    def getUserPlanName(self):
        self.plan
        
        
"""class UserPreference(models.Model):
    TODO: Move user preferehences to the Settings/Accounts app
    OPTIONS = [(YES, 'Yes'),(NO, 'No')]

    subscriber = models.OneToOneField(Subscriber, related_name='preferences', on_delete=models.CASCADE)
    leagues = models.ManyToManyField(League, related_name='+')
    marketing_opt = models.CharField(max_length=1, choices=OPTIONS, default =NO)
    sms_opt = models.CharField(max_length=1,choices=OPTIONS, default=NO)
    email_opt = models.CharField(max_length=1,choices=OPTIONS, default =NO)

    class Meta:
      db_table = 'user_preferences'

    def __str__(self):
        return ("User: %s, Marketing: %s, SMS Opt in: %s, Email Opt: %s ") % (self.subscriber, self.marketing_opt, self.sms_opt, self.email_opt)
"""        
        
class federationLookUp(models.Model):
    fed_id = models.PositiveIntegerField(primary_key=True, editable=False)
    fed_name = models.CharField(max_length = 30)
    region = models.CharField(max_length=28)
    country = models.CharField(max_length=30)

    class Meta:
      db_table = 'fed_lookup'

    def __str__(self):
        return "Fed name: %s, Country: %s" % (self.fed_name, self.country)
