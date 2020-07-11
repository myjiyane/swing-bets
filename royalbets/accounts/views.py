# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from leagues.models import User,Subscriber, SubscriptionPlan, UserPlan
from leagues.serializers import SubscriptionPlanSerializer
from .forms import SignUpForm

from rest_framework.decorators import api_view

from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView

@api_view(['GET', 'POST'])
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            
            pref_plan_name = request.session['preferred_plan']    
            subscriber = Subscriber.objects.get(user = user)
            subcr_plan = SubscriptionPlan.objects.get(plan_descr = pref_plan_name)
            
            """Create subscription plan for the user"""
            UserPlan.objects.create(user = subscriber, plan = subcr_plan, num_sets = subcr_plan.alloc_sets) 
            
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


@api_view(['GET'])
def setPrefPlan(request, *args, **kwargs):
    """Sets default subscription plan"""
    request.session['preferred_plan'] = kwargs.get('plan_name', 'Free')
    return redirect('signup') 


@api_view(['POST'])
def upgradeOrSetPlan(request, **kwargs):
    
    if request.user.is_authenticated: 
        subscriber = Subscriber.objects.get(user = request.user)
        upgradePlanName = kwargs.get('plan_name', 'Free')
        
        """Get subscription plan details from kwargs"""
        subcr_plan = SubscriptionPlan.objects.get(plan_descr = upgradePlanName)
        try:
            currUserPlan = UserPlan.objects.get(user = subscriber)
        except(KeyError, UserPlan.DoesNotExist):
            UserPlan.objects.create(user = subscriber, plan = subcr_plan, num_sets = subcr_plan.alloc_sets)
        else:
            currUserPlan.plan = subcr_plan
            currUserPlan.save()
            
    return render(request, 'plan_upgrade_complete.html', {'new_plan': upgradePlanName}) 
    

class PricePlanListView(ListView):
    """Allows unregistered/registered users to chose their subscription plan options from the given list"""
    serializer_class = SubscriptionPlanSerializer("json", many=True)
    template_name = "pricing-plan.html"
    
    def get_queryset(self):
        self.plans = SubscriptionPlan.objects.all()
        queryset = self.plans
        return queryset
    
    def get_context_data(self, **kwargs):
     kwargs['free'] = self.get_queryset().get(plan_descr = 'Free')
     kwargs['basic'] = self.get_queryset().get(plan_descr = 'Basic')
     kwargs['prof'] = self.get_queryset().get(plan_descr = 'Professional')
     kwargs['expert'] = self.get_queryset().get(plan_descr = 'Expert')
     
     if self.request.user.is_authenticated():
        subscriber = Subscriber.objects.get(user = self.request.user)
        
        try:
            currUserPlan = UserPlan.objects.get(user = subscriber)
        except(KeyError, UserPlan.DoesNotExist):
            kwargs['curr_plan'] = 'None'
        else:
            kwargs['curr_plan'] = currUserPlan.plan.plan_descr
            
     context = super(PricePlanListView, self).get_context_data(**kwargs)   
     return context
    

    
@api_view(['GET'])
def aboutUs(request):
    return render(request, 'about-us.html')