import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._idMap = {}
        self._solBest = []
        self._scoreBest = 0
        self._componenteConnessaMax = []

    def getPath(self, k, m, y1, y2):
        self._solBest=[]
        self._scoreBest = 0
        parziale = []
        self._ricorsione(parziale,k,m, y1, y2)


    def _ricorsione(self, parziale, k, m, y1, y2):
        if len(parziale) == k:
            if self._calcolaImprevisti(parziale) > self._scoreBest:
                self._solBest = copy.deepcopy(parziale)

        for c in self._componenteConnessaMax:
            if self._stepIsValid(c, m ,y1, y2):
                parziale.append(c)
                self._ricorsione(parziale, k, m, y1, y2)
                parziale.pop()


    def _calcolaImprevisti(self, parziale):
        pass

    def _stepIsValid(self, c, m, y1, y2):
        # Verifico che il costruttore c abbia partecipato ad almeno m campionati nel range tra year1 e year2
        i = 0
        for y in range(int(y1), int(y2) + 1):
            # Se l'anno y è chiave del dizionario result del costruttore, allora incremento i di 1
            if y in c.result:
                i += 1

        if i>=m:
            return True

        return False

    def buildGraph(self, year1, year2):
        self._graph.clear()
        self._idMap = {}
        nodes = DAO.getAllConstructors()
        for node in nodes:
            node.result = {}  # <--- SVUOTA il dizionario per sicurezza prima di ripopolarlo
            self._idMap[node.constructorId] = node
        self._graph.add_nodes_from(nodes)
        DAO.getPiazzamenti(self._idMap, year1, year2)
        self._addEdges(year1, year2)


    def _addEdges(self, year1, year2):
        archi = DAO.getAllEdges(self._idMap, year1, year2)
        for a in archi:
            for y in range(int(year1), int(year2) + 1):

                # Potrebbe, quel costruttore, non aver corso nell'anno corrente
                # Gestione per il costruttore 1
                if y in a.c1.result:
                    a.peso += len(a.c1.result[y])
                else:
                    a.peso += 0  # Non ha corso in questo anno, aggiungi zero

                # Gestione per il costruttore 2
                if y in a.c2.result:
                    a.peso += len(a.c2.result[y])
                else:
                    a.peso += 0
            self._graph.add_edge(a.c1, a.c2, weight=a.peso)

    def getAllYears(self):
        years = DAO.getAllYears()
        return years

    def getNumNodesEdges(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getGraphDetails(self):
        # Genera una lista di componenti connesse
        componenteConnessa = nx.connected_components(self._graph)

        # Trovo la componente connessa piu luna (key=len)
        self._componenteConnessaMax = max(componenteConnessa, key=len)

        # Creo una lista di tuple (nodo, peso_massimo)
        nodi_con_peso = []
        for nodo in self._componenteConnessaMax:
            # Trovo il peso massimo degli archi incidenti su questo nodo
            archi_incidenti = self._graph.edges(nodo, data=True)

            if archi_incidenti:
                # Estraggo il valore del 'weight' da ogni arco incidente e prendo il massimo
                max_peso = max([dati['weight'] for u, v, dati in archi_incidenti])
            else:
                max_peso = 0

            nodi_con_peso.append((nodo, max_peso))

        # Ordino in senso decrescente in base al peso massimo (x[1])
        nodi_con_peso.sort(key=lambda x: x[1], reverse=True)
        return nodi_con_peso

