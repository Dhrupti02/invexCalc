from django import forms 
from django.forms import formset_factory
from .models import *

class OptionStrategyDupForm(forms.ModelForm):
    class Meta:
        model = OptionStrategyDup
        fields = ('ticker', 'current_stock_price', 'risk_free_rate', 'days_from_today', 'default_interval', 'start_date', 'end_date', 'current_date', 'is_active', 'cash_in_hand', 'extra_cash')

class OptionStrategyPositionDupForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):

        if kwargs.get('dates') != None:
            dates = kwargs.pop('dates')
            super(OptionStrategyPositionDupForm, self).__init__(*args, **kwargs)
            self.fields["expiry_date"] = forms.ChoiceField(choices = dates)
            self.fields["strike"] = forms.ChoiceField(choices = [('','--------')])
        else:
            super(OptionStrategyPositionDupForm, self).__init__(*args, **kwargs)

        # self.fields["submitted_by"] = kwargs["submitted_by"]

    class Meta:
        model = OptionStrategyPositionDup
        fields = ('buysell', 'contract', 'callput', 'volatility', 'premium', 'debit_credit', 'initial_trade_cost', 'cash_required', 'initial_cash_req', 'strike')

OptionStrategyPositionDupFormSet = formset_factory(OptionStrategyPositionDupForm, extra=1)

class OptionStrategySpreadDupForm(forms.ModelForm):
    class Meta:
        model = OptionStrategySpreadDup
        fields = ('cash_required', 'initial_cash_required')