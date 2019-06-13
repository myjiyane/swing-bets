# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.urls import resolve, reverse

from leagues.models import League, Team
from ..views import team_list

# Create your tests here.
class TeamListViewTest(TestCase):
    def setUp(self):
        self.league = League.objects.create(league_name="Engish Premier League", division= "First Division", country_name="England", federation_name="UEFA")
        self.team = Team.objects.create(team_cd="TOT", team_name="Tottehnam", league=self.league, played=5)
        #self.response = self.client.get(reverse('league:team_list', kwargs={'pk': self.league.pk}))
        #return self.response
        
        
    def test_success_response(self):
        res = self.client.get(reverse('leagues:team_list', kwargs={'pk': self.league.leag_id}))
        self.assertEquals(res.status_code, 200)


    def test_no_team_exists(self):
        response = self.client.get(reverse('leagues:team_list', kwargs={'pk':5}))
        self.assertEquals(response.status_code, 404)
    
    
    def test_view_team_list(self):
        """Verifies if the correct view was used to serve the the response --> used in function-based views"""
        view = resolve('/leagues/2000/')
        self.assertEquals(view.func, TeamListView)