import csv


# Grafo sujeito - predicado - objeto
class Graph:

    # Estrutura de dados definida: listas
    def __init__(self):
        self._spo = []
        self._pos = []
        self._osp = []

    # Adiciona permutações do triplo à lista correspondente
    def add(self, suj, pred, obj):
        self._addToIndex(self._spo, suj, pred, obj)
        self._addToIndex(self._pos, pred, obj, suj)
        self._addToIndex(self._osp, obj, suj, pred)

    # Adiciona o triplo à lista fornecida
    def _addToIndex(self, index, a, b, c):
        aPos = self.searchAPos(index, a)                # Triplos da lista cujo primeiro termo é "a"
        if aPos is None:
            index.append([a, [b, [c]]])
        else:
            bPos = self.searchBPos(index, b, aPos)      # Triplos, da lista de triplos com primeiro termo "a", com segundo termo "b"
            if bPos is None:
                index[aPos].append([b, [c]])
            else:
                index[aPos][bPos][1].append(c)

    # Devolve os triplos da lista cujo primeiro termo é "a"
    def searchAPos(self, list, a):
        if list is None:
            return None
        if a is not None:
            for pos, val in enumerate(list):
                if str(val[0]) == str(a):
                    return pos

    # Devolve os triplos, da lista cujo primeiro termo é "a" (aPos), com segundo termo "b"
    def searchBPos(self, list, b, aPos):
        if list is None:
            return None
        if b is not None:
            for pos, val in enumerate(list[aPos]):
                if str(val[0]) == str(b) and not type(val) is str:
                    return pos

    # Remove todas as permutações do triplo da lista correspondente
    def remove(self, suj, pred, obj):
        triples = list(self.triples(suj, pred, obj))                # Pesquisa pelos triplos com o padrão fornecido
        for (delSuj, delPred, delObj) in triples:
            self._removeFromIndex(self._spo, delSuj, delPred, delObj)
            self._removeFromIndex(self._pos, delPred, delObj, delSuj)
            self._removeFromIndex(self._osp, delObj, delSuj, delPred)

    # Remove o triplo de uma dada lista
    def _removeFromIndex(self, index, a, b, c):
        try:
            aPos = self.searchAPos(index, a)
            bPos = self.searchBPos(index, b, aPos)                   # Na lista de triplos obtida, procura os triplos com segundo termo "b"
            for pos, val in enumerate(index[aPos][bPos]):
                if type(val) is not str:
                    for pos2, val2 in enumerate(val):
                        if val2 == c:
                            del index[aPos][bPos][pos][pos2]
            if len(index[aPos][bPos][1]) == 0:
                del index[aPos][bPos]
            if len(index[aPos]) == 1:
                del index[aPos]
        except KeyError:
            pass

    # Pesquisa um triplo
    def triples(self, suj, pred, obj):
        try:
            if suj != None:
                if pred != None:
                    # suj pred obj
                    if obj != None:
                        sujPos = self.searchAPos(self._spo, suj)
                        if sujPos is not None:
                            predPos = self.searchBPos(self._spo, pred, sujPos)
                            if predPos is not None:
                                if obj in self._spo[sujPos][predPos][1]:
                                    yield (suj, pred, obj)
                                else:
                                    print("O objeto pretendido não existe")
                            else:
                                print("O predicado pretendido não existe")
                        else:
                            print("O sujeito pretendido não existe")
                    # suj pred None
                    else:
                        sujPos = self.searchAPos(self._spo, suj)
                        if sujPos is not None:
                            predPos = self.searchBPos(self._spo, pred, sujPos)
                            if predPos is not None:
                                for retObj in self._spo[sujPos][predPos][1]:
                                    yield (suj, pred, retObj)
                            else:
                                print("O predicado pretendido não existe")
                        else:
                            print("O sujeito pretendido não existe")
                else:
                    # suj None obj
                    if obj != None:
                        objPos = self.searchAPos(self._osp, obj)
                        if objPos is not None:
                            sujPos = self.searchBPos(self._osp, suj, objPos)
                            if sujPos is not None:
                                for retPred in self._osp[objPos][sujPos]:
                                    if type(retPred) is not str:
                                        for pred in retPred:
                                            yield (suj, pred, obj)
                            else:
                                print("O sujeito pretendido não existe")
                        else:
                            print("O objeto pretendido não existe")
                    # suj None None
                    else:
                        sujPos = self.searchAPos(self._spo, suj)
                        listAux = []                                            # Lista auxiliar para guardar predicados e objetos
                        if sujPos is not None:
                            for item in self._spo[sujPos]:                          # Percorremos os triplos com primeiro termo "suj"
                                if type(item) is not str:
                                    listAux.append((item[0], item[1]))
                            for retPred, objSet in listAux:                         # Para cada predicado com sujeito "suj",
                                for retObj in objSet:                               # Vamos percorrer os objetos
                                    yield (suj, retPred, retObj)
                        else:
                            print("O sujeito pretendido não existe")
            else:
                if pred != None:
                # None pred obj
                    if obj != None:
                        predPos = self.searchAPos(self._pos, pred)
                        if predPos is not None:
                            objPos = self.searchBPos(self._pos, obj, predPos)
                            if objPos is not None:
                                for retSuj in self._pos[predPos][objPos]:
                                    if type(retSuj) is not str:
                                        for item in retSuj:
                                            yield (item, pred, obj)
                            else:
                                print("O objeto pretendido não existe")
                        else:
                            print("O predicado pretendido não existe")
                    # None pred None
                    else:
                        predPos = self.searchAPos(self._pos, pred)
                        listAux = []                                            # Lista auxiliar para guardar sujeitos e objetos
                        if predPos is not None:
                            for item in self._pos[predPos]:
                                if type(item) is not str:
                                    listAux.append((item[0], item[1]))
                            for retObj, sujSet in listAux:                          # Percorre os objetos do conjunto de sujeitos obtidos
                                for retSuj in sujSet:
                                    yield (retSuj, pred, retObj)
                        else:
                            print("O predicado pretendido não existe")
                else:
                    # None None obj
                    if obj != None:
                        objPos = self.searchAPos(self._osp, obj)
                        listAux = []                                            # Lista auxiliar para guardar sujeitos e predicados
                        if objPos is not None:
                            for item in self._osp[objPos]:
                                if type(item) is not str:
                                    listAux.append((item[0], item[1]))
                            for retSuj, predSet in listAux:                         # Retem o sujeito e percorre a sua lista de predicados
                                for retPred in predSet:
                                    yield (retSuj, retPred, obj)
                        else:
                            print("O objeto pretendido não existe")
                    # None None None
                    else:
                        listAux = []
                        varAux = None
                        for item in self._spo:
                            if type(item) is not str:
                                for po in item:                                 # Subconjunto de predicados e objetos
                                    if type(po) is not str:
                                        listAux.append((varAux, po))
                                    else:
                                        varAux = po
                        for retSuj, predSet in listAux:                         # Retem o sujeito e percorre todos os seus predicados
                            varAux2 = None
                            for pred in predSet:
                                if type(pred) is not str:
                                    for obj in pred:                            # Percorre os objetos de cada predicado
                                        yield (retSuj, varAux2, obj)
                                else:
                                    varAux2 = pred
        except KeyError:
            pass

    # Lê cada linha (triplo) do ficheiro csv e guarda as permutações no grafo
    def load(self, filename):
        file = open(filename, "r", encoding="utf-8")
        reader = csv.reader(file)
        for suj, pred, obj in reader:
            self.add(suj, pred, obj)
        file.close()

    # Guarda os triplos do grafo em mémoria num ficheiro csv
    def save(self, filename):
        file = open(filename, "w", encoding="utf-8", newline='')
        writer = csv.writer(file)
        for suj, pred, obj in self.triples(None, None, None):
            writer.writerow([suj, pred, obj])
        file.close()

    # Imprime todos os triplos
    def printAllTriples(self):
        triple = self.triples(None, None, None)
        Graph.printTriples(triple)

    # Imprime um triplo individual
    @staticmethod
    def printTriples(triple):
        for suj, pred, obj in triple:
            print("("+str(suj)+", "+str(pred)+", "+str(obj)+")")

    # Lista de triplos resultantes de query
    def query(self, clauses):
        outputs = None
        for clause in clauses:
            positions = {}                              # Associa a variável à sua posição no triplo (dicionário)
            input = []                                  # Elementos de input ao método triples (lista)
            for pos, val in enumerate(clause):
                if val.startswith('?'):
                    input.append(None)
                    positions[val[1:]] = pos
                else:
                    input.append(val)

            rows = list(self.triples(input[0], input[1], input[2]))

            if outputs == None:
                outputs = []
                for row in rows:
                    output = {}
                    for var, pos in positions.items():
                        output[var] = row[pos]
                    outputs.append(output)

            else:
                new_output = []
                for output in outputs:
                    for row in rows:
                        validmatch = True
                        temp_output = output.copy()
                        for var, pos in positions.items():
                            if var in temp_output:
                                if temp_output[var] != row[pos]:
                                    validmatch = False
                            else:
                                temp_output[var] = row[pos]
                        if validmatch:
                            new_output.append(temp_output)
                outputs = new_output
        return outputs


    # Aplica uma dada inferência ao grafo
    def applyinference(self, rule):
        queries = rule.getqueries()
        outputs = []
        for query in queries:
            outputs += self.query(query)
        for pos in outputs:
            new_triples = rule.maketriples(pos)
            for suj, pred, obj in new_triples:
                self.add(suj, pred, obj)

        return outputs


    # Transformação do grafo para formato DOT
    def triples2dot(self, triples):
        dot = \
    """
    graph "SimpleGraph" {
    overlap = "scale";
    """
        for s, p, o in triples:
            dot = dot + ('"%s" -- "%s" [label="%s"]\n' % (s, o, p))
        dot = dot + "}"
        return dot
