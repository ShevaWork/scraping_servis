import requests
import json

site_status = "http://172.18.96.90/ODJET_CGI?ppsw=status"
site_values = "http://172.18.96.90/ODJET_CGI?pread=all"

r_status = requests.get(site_status).text
r_values = requests.get(site_values).text

js_text_status = json.loads(r_status)
js_text_values = json.loads(r_values)

# lists
temperature = {'Room temp': '2009',
               'On delta C1': '2958',
               'On delta C2': '2959',
               'Off delta C1': '3007',
               'Off delta C2': '3008',
               'Setpoint C1': '3011',
               'Setpoint C2': '3012'}
condition = {'Enable email': '2957',
             'State C1': '3003',
             'State C2': '3004',
             'Manual mode': '3005',
             'Off delay C1': '3009',
             'Off delay C2': '3010',
             'Start delay C1': '3013',
             'Start delay C2': '3014',
             'Work mode': '3027'}
rotation = {'Hours in work C1': '2100',
            'Worked hours C1': '2102',
            'Hours in work C2': '2103',
            'Worked hours C2': '2105',
            'Rotation mode': '3006',
            'Hours diff': '3026',
            'Rotation day': '3028',
            'Rotation time': '3029'}
alarms = {'Num1': '6500',
          'Num2': '6501',
          'Num3': '6502',
          'Num4': '6503',
          'Num5': '6504'}


def unlock(jstext_status):
    for array in jstext_status['tab_system']:
        return array['ppsw']


def universal_param(jstext_values, name, id_param):
    for item in jstext_values['tab_param']:
        if item['addr'] == id_param:
            text = name + ' : ' + item['value']
            return text


def getlist(jstext_values, listik):
    text = ''
    for i in listik:
        text += universal_param(jstext_values, i, listik[i]) + '\n'
    return text





def getTemperature():
    status_list = json.loads(requests.get(site_status).text)
    value_list = json.loads(requests.get(site_values).text)
    if unlock(status_list) == "unlock":
        return getlist(value_list, temperature)
    else:
        return "Не вдалось встановити зв'язок"


def getCondition():
    status_list = json.loads(requests.get(site_status).text)
    value_list = json.loads(requests.get(site_values).text)
    if unlock(status_list) == "unlock":
        return getlist(value_list, condition)
    else:
        return "Не вдалось встановити зв'язок"


def getRotation():
    status_list = json.loads(requests.get(site_status).text)
    value_list = json.loads(requests.get(site_values).text)
    if unlock(status_list) == "unlock":
        return getlist(value_list, rotation)
    else:
        return "Не вдалось встановити зв'язок"


def getAlarams():
    status_list = json.loads(requests.get(site_status).text)
    value_list = json.loads(requests.get(site_values).text)
    if unlock(status_list) == "unlock":
        return getlist(value_list, alarms)
    else:
        return "Не вдалось встановити зв'язок"


# ID-LIBRARY
# id - Temperature
# 2009 - Room temp
# 2958 - On delta C1
# 2959 - On delta C2
# 3007 - Off delta C1
# 3008 - Off delta C2
# 3011 - Setpoint C1
# 3012 - Setpoint C2
##################################################################################################################
# id - Condition
# 2957 - Enable email
# 3003 - State C1
# 3004 - State C2
# 3005 - Manual mode
# 3009 - Off delay C1
# 3010 - Off delay C2
# 3013 - Start delay C1
# 3014 - Start delay C2
# 3027 - Work mode
##################################################################################################################
# id - Rotation
# 2100 - Hours in work C1
# 2102 - Worked hours C1
# 2103 - Hours in work C2
# 2105 - Worked hours C2
# 3006 - Rotation mode
# 3026 - Hours diff
# 3028 - Rotation day
# 3029 - Rotation time
# 3030 - Rotation time - no_display
##################################################################################################################
# id - Alarms
# 6500 - Num1
# 6501 - Num2
# 6502 - Num3
# 6503 - Num4
# 6504 - Num5ID
