# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from django.utils import timezone
#from django_mysql.models import JSONField

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

MOBI = 'M'
DESKTOP = 'DESKTOP'
APP = 'APP'

WIN = '1'
DRAW = 'X'
AWAY = '2'
LOST = '0'

CANCELLED = 'CANC'
PENDING = 'PEND'
POSTPONED = 'POST'
CORRECT = 'CORR'
INCORRECT = 'INCO'
NO_RESULTS = 'NRES'
ABANDONED = 'ABAN'

YES= 'Y'
NO = 'N'


# Create your models here.
class League(models.Model):
    leag_id = models.BigAutoField(primary_key=True, editable=False)
    league_name = models.CharField(max_length=30, null=False, blank=False)
    division = models.CharField(max_length=30, null=True)
    country_name = models.CharField(max_length=30, unique=True)
    country_iso = models.CharField(max_length=6)
    federation_name = models.CharField(max_length=55)
    last_updated = models.DateTimeField(auto_now_add=True)

    class Meta:
      ordering = ('league_name', 'federation_name',)
      db_table = 'leagues'
      
    def __str__(self):
      return "%s (%s)" % (self.league_name, self.country_name)

     
class Team(models.Model):
    team_id = models.BigAutoField(primary_key=True, editable=False)    
    team_cd = models.CharField(max_length=8, null=False)    
    team_name = models.CharField(max_length=32)
    league = models.ForeignKey(League, related_name='teams', on_delete=models.CASCADE)
    played = models.PositiveIntegerField(null=False, blank=False, default = 0)
    won = models.PositiveIntegerField(null=False, blank=False, default = 0)
    draw = models.PositiveIntegerField(null=False, blank=False, default = 0)
    lost = models.PositiveIntegerField(null=False, blank=False, default = 0)
    points = models.PositiveIntegerField(null=False, blank=False, default = 0)
    goal_diff = models.IntegerField(null=False, blank=False, default = 12)
    league_position = models.PositiveIntegerField(editable=True, null=False, blank=False, default = 0)
    lst_five_games = models.CharField(max_length=6, null=False, blank=False, default='W')
    lst_five_home = models.CharField(max_length=6, null=False, blank=False, default='W')
    lst_five_away = models.CharField(max_length=6, null=False, blank=False, default='W')
    season = models.CharField(max_length=16, null=False, blank=False, default='2018-19')
    
    class Meta:
      db_table = 'team'
      ordering = ('team_name',)
      
    def __str__(self):
     return "%s (League name: %s)" % (self.team_name, self.league.league_name)


class MatchSets(models.Model):
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

    PREDICTION_OPTIONS = [(WIN, 'Home win'), (AWAY, 'Away win'), (DRAW, 'Draw'),
                          (CANCELLED, 'Match cancelled'), (PENDING, 'Pending'),
                          (POSTPONED, 'Match Postponed')]
    
    

    GAME_RESULTS = [(CORRECT, 'Correct prediction'), (INCORRECT, 'Incorrect prediction'),
                    (PENDING, 'Results pending'), (NO_RESULTS, 'No results')]
    
    match_id = models.BigAutoField(primary_key=True, editable=False) 
    home_team = models.OneToOneField(Team, related_name = '+' ,null=False, blank=False, on_delete=models.CASCADE)
    away_team = models.OneToOneField(Team, related_name = '+', null=False, blank=False, on_delete=models.CASCADE)
    start_time = models.DateTimeField(null=True)
    finish_time = models.DateTimeField(null=True)
    venue = models.CharField(max_length=50, null=True)
    league = models.ForeignKey(League, related_name = 'matches', on_delete=models.CASCADE)
    match_set = models.ForeignKey(MatchSets, related_name='matches', on_delete=models.CASCADE)
    source_api = models.CharField(max_length=25, null=True)
    results = models.CharField(max_length=6, choices=GAME_RESULTS, default=PENDING)
    score = models.CharField(max_length=6, null=True, blank=True, default = '0:0')
    last_updated = models.DateTimeField(auto_now_add=True)
    
    class Meta:
      ordering = ('start_time', 'last_updated',)
      db_table = 'match'
      
    def __str__(self):
     return "%d - %s vs %s" %(self.match_id, self.home_team, self.away_team)
    

class AvailableMarkets(models.Model):
    
    PREDICTION_OPTIONS = [(WIN, 'Home win'), (AWAY, 'Away win'), (DRAW, 'Draw'),
                          (CANCELLED, 'Match cancelled'), (PENDING, 'Pending'),
                          (POSTPONED, 'Match Postponed')]

    avail_id = models.BigAutoField(primary_key=True, editable=False)
    match = models.ForeignKey(Match, related_name='available_markets', on_delete = models.CASCADE)
    market_type = models.CharField(max_length=16, null=False, default = 'NA')
    market = models.CharField(max_length=100, null=False, default = 'NA')
    prediction = models.CharField(max_length=6, choices=PREDICTION_OPTIONS, default=PENDING)
    date_created = models.DateTimeField(blank=False)
    last_updated = models.DateTimeField(auto_now_add=True)
        
    class Meta:
      db_table = 'avail_markets'
      ordering = ('last_updated',)
      
    def __str__(self):
      return "Avail id: %d (Match: %s)" %(self.avail_id, self.match)

    
class Subscriber(models.Model):
    CHANNEL_IDS = [(MOBI, 'Mobi site'), (APP, 'Smart App'), (DESKTOP,'Desktop computer')]
    
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
      ordering = ('reg_date',)

    def __str__(self):
        return self.user.username
    
    
class SubscriptionPlan(models.Model): 
    plan_descr = models.CharField(max_length=100, default='Plan A')
    price = models.DecimalField(max_digits=4, decimal_places=2, editable=True, default=0.0)
    alloc_sets = models.IntegerField(editable=True, default=1)

    class Meta:
      db_table = 'subscr_plan'

    def __str__(self):
        return self.plan_descr


class UserPlan(models.Model):
    user = models.OneToOneField(Subscriber, related_name='userplan', on_delete=models.CASCADE)    
    plan = models.OneToOneField(SubscriptionPlan, related_name='+', on_delete=models.CASCADE)
    num_sets = models.IntegerField(editable=True, default=1)
    eff_from = models.DateTimeField(auto_now_add=True)
    eff_to = models.DateTimeField(default=timezone.now() + datetime.timedelta(days=364, hours=23, minutes=59, seconds=59))

    class Meta:
      db_table= 'userplan'
      ordering= ('eff_from',)

    def __str__(self):
        return "User: %s, Plan: %s, Num sets: %d" % (self.user, self.plan.plan_descr, self.num_sets)


class UserPreferences(models.Model):
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
        
        
class federationLookUp(models.Model):
    fed_id = models.PositiveIntegerField(primary_key=True, editable=False)
    fed_name = models.CharField(max_length = 30)
    region = models.CharField(max_length=28)
    country = models.CharField(max_length=30)

    class Meta:
      db_table = 'fed_lookup'

    def __str__(self):
        return "Fed name: %s, Country: %s" % (self.fed_name, self.country)
