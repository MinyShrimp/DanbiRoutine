
from datetime import timedelta
from django.utils.timezone import now

day_convertor_key   = { "MON": 0, "TUE": 1, "WED": 2, "THU": 3, "FRI": 4, "SAT": 5, "SUN": 6 }
day_convertor_value = { 0: "MON", 1: "TUE", 2: "WED", 3: "THU", 4: "FRI", 5: "SAT", 6: "SUN" }

def DateConvertor(_days):
    global day_convertor_key
    _now, result  = now(), []
    today         = _now.weekday()

    for day in _days:
        weekday = day_convertor_key[day]
        output  = ( weekday - today ) if weekday >= today else ( 7 - ( today - weekday ) )
        result.append( ( _now + timedelta(days = output) ).date() )

    return result

def DateSort(_days ):
    global day_convertor_key
    result = [ { "title": value, "value": day_convertor_key[value] } for value in _days ]

    result = sorted( result, key=lambda x: x["value"] )
    return [ _["title"] for _ in result ]