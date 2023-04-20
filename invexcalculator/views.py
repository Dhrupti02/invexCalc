from django.shortcuts import render
from django.http import HttpResponse
from .models import *
import json
from .forms import *
import requests
from django.db import transaction
from django.shortcuts import render, redirect
import math 
from datetime import date, datetime

# Create your views here.
def home(request):
    return render(request, 'index.html')

def analyserT1CalcDup(data, strategy):
    res = {}
    daysFromToday = data['days_from_today']
    h1 = stock_price = data['stock_price']
    min_int = round((100 - data['interval']) / 100, 2)
    max_int = round((100 + data['interval']) / 100, 2)
    g1 = l1 = round(stock_price * min_int, 2)
    f1 = l2 = round(l1 * min_int, 2)
    e1 = l3 = round(l2 * min_int, 2)
    d1 = l4 = round(l3 * min_int, 2)
    c1 = l5 = round(l4 * min_int, 2)
    b1 = l6 = round(l5 * min_int, 2)
    l7 = round(l6 * min_int, 2)
    l8 = round(l7 * min_int, 2)
    l9 = round(l8 * min_int, 2)
    l10 = round(l9 * min_int, 2)

    i = h1 = round(data['stock_price'] * max_int, 2)
    j = h2 = round(h1 * max_int, 2)
    k = h3 = round(h2 * max_int, 2)
    l = h4 = round(h3 * max_int, 2)
    m = h5 = round(h4 * max_int, 2)
    n = h6 = round(h5 * max_int, 2)
    h7 = round(h6 * max_int, 2)
    h8 = round(h7 * max_int, 2)
    h9 = round(h8 * max_int, 2)
    h10 = round(h9 * max_int, 2)

    res['row1'] = {
        'l1': l1,
        'l2': l2,
        'l3': l3,
        'l4': l4,
        'l5': l5,
        'l6': l6,
        'h1': h1,
        'h2': h2,
        'h3': h3,
        'h4': h4,
        'h5': h5,
        'h6': h6,
        'h7': h7,
        'h8': h8,
        'h9': h9,
        'h10': h10,
        'l7': l7,
        'l8': l8,
        'l9': l9,
        'l10': l10,
        'sp': round(data['stock_price'], 2)
    }

    dbcr_total = 0
    itc_total = 0
    total_spread_val = 0
    sids = []
    spread = []

    if 'spreadid' in data and len(data['spreadid']):
        for spreadid in data['spreadid']:
            _sids = spreadid.split("-")
            sids.append(_sids[0])
            sids.append(_sids[1])
            
            if data['buysell'][_sids[0]] == 'buy':
                lsid = _sids[0]
                ssid = _sids[1]
            else:
                lsid = _sids[1]
                ssid = _sids[0]
                
            if data['initial_cash_required'][_sids[0]] != "":
                icr1 = data['initial_cash_required'][_sids[0]]
            else:
                if data['buysell'][_sids[0]] == 'buy':
                    icr1 = strategy[_sids[0]] * data['quantity'][_sids[0]] * 100
                else:
                    icr1 = strategy[_sids[0]] * data['quantity'][_sids[0]] * (-100)
                    
            if data['initial_cash_required'][_sids[1]] != "":
                icr2 = data['initial_cash_required'][_sids[1]]
            else:
                if data['buysell'][_sids[1]] == 'buy':
                    icr2 = strategy[_sids[1]] * data['quantity'][_sids[0]] * 100
                else:
                    icr2 = strategy[_sids[1]] * data['quantity'][_sids[0]] * (-100)
            
            if data['instrument'][_sids[0]] == 'p' and data['strike'][ssid] > data['strike'][lsid]:
                Net_ITC = round((icr1 + icr2), 2)
                totalSpreadVal += (data['strike'][ssid] - data['strike'][lsid]) * (data['quantity'][_sids[0]] * 100) + Net_ITC
                spread[spreadid] = (data['strike'][ssid] - data['strike'][lsid]) * (data['quantity'][_sids[0]] * 100) + Net_ITC
            elif data['instrument'][_sids[0]] != 'c':
                Net_ITC = round((icr1 + icr2), 2)
                totalSpreadVal += Net_ITC
                spread[spreadid] = Net_ITC

            if data['instrument'][_sids[0]] == 'c' and data['strike'][ssid] < data['strike'][lsid]:
                Net_ITC = round((icr1 + icr2), 2)
                totalSpreadVal += (data['strike'][lsid] - data['strike'][ssid]) * (data['quantity'][_sids[0]] * 100) + Net_ITC
                spread[spreadid] = (data['strike'][lsid] - data['strike'][ssid]) * (data['quantity'][_sids[0]] * 100) + Net_ITC
            elif data['instrument'][_sids[0]] != 'p':
                Net_ITC = round((icr1 + icr2), 2)
                totalSpreadVal += Net_ITC
                spread[spreadid] = Net_ITC

    for key, value in strategy.items():
        if data['buysell'][key] == 'buy':
            dbcrTotal += value * data['quantity'][key] * 100
        else:
            dbcrTotal -= value * data['quantity'][key] * 100
            
        if 'itci' in data and data['itci'][key] != 0:
            itcTotal += data['itci'][key]
            
        if key not in sids:
            if data['buysell'][key] == 'buy':
                totalSpreadVal += (value * data['quantity'][key] * 100)
            else:
                totalSpreadVal -= (value * data['quantity'][key] * 100)
    # for spread calc
    totalICRVal = 0
    if 'initial_cash_required' in data:
        for icr in data['initial_cash_required']:
            if icr:
                totalICRVal += icr
    totalICRVal = totalICRVal - data['cash']

    calc_itc = 0
    for key, buysell in enumerate(data['buysell']):
        time = round((data['days_to_exp'][key] - daysFromToday) / 365, 4)
        lastkey = ""
        calc_itc += data['itci'][key]
        for k, value in enumerate(res['row1']):
            lastkey = k
            tmp = BlackScholes(data['instrument'][key], value, data['strike'][key], time, data['risk_free_rate'], data['volatility'][key])
            if isinstance(tmp, (int, float)):
                tmp = round(tmp, 4)
            if buysell == 'sell':
                tmp = tmp * (-1)
            if k in res['row2']:
                res['row2'][k] += data['quantity'][key] * tmp * 100  # 1 contract = 100 quantity
            else:
                res['row2'][k] = data['quantity'][key] * tmp * 100
            res['row11'][key][k] = {'total': data['quantity'][key] * tmp * 100, 'instrument': data['instrument'][key], 'value': value, 'strike': data['strike'][key], 'days': data['days_to_exp'][key], 'risk_free_rate': data['risk_free_rate'], 'volatility': data['volatility'][key], 'buysell': buysell, 'contract': data['quantity'][key], 'premium': tmp}
            res['row2'][k] = round(res['row2'][k], 4)

    optStr = None
    if 'id' in data:
        optStr = OptionStrategyDup.objects.filter(id=data['id']).first()
    if optStr and optStr.parent_id:
        parent = OptionStrategyDup.objects.filter(id=optStr.parent_id).first()
        if parent:
            calc_itc = parent.calc_itc + data['extra_cash']
    else:
        calc_itc = calc_itc + data['extra_cash']
    for key, value in res['row2'].items():
        if 'initial_trade_cost' in data and data['initial_trade_cost'] != 0:
            res['row3'][key] = round(((value - data['initial_trade_cost'])/data['initial_trade_cost'])*100, 2)
        else:
            res['row3'][key] = round(((value - res['row2']['sp'])/res['row2']['sp'])*100, 2)
        res['row4'][key] = round(((res['row1'][key]*100)/res['row1']['sp'])-100, 2) + " %"
        cash = 0
        if 'cash' in data and data['cash'] != "":
            cash = data['cash']
        for k, val in enumerate(data['itci']):
            itcVal = res['row11'][k]['sp']['total']
            if val is not None and val != 0:
                res['row5'][k][key] = round(((res['row11'][k][key]['total'] - val)/val)*100, 2)
                res['row11'][k][key]['total'] = res['row11'][k][key]['total'] - val
            else:
                res['row5'][k][key] = round(((res['row11'][k][key]['total']/res['row11'][k]['sp']['total'])*100-100), 2)
                res['row11'][k][key]['total'] = res['row11'][k][key]['total'] - itcVal
            if data['buysell'][k] == 'sell':
                res['row5'][k][key] = res['row5'][k][key]*(-1)
            if key in res['netpl']:
                res['netpl'][key] = round((res['netpl'][key]+res['row11'][k][key]['total']+cash), 2)
            else:
                res['netpl'][key] = round(res['row11'][k][key]['total']+cash, 2)
            if totalICRVal != 0:
                res['netpl'][key+'p'] = round((res['netpl'][key]/calc_itc)*100, 2)
            else:
                res['netpl'][key+'p'] = round((res['netpl'][key]/totalSpreadVal)*100, 2)
            cash = 0
    res['totalICRVal'] = round(totalICRVal, 3)
    res['spread'] = spread
    res['totalSpreadVal'] = totalSpreadVal

def calculateFcfmRnd(request):
    data = request.copy()
    yearVals = data['amo_year_val']
    currYearRndExp = data['curr_year_rnd_exp']
    cal = 0
    ammortAssetCurrYr = 0
    b3 = len(yearVals)
    for key, value in enumerate(yearVals):
        cal += value * (b3 - key) / b3
        ammortAssetCurrYr += value / b3
    researchAsset = cal + currYearRndExp
    capitalizedRnd = currYearRndExp - ammortAssetCurrYr
    return {'researchAsset': researchAsset, 'capitalizedRnd': capitalizedRnd}

def BlackScholes(call_put_flag, S, X, T, r, v):
    r = r / 100
    v = v / 100
    d1 = (math.log(S / X) + (r + pow(v, 2) / 2) * T) / (v * pow(T, 0.5))
    d2 = d1 - v * pow(T, 0.5)
    if call_put_flag == 'c':
        return S * CND(d1) - X * math.exp(-r * T) * CND(d2)
    else:
        return X * math.exp(-r * T) * CND(-d2) - S * CND(-d1)
    
def CND(x):
    Pi = 3.141592653589793238
    a1 = 0.319381530
    a2 = -0.356563782
    a3 = 1.781477937
    a4 = -1.821255978
    a5 = 1.330274429
    L = abs(x)
    k = 1 / (1 + 0.2316419 * L)
    p = 1 - 1 / pow(2 * Pi, 0.5) * math.exp(-pow(L, 2) / 2) * (
            a1 * k + a2 * pow(k, 2) + a3 * pow(k, 3) + a4 * pow(k, 4) + a5 * pow(k, 5))
    if x >= 0:
        return p
    else:
        return 1 - p
    
def optionCalcDup(request):
    data = request.data
    res = []
    daysFromToday = data['days_from_today']
    for key, buysell in enumerate(data['buysell']):
        time = (data['days_to_exp'][key]-daysFromToday)/365
        res.append(BlackScholes(data['instrument'][key], data['stock_price'], data['strike'][key], time, data['risk_free_rate'], data['volatility'][key]))
        if isinstance(res[key], (int, float)): res[key] = round(res[key], 4)
    response = {}


    response['analyserT1Calc'] = analyserT1CalcDup(data, res)
    response['strategy'] = res
    return response

def save_spread_dup(strategy, calc, post_data):
    spread = {}
    spread['option_strategy_id'] = strategy.id

    for key, value in calc['spread'].items():
        pids = key.split("-")
        spread['position_id_first'] = pids[0]
        spread['position_id_second'] = pids[1]
        spread['cash_required'] = value

        if 'initial_cash_required' in post_data and post_data['initial_cash_required'][key] != "" and post_data['initial_cash_required'][key] != 0:
            spread['initial_cash_required'] = post_data['initial_cash_required'][key]

        OptionStrategySpreadDup.update_or_create(
            option_strategy_id=strategy.id,
            position_id_first=pids[0],
            position_id_second=pids[1],
            defaults=spread
        )

def getCalc(request):
    context = {}
    if request.method == 'GET':
        ticker = request.GET.get('ticker')

        price = requests.get('https://cp1.invexwealth.com/api/v2/company-profile-quote?symbol=AAPL')
        price = price.json()['data']['price']

        data = '{"date":"2023/04/06","symbol":"AAPL","low_strike":"1","high_strike":"100"}'
        expiry = requests.post('https://cp2.invexwealth.com/option_chain', data=data)
        
        exp = list(expiry.json()['data'].keys())
        dta = {i: list(expiry.json()['data'][i]["Strike"].values()) for i in expiry.json()['data'].keys()}
        dictt = {'ticker':ticker, 'current_stock_price':price}

        frm = OptionStrategyDupForm(dictt)
        # frm1 = OptionStrategyPositionDupForm(dates=((a,a) for a in exp))
        frm1 = OptionStrategyPositionDupFormSet(form_kwargs={"dates":((a,a) for a in exp)})
        
        context['form'] = frm
        context['formsets'] = frm1
        context['strike'] = json.dumps(dta)

        request.session['expiry_date'] = exp
        request.session['strike'] = json.dumps(dta)
        request.session['exp'] = exp
        request.session['dta'] = dta

        return render(request, 'calculator.html', context)

def calc(request):
    form = OptionStrategyDupForm(request.POST or None)
    # form1 = OptionStrategyPositionDupForm(request.POST  or None)
    formset = OptionStrategyPositionDupFormSet(request.POST or None)
    context = {}
    context1 = {}
    context['form'] = form
    context['formsets'] = formset
    if request.session.has_key('expiry_date'):
        exp_date = request.session.get('expiry_date')
        strike1 = request.session.get('strike')  
        dictt = request.session.get('dictt')  

    # print(strike1)    

    ### Calculator 
    if request.method == 'POST':
                if formset.is_valid():
                    premium = []
                    total = request.POST['form-TOTAL_FORMS']
                    total = int(total)-1

                    stock_price = float(request.POST['current_stock_price'])
                    risk_free_rate = float(request.POST['risk_free_rate'])
                    days_from_today = int(request.POST['days_from_today'])
                    interval = int(request.POST['default_interval'])
                    start_date = request.POST['start_date']

            # for form in formset:
                buysell = request.POST['form-'+str(total)+'-buysell']
                contract = int(request.POST['form-'+str(total)+'-contract'])
                callput = request.POST['form-'+str(total)+'-callput'] 
                strike = int(request.POST['form-'+str(total)+'-strike'])
                days_to_exp = request.POST['form-'+str(total)+'-expiry_date']
                volatility = float(request.POST['form-'+str(total)+'-volatility'])
                

                startdate_object = datetime.strptime(start_date, '%d/%m/%Y').date()
                expdate_object = datetime.strptime(days_to_exp, '%m/%d/%Y').date()

                daystoexp = (expdate_object - startdate_object).days

                if callput == 'call':
                    callput_flag = 'c'
                elif callput == 'put':
                    callput_flag = 'p'
                else:
                    callput_flag = 's'
                

                time = (daystoexp - days_from_today)/365
                # print(formset[-1])

                if callput_flag == 's':
                    premium = stock_price
                else:
                    premium = BlackScholes(callput_flag, stock_price, strike, time, risk_free_rate, volatility)
                
                dbc = premium*contract*100

                context['buysell'] = buysell
                context['expiry'] = days_to_exp
                context['contract'] = contract
                context['callput'] = callput
                context['volatility'] = volatility
                context['premium'] = premium
                context['debit_credit'] = dbc
                context['strike'] = strike1
                # frm1 = OptionStrategyPositionDupFormSet(form_kwargs={"dates":((a,a) for a in exp_date)})
                # context['formsets'] = formset
                # return redirect('getCalc')
                return render(request,  'calculator.html', context) 
        
    else:

            formset = OptionStrategyPositionDupFormSet(form_kwargs={"dates":((a,a) for a in exp_date)})
        
            context['formsets'] = formset
        
    return render(request, 'calculator.html', context)  

def getEmptyForm(request):
    context2 = {}
    exp = request.session.get('exp')

    frm1 = OptionStrategyPositionDupFormSet(form_kwargs={"dates":((a,a) for a in exp)})

    strike1 = request.session.get('strike')  
    dictt = request.session.get('dictt') 
    dta = request.session.get('dta')

    context2['form1'] = frm1
    context2['strike'] = json.dumps(dta)
    return render(request, 'calculator.html', context2)