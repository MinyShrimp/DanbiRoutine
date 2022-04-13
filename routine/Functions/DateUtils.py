
from datetime import timedelta, datetime
from django.utils.timezone import now

day_convertor_key   = { "MON": 0, "TUE": 1, "WED": 2, "THU": 3, "FRI": 4, "SAT": 5, "SUN": 6 }
day_convertor_value = { 0: "MON", 1: "TUE", 2: "WED", 3: "THU", 4: "FRI", 5: "SAT", 6: "SUN" }

def getDateTimeMon() -> datetime:
    _now   = now()
    today  = _now.weekday()
    result = _now - timedelta( days = today )
    return datetime( result.year, result.month, result.day, 0, 0, 0, 0 )

def getDateTimeSun() -> datetime:
    _now   = now()
    today  = _now.weekday()
    result = _now + timedelta( days = 7 - today - 1 )
    return datetime( result.year, result.month, result.day, 0, 0, 0, 0 )

def getDateTimeByDay( day ):
    return getDateTimeMon() + timedelta( days = day_convertor_key[day] )

def DateConvertor( _days ):
    global day_convertor_key
    result, start = [], getDateTimeMon()

    for day in _days:
        weekday = day_convertor_key[day]
        output  = start + timedelta( days = weekday )
        result.append( output.date() )

    return result

def DateSort( _days ):
    global day_convertor_key
    result = [ { "title": value, "value": day_convertor_key[value] } for value in _days ]

    result = sorted( result, key=lambda x: x["value"] )
    return [ _["title"] for _ in result ]

def DateConvertorToDate( _days ):
    global day_convertor_value
    return DateSort( [ day_convertor_value[day.day.weekday()] for day in _days ] )