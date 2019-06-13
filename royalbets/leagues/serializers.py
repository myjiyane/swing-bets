# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers 
from leagues.models import Team, League, Match, AvailableMarkets

# Create your own model serializer here.
    
class TeamSerializer(serializers.ModelSerializer): 
   league = serializers.PrimaryKeyRelatedField(many=False, queryset= League.objects.all())
   class Meta:
      model = Team
      fields = 'team_id', 'team_cd', 'team_name', 'league', 'played', 'won', 'draw', 'lost', 'points', 'goal_diff', 'league_position', 'lst_five_home', 'lst_five_away', 'season' 
      depth = 1
   

class LeagueSerializer(serializers.ModelSerializer):
   teams = TeamSerializer(many=True)
   class Meta:
      model = League
      fields = 'leag_id', 'league_name', 'division', 'country_name', 'federation_name', 'teams'
      depth = 1
    

class MatchSerializer(serializers.ModelSerializer):
   home_team = serializers.PrimaryKeyRelatedField(many=False, queryset= Team.objects.all())  
    
   class Meta:
      model = Match
      fields = 'match_id', 'home_team', 'start_time', 'finish_time', 'results', 'score'
      depth = 1                             