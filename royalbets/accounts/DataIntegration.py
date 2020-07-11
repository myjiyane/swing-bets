# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from leagues.models import User,Subscriber, SubscriptionPlan, UserPlan
from leagues.serializers import SubscriptionPlanSerializer
from .forms import SignUpForm

from rest_framework.decorators import api_view

from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView

