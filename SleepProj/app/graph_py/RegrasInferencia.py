class InferenceRule:
    def getqueries(self):
        return None

    def maketriples(self, binding):
        return self._maketriples(**binding)


class Inf1(InferenceRule):
    def getqueries(self):
        qual = [('?suj', 'quality', '100%')]
        return [qual]

    def _maketriples(self, suj):
        return [(suj, 'result', 'Good Sleep Quality!')]


class Inf2(InferenceRule):
    def getqueries(self):
        sleep = [('?suj', 'time_in_bed', '8:00')]
        return [sleep]

    def _maketriples(self, suj):
        return [(suj, 'result', 'Ideal Time Sleeping')]


class Inf3(InferenceRule):
    def getqueries(self):
        heart = [('?suj', 'heart_rate', '55')]
        return [heart]

    def _maketriples(self, suj):
        return [(suj, 'result', 'Ideal Heart Rate')]


class Inf4(InferenceRule):
    def getqueries(self):
        feel = [('?suj', 'feeling', ':)')]
        return [feel]

    def _maketriples(self, suj):
        return [(suj, 'result', 'Good Rest Nigth!')]


class Inf5(InferenceRule):
    def getqueries(self):
        excelent = [('?suj', 'quality', '100%'), ('?suj', 'feeling', ':)')]
        return [excelent]

    def _maketriples(self, suj):
        return [(suj, 'result', 'Deep Rest')]
    