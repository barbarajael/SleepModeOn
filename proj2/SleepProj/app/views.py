from django.http import HttpResponse, HttpRequest
from datetime import datetime, timedelta
import datetime
from django.template import loader
import os

# RDF Graphi
from rdflib import ConjunctiveGraph, Namespace


# -------------------------------
# ------------ GRAPH ------------
# -------------------------------

filePath = os.path.join(os.path.dirname(__file__), "graph_py", "sleepdata_rdf.nt");
_graph = ConjunctiveGraph()
_graph.parse(filePath, format="nt")


def totalsleep():
    tempos = []

    totaltime = _graph.query(
        """ prefix pred: <http://sleepdata.com/predicate/>
        select ?time where { ?s pred:time_in_bed ?time. } """)
    for t in totaltime:
        st = str(t)
        tempos.append(st.replace("rdflib.term.Literal", "").replace("(", "").replace(")", "")
                      .replace("',", "'").replace("'", ""))

    return tempos


def time_feel(feel):
    tempos = []

    totaltime = _graph.query(
        """ prefix pred: <http://sleepdata.com/predicate/>
        select ?time where { ?s pred:feeling \"""" + feel + """\" ; pred:time_in_bed ?time. } """)
    for t in totaltime:
        st = str(t)
        tempos.append(st.replace("rdflib.term.Literal", "").replace("(", "").replace(")", "")
                      .replace("',", "'").replace("'", ""))

    return tempos


# -----------------------------------
# ------------- HELPERS -------------
# -----------------------------------


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

    minTimeHappy = _graph.query(
        """ prefix pred: <http://sleepdata.com/predicate/>
        select (min(?time) as ?minTime) where { ?s pred:feeling \":)\" ; pred:time_in_bed ?time. } """)
    
    maxTimeHappy = _graph.query(
        """ prefix pred: <http://sleepdata.com/predicate/>
        select (max(?time) as ?maxTime) where { ?s pred:feeling \":)\" ; pred:time_in_bed ?time. } """)

    for t in minTimeHappy:
        st = str(t).replace("rdflib.term.Literal", "").replace("(", "").replace(")", "").replace(",", "").replace("'", "")
        minTH = st.split(':')

    for t in maxTimeHappy:
        st = str(t).replace("rdflib.term.Literal", "").replace("(", "").replace(")", "").replace(",", "").replace("'", "")
        maxTH = st.split(':')

    hour_min = int(hourTH[0]) - int(minTH[0])
    minutes_min = int(hourTH[1]) - int(minTH[1])
    tmin = str(datetime.timedelta(hours=hour_min, minutes=minutes_min))

    hour_max = int(hourTH[0]) - int(maxTH[0])
    minutes_max = int(hourTH[1]) - int(maxTH[1])
    tmax = str(datetime.timedelta(hours=hour_max, minutes=minutes_max))

    return [tmin, tmax]



# --------------------------------
# ------------- VIEW -------------
# --------------------------------


def dataSleep(request):
    assert isinstance(request, HttpRequest)
    template = loader.get_template('index.html')

    # --------------------------------------------------


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


    # --------------------------------------------------

    # ------- inference1 (good sleep) -------

    sujs = []
    timesbed = []

    # inferencia em si
    binds = _graph.query(
        """ prefix pred: <http://sleepdata.com/predicate/>
        construct { ?s pred:result "Good Sleep Quality!" }
        where { ?s pred:quality "100%" } """)

    # resultado da inferencia e remocao dos termos do sparql result para fazer string
    for t in binds:
        st = str(t).replace("(rdflib.term.URIRef(", "").replace("rdflib.term.URIRef(", "")\
            .replace("rdflib.term.Literal(", "").replace("'),", "").replace("'))", "").replace("'", "")

        # adicionar apenas sujeito na lista, com formato <subj> como sera necessario
        stsplit = st.split(" ")
        sujs.append("<" + stsplit[0] + ">")

    # ir buscar o tempo dos sujeitos acima (ou seja, dos sujeitos com bom sono)
    for s in sujs:
        q = _graph.query(
            """ prefix pred: <http://sleepdata.com/predicate/>
            select ?time
            where { """ + s + """ pred:time_in_bed ?time } """)

        # adicionar tempos na lista
        #       com remocao dos termos do sparql result para fazer string
        #       sem duplicados
        for t in q:
            myTime = str(t).replace("(rdflib.term.Literal('", "").replace("'),)", "")

            if myTime not in timesbed:
                timesbed.append(myTime)

    # construir string para aparecer no site a lista de tempos
    timesGoodSleep = str(timesbed)\
        .replace('[', '')\
        .replace(']', '')\
        .replace('\'', '')


    # ------- inference3 (best heart rate) -------

    sujs = []
    timesbed = []
    beatbed = []

    # inferencia em si
    binds = _graph.query(
        """ prefix pred: <http://sleepdata.com/predicate/>
        construct { ?s pred:result "Ideal Heart Rate" }
        where { ?s pred:heart_rate "55" } """)

    # resultado da inferencia e remocao dos termos do sparql result para fazer string
    for t in binds:
        st = str(t).replace("(rdflib.term.URIRef(", "").replace("rdflib.term.URIRef(", "")\
            .replace("rdflib.term.Literal(", "").replace("'),", "").replace("'))", "").replace("'", "")

        stsplit = st.split(" ")
        sujs.append("<" + stsplit[0] + ">")

    for s in sujs:
        # ir buscar o tempo dos sujeitos acima (ou seja, dos sujeitos com bom heartrate)
        q1 = _graph.query(
            """ prefix pred: <http://sleepdata.com/predicate/>
            select ?time
            where { """ + s + """ pred:time_in_bed ?time } """)

        # adicionar tempos na lista
        #       com remocao dos termos do sparql result para fazer string
        #       sem duplicados
        for t in q1:
            myTime = str(t).replace("(rdflib.term.Literal('", "").replace("'),)", "")

            if myTime not in timesbed:
                timesbed.append(myTime)


        # ir buscar o heartrate considerado bom, para aparecer no site o heartrate
        q2 = _graph.query(
            """ prefix pred: <http://sleepdata.com/predicate/>
            select ?beat
            where { """ + s + """ pred:heart_rate ?beat } """)

        # adicionar um dos bons heartrates (basta um, sao iguais)
        for t in q2:
            beatbed = str(t).replace("(rdflib.term.Literal('", "").replace("'),)", "")
        

    # construir string para aparecer no site a lista de tempos
    timesGoodRate = str(timesbed) \
        .replace('[', '') \
        .replace(']', '') \
        .replace('\'', '')




    # --------------------------------------------------


    # ------- form things (calc) -------

    min_whenSleep = '_____'
    max_whenSleep = '_____'

    if 'horas_drop' in request.POST and 'minutos_drop' in request.POST:
        hours = request.POST.get('horas_drop')
        minutes = request.POST.get('minutos_drop')

        whenSleep = timeToSleep(str(hours) + ':' + str(minutes))

        min_whenSleep = whenSleep[0][:-3]
        max_whenSleep = whenSleep[1][:-3]

        if 'day' in min_whenSleep:
            min_whenSleep = min_whenSleep[8:]
        if 'day' in max_whenSleep:
            max_whenSleep = max_whenSleep[8:]

        if min_whenSleep < max_whenSleep:
            tmp1 = min_whenSleep
            tmp2 = max_whenSleep

            min_whenSleep = tmp2
            max_whenSleep = tmp1


    # --------------------------------------------------


    return HttpResponse(template.render({
            'avgTime': avgTime[0],
            'avgHappyTime': avgHappyTime[0],
            'avgMehTime': avgMehTime[0],
            'avgSadTime': avgSadTime[0],

            'timesGoodSleep': timesGoodSleep,
            'beatbed': beatbed,
            'timesGoodRate': timesGoodRate,

            'min_whenSleep': min_whenSleep,
            'max_whenSleep': max_whenSleep
        }, request))
