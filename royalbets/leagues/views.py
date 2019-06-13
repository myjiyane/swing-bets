# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.shortcuts import render, get_object_or_404
from rest_framework import renderers, status, generics

from django.http import HttpResponse
from django.views.generic import ListView

from .models import League, Team, AvailableMarkets, Match
from .serializers import LeagueSerializer, TeamSerializer, MatchSerializer

# Create your views here.

@api_view(['GET'])
def home(request, format='html'):
    """
    List all leagues, or create a new ones.
    """
    queryset = League.objects.all()
    serializer_class = LeagueSerializer(queryset, many=True)
    
    return Response({'leagues': serializer_class.data}, template_name='league-list.html', status=status.HTTP_200_OK)


class TeamListView(ListView):
  serializer_class = TeamSerializer("json", many=True)
  template_name = 'teams.html'
    
 """Overriding default context""" 
  def get_context_data(self, **kwargs):
        kwargs['league'] = self.league
        kwargs['leaguelist'] = League.objects.all()
        context = super(TeamListView, self).get_context_data(**kwargs)
        return context
    
  def get_queryset(self):
       self.league = get_object_or_404(League, pk=self.kwargs.get('pk'))
       queryset = self.league.teams
       return queryset

    
class MatchListView(ListView):
  """
  Returns a list of all games under a given leauge id
  """
  serializer_class = MatchSerializer("json", many=True)
  template_name = 'teams.html'
  
  def get_context_data(self, **kwargs):
         kwargs['league'] = self.league
         context = super(MatchListView, self).get_context_data(**kwargs)
         return context

  def get_quertset(self):
      self.league = get_object_or_404(League, pk = self.kwargs('pk'))
      queryset = self.league.matches
      return queryset