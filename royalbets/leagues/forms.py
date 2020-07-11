# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
import datetime

class GeneralQuoteForm(forms.Form):
    OPT = (
    ('Y', 'Yes'),
    ('N', 'No')
)   
    RES_TYPE = (
    ('TWNH', 'Townhouse'),
    ('DUE', 'Duet'),
    ('FL1', 'Flat (Above ground level)'),
    ('FL2', 'Flat (Ground level)')    
)   
    claim_type = forms.CharField(label='claim_type', max_length=24, required=False)
    name = forms.CharField(label='Name', max_length=24, required=False)
    surname = forms.CharField(label='Surname', required=False)
    id = forms.CharField(label='ID No', required=False)
    occ_bus = forms.CharField(label='Occupation / Business')
    landline = forms.CharField(label='Tel No landline')
    cell_no = forms.CharField(label='Cell No', required=False)
    email = forms.CharField(label='Email', required=False, widget=forms.TextInput())
    address_1 = forms.CharField(label='Address Line 1', required=False, widget=forms.TextInput())
    address_2 = forms.CharField(label='Address Line 2', widget=forms.TextInput())
    postal_cd = forms.CharField(label='Postal code', required=False)
    primary_address_1 = forms.CharField(label='Address', required=False, widget=forms.TextInput())
    primary_address_2 = forms.CharField(label='', required=False, widget=forms.TextInput())
    primary_postal_cd = forms.CharField(label='Postal code', required=False)
    primary_insured_amt = forms.DecimalField(label='Residence', min_value=1, decimal_places=2)
    primary_accidental_damage_amt = forms.DecimalField(label='Accidental damage cover', min_value=1, decimal_places=2)
    primary_mech_breakdown_amt = forms.DecimalField(label='Mechanical / Electrical breakdown cover', min_value=1, decimal_places=2)
    primary_power_surge_amt = forms.DecimalField(label='Power surge cover', min_value=1, decimal_places=2)
    primary_wild_baloons_amt = forms.DecimalField(label='Wild baloons & Monkeys cover', min_value=1, decimal_places=2)
    primary_residence_type = forms.ChoiceField(label='', choices=RES_TYPE)
    primary_residence_type_other = forms.CharField(label='Other (Describe)', required=False)
    primary_residence_sec_meas = forms.CharField(label='', required=False)
    primary_high_security = forms.ChoiceField(label='',choices=OPT, required=False)
    secondary_address_1 = forms.CharField(label='Address', required=False, widget=forms.TextInput())
    secondary_address_2 = forms.CharField(label='', required=False, widget=forms.TextInput())
    secondary_postal_cd = forms.CharField(label='Postal code', required=False)
    secondary_insured_amt = forms.DecimalField(label='Residence', min_value=1, decimal_places=2)
    secondary_accidental_damage_amt = forms.DecimalField(label='Accidental damage cover', min_value=1, decimal_places=2)
    secondary_mech_breakdown_amt = forms.DecimalField(label='Mechanical / Electrical breakdown cover', min_value=1, decimal_places=2)
    secondary_power_surge_amt = forms.DecimalField(label='Power surge cover', min_value=1, decimal_places=2)
    secondary_wild_baloons_amt = forms.DecimalField(label='Wild baloons & Monkeys cover', min_value=1, decimal_places=2)
    secondary_residence_type = forms.ChoiceField(label='', choices=RES_TYPE)
    current_insurer = forms.CharField(label='Current Insurer:')
    itc_check = forms.ChoiceField(label='',choices=OPT, required=False)
    year = forms.DateField(label='', input_formats=['%Y'])
    claims = forms.CharField(label='', required=False, widget=forms.TextInput())
    claims_value = forms.DecimalField(label='Rands', min_value=1, decimal_places=2)
    unspec_risk_1 = forms.CharField(label='', required=False, widget=forms.TextInput())
    unspec_risk_2 = forms.CharField(label='', required=False, widget=forms.TextInput())
    unspec_risk_3 = forms.CharField(label='', required=False, widget=forms.TextInput())
    unspec_risk_4 = forms.CharField(label='', required=False, widget=forms.TextInput())
    unspec_risk_5 = forms.CharField(label='', required=False, widget=forms.TextInput())
    unspec_risk_amt_1 = forms.DecimalField(label='', min_value=1, decimal_places=2)
    unspec_risk_amt_2 = forms.DecimalField(label='', min_value=1, decimal_places=2)
    unspec_risk_amt_3 = forms.DecimalField(label='', min_value=1, decimal_places=2)
    unspec_risk_amt_4 = forms.DecimalField(label='', min_value=1, decimal_places=2)
    unspec_risk_amt_5 = forms.DecimalField(label='', min_value=1, decimal_places=2)
    owner_name_motor_1 = forms.CharField(label='Owner name', required=False, widget=forms.TextInput())
    owner_surname_motor_1 = forms.CharField(label='Surname', required=False, widget=forms.TextInput())
    name_motor_1 = forms.CharField(label='Name', required=False, widget=forms.TextInput())
    surname_motor_1 = forms.CharField(label='Surname', required=False, widget=forms.TextInput())
    ID_motor_1 = forms.CharField(label='ID No', required=False, widget=forms.TextInput())
    licence_cd_motor_1 = forms.CharField(label='Licence code', required=False, widget=forms.TextInput())
    date_of_lic_motor_1 = forms.DateField(label='Date of licence', required=False, input_formats=['%Y'])
    addr1_motor_1 = forms.CharField(label='Address', required=False, widget=forms.TextInput())
    addr2_motor_1 = forms.CharField(label='', required=False, widget=forms.TextInput())
    postal_motor_1 = forms.CharField(label='Postal code', required=False, widget=forms.TextInput())
    degree_motor_1 = forms.ChoiceField(label='',choices=OPT, required=False)
    claim_year_motor_1 = forms.CharField(label='', required=False, widget=forms.TextInput())
    claim_type_motor_1 = forms.CharField(label='', required=False, widget=forms.TextInput())
    claim_value_motor_1 = forms.DecimalField(label='', min_value=1, decimal_places=2)
    cover_motor_1 = forms.ChoiceField(label='',choices=OPT, required=False)
    additional_cover_motor_1 = forms.ChoiceField(label='',choices=OPT, required=False)
    year_motor_1 = forms.CharField(label='Year', required=False, widget=forms.TextInput())
    reg_motor_1 = forms.CharField(label='Reg no', required=False, widget=forms.TextInput())
    engine_motor_1 = forms.CharField(label='Engine no', required=False, widget=forms.TextInput())
    vin_motor_1 = forms.CharField(label='Vin no', required=False, widget=forms.TextInput())
    make_motor_1 = forms.CharField(label='Make', required=False, widget=forms.TextInput())
    model_motor_1 = forms.CharField(label='Model', required=False, widget=forms.TextInput())
    color_motor_1 = forms.CharField(label='Color', required=False, widget=forms.TextInput())
    use_motor_1 = forms.CharField(label='Type of use', required=False, widget=forms.TextInput())
    night_park_motor_1 = forms.CharField(label='Overnight parking', required=False, widget=forms.TextInput())
    sec_motor_1 = forms.CharField(label='Security', required=False, widget=forms.TextInput())
    other_motor_1 = forms.CharField(label='Other', required=False, widget=forms.TextInput())
    
    
    
    
    
    
    
