# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers 
from leagues.models import Team, League, Match, AvailableMarket, SubscriptionPlan

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
      fields = 'leag_id', 'league_name','league_cd', 'division', 'country_name', 'federation_name', 'teams','matches', 'available_markets'
      depth = 1
    

class MatchSerializer(serializers.ModelSerializer):
   available_markets = serializers.PrimaryKeyRelatedField(many=True, queryset = AvailableMarket.objects.all())  
    
   class Meta:
      model = Match
      fields = 'match_id', 'home_team', 'start_time', 'finish_time', 'venue', 'match_set', 'source_api', 'last_updated', 'available_markets','results', 'score'
      depth = 1    

class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
       model = SubscriptionPlan
       fields = '__all__'
       depth = 1