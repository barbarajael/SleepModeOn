from django.http import HttpResponse, HttpRequest
from datetime import datetime, timedelta
import datetime

from django.template import loader

from app.graph_py.grafo import Graph
from app.graph_py.RegrasInferencia import Inf1, Inf3


# ------------- MENU / GRAPH -------------

_graph = Graph()
_graph.load("app/graph_py/sleepdata_triples.csv")


def totalsleep():
    lista = _graph.query([('?suj', 'time_in_bed', '?time')])
    tempos = []

    for dic in lista:
        tempos.append(dic['time'])

    return tempos


def time_feel(feel):
    lista = _graph.query([('?suj', 'feeling', feel), ('?suj', 'time_in_bed', '?time')])
    tempos = []

    for dic in lista:
        tempos.append(dic['time'])

    return tempos



# ------------- HELPERS -------------


def makeAverage(tempos):
    return str(
        timedelta(
            seconds=sum(
                map(lambda f: int(f[0]) * 3600 + int(f[1]) * 60, map(lambda f: f.split(':'), tempos))
            ) / len(tempos)
        )
    )


def timeToSleep(hour):
    hourTH = hour.split(':')
    lista = _graph.query([('?suj', 'feeling', ':)'), ('?suj', 'time_in_bed', '?time')])
    timesHappy = []

    for dic in lista:
        timesHappy.append(dic['time'])

    minTimeHappy = min(timesHappy)  # 0:46
    minTH = minTimeHappy.split(':')
    maxTimeHappy = max(timesHappy)  # 9:31
    maxTH = maxTimeHappy.split(':')

    hour_min = int(hourTH[0]) - int(minTH[0])
    minutes_min = int(hourTH[1]) - int(minTH[1])
    tmin = str(datetime.timedelta(hours=hour_min, minutes=minutes_min))

    hour_max = int(hourTH[0]) - int(maxTH[0])
    minutes_max = int(hourTH[1]) - int(maxTH[1])
    tmax = str(datetime.timedelta(hours=hour_max, minutes=minutes_max))

    return [tmin, tmax]



# ------------- VIEW -------------

def dataSleep(request):
    assert isinstance(request, HttpRequest)
    template = loader.get_template('index.html')

    # ------------------------------------------

    # ------- total average -------

    timeAll = totalsleep()
    avgTime = makeAverage(timeAll)
    avgTime = avgTime.rsplit(':', 1)


    # ------- average happy -------

    timeHappy = time_feel(':)')
    avgHappyTime = makeAverage(timeHappy)
    avgHappyTime = avgHappyTime.rsplit(':', 1)


    # ------- average meh -------

    timeMeh = time_feel(':|')
    avgMehTime = makeAverage(timeMeh)
    avgMehTime = avgMehTime.rsplit(':', 1)


    # ------- average sad -------

    timeSad = time_feel(':(')
    avgSadTime = makeAverage(timeSad)
    avgSadTime = avgSadTime.rsplit(':', 1)


    # ------------------------------------------


    # ------- inference1 (good sleep) -------

    binds = _graph.applyinference(Inf1())
    sujs = []
    timesbed = []
    for b in binds:
        sujs.append(b['suj'])

    for s in sujs:
        q = _graph.query([(s, 'time_in_bed', '?time')])
        for a in q:
            timesbed.append(a['time'])

    timesGoodSleep = str(timesbed)\
        .replace('[', '')\
        .replace(']', '')\
        .replace('\'', '')


    # ------- inference3 (best heart rate) -------

    binds = _graph.applyinference(Inf3())
    sujs = []
    timesbed = []
    beatbed = []

    for b in binds:
        sujs.append(b['suj'])

    for s in sujs:
        q = _graph.query([(s, 'time_in_bed', '?time')])
        for a in q:
            timesbed.append(a['time'])

    for s in sujs:
        q = _graph.query([(s, 'heart_rate', '?beat')])
        for a in q:
            beatbed = a['beat']
            break

    timesGoodRate = str(timesbed) \
        .replace('[', '') \
        .replace(']', '') \
        .replace('\'', '')


    # ------------------------------------------


    return HttpResponse(template.render({
            'avgTime': avgTime[0],
            'avgHappyTime': avgHappyTime[0],
            'avgMehTime': avgMehTime[0],
            'avgSadTime': avgSadTime[0],
            'min_whenSleep': '_____',
            'max_whenSleep': '_____',
            'timesGoodSleep': timesGoodSleep,
            'beatbed': beatbed,
            'timesGoodRate': timesGoodRate
        }, request))




def calcTimesSleep(request):
    assert isinstance(request, HttpRequest)
    template = loader.get_template('index.html')

    hours = request.POST.get('horas_drop')
    minutes = request.POST.get('minutos_drop')
    whenSleep = timeToSleep(str(hours) + ':' + str(minutes))
    # whenSleep = timeToSleep('9:31')
    min_whenSleep = whenSleep[0]
    max_whenSleep = whenSleep[1]