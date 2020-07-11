# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .models import League, Team, AvailableMarket, Match, Subscriber, UserPlan
from .serializers import LeagueSerializer, TeamSerializer, MatchSerializer, SubscriptionPlanSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.shortcuts import render, get_object_or_404
from rest_framework import renderers, status, generics
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import GeneralQuoteForm
from django.http import HttpResponse
from django.views.generic import ListView

from django.utils import timezone
import datetime

# Create your views here.
class HomeListView(ListView):
    """List all leagues, latest footballing tips, scores, and match schedules
    """
    serializser_class = TeamSerializer("json", many=True)
    template_name = 'index.html'
    
    def get_queryset(self):
        queryset = Match.objects.all()
        return queryset
   
    def get_context_data(self, **kwargs):
        tDate = timezone.now() 
        today = tDate.strftime("%Y-%m-%d")
        yestDate = (tDate - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        tomorDate = (tDate + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
         
        kwargs['matches_all'] = self.get_queryset
        kwargs['matches_today'] = self.get_queryset().filter(start_time = today)
        kwargs['matches_yest'] = self.get_queryset().filter(start_time = yestDate)
        kwargs['matches_tomor'] = self.get_queryset().filter(start_time = tomorDate)
        kwargs['all_mkts'] = AvailableMarkets.objects.all()
        context = super(HomeListView, self).get_context_data(**kwargs)
        return context
    
    
class TeamListView(ListView):
  serializer_class = TeamSerializer("json", many=True)
  template_name = 'league-details.html'
  
  def get_queryset(self):
       league = self.kwargs.get('league_name')
       
       if league == 'epl':
          league = 'English Premier League'
       elif league == 'esp':        
          league = 'Spanish Primera Liga' 
       elif league == 'seria':
          league = 'Seria A'
       elif league == 'psl':        
          league = 'Premier Soccer League'   
       elif league == 'fra':        
          league = 'French legue'
       else:         
          league = 'all'
        
       self.league = get_object_or_404(League, league_name=league)
       queryset = self.league.teams
       return queryset

  """Overriding default context""" 
  def get_context_data(self, **kwargs):
        kwargs['league'] = self.league
        kwargs['matches'] = self.league.matches
        kwargs['predictions'] = self.league.available_markets
        kwargs['leaguelist'] = League.objects.all()
        context = super(TeamListView, self).get_context_data(**kwargs)
        return context

    
class PredictionsListView(LoginRequiredMixin, ListView):
  """
  Returns a list of all games for a given leauge 
  """
  serializer_class = TeamSerializer("json", many=True)
  template_name = 'predictions.html'  
  
  def get_queryset(self):
       self.available_markets = AvailableMarkets.objects.all()
       queryset = self.available_markets
       return queryset

  """Overriding default context""" 
  def get_context_data(self, **kwargs):
        
        kwargs['predictions'] = self.get_queryset
        kwargs['pred_double'] = self.get_queryset().filter(market_type='Double chance')
        kwargs['pred_over_under_1'] = self.get_queryset().filter(market_type='Over/Under 1.5')
        kwargs['pred_over_under_2'] = self.get_queryset().filter(market_type='Over/Under 2.5')
        
        
        """TODO: Ensure that this check passes test"""
        if self.request.user.is_authenticated():
          
          """Get current logged in user""" 
          currentUser = Subscriber.objects.get(user=self.request.user)
          userplan = UserPlan.objects.get(user=currentUser)
         
          kwargs['sub_plan'] = userplan.plan.plan_descr
        
          if userplan.plan == 'Basic': 
             kwargs['pred_straight'] = self.get_queryset().filter(market_type='Straight chance')
          elif userplan.plan == 'Professional':
             kwargs['pred_straight'] = self.get_queryset().filter(market_type='Straight chance')
             kwargs['pred_half'] = self.get_queryset().filter(market_type='Half chance')
          elif userplan.plan == 'Expert':  
             kwargs['pred_straight'] = self.get_queryset().filter(market_type='Straight chance')
             kwargs['pred_half'] = self.get_queryset().filter(market_type='Half chance')  
          
        context = super(PredictionsListView, self).get_context_data(**kwargs)
        return context
    
    
class LeagueListView(ListView):
    """ 
    Returns a list of all major football leagues 
    """
    serializer_class = LeagueSerializer("json", many=True)
    template_name = 'league-list.html'
    
    def get_queryset(self):
       self.league = League.objects.all()
       queryset = self.league
       return queryset
    
    """Capture only the major leagues"""
    def get_context_data(self, **kwargs):
        kwargs['leagues'] = self.get_queryset()
        kwargs['england'] = self.get_queryset().filter(country__name = 'England')
        kwargs['italy'] = self.get_queryset().filter(country__country__name = 'Italy')
        kwargs['spain'] = self.get_queryset().filter(country__name = 'Spain')
        kwargs['france'] = self.get_queryset().filter(country__country_name = 'France')
        kwargs['rsa'] = self.get_queryset().filter(country__name = 'South Africa')
        kwargs['germany'] = self.get_queryset().filter(country__name = 'Germany')
        kwargs['scotland'] = self.get_queryset().filter(country__name = 'Scotland')
        
        context = super(LeagueListView, self).get_context_data(**kwargs)
        return context
     
    