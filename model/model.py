import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._idMapDrivers={}
        self._optListPiloti = None
        self._minDistAnni = None

    def getListaPilotiOttima(self, k):
        self._optListPiloti= []
        self._minDistAnni =100*365
        components= list(nx.connected_components(self._grafo))
        if len(components) < k:
            #non ho abbastanza componenti connesse da cui pescare e non posso trovare una soluzione
            return None, 0
        parziale = []
        self._ricorsione(components,k, parziale, 0)
        return self._optListPiloti, self._minDistAnni

    def _ricorsione(self, components, k, parziale, indexComponente):
        #cond ottimalità
        if len(parziale) == k:
            #solu accettabile
            dateNascita = [p.dob for p in parziale]
            distanza = (max(dateNascita)-min(dateNascita)).days
            if distanza < self._minDistAnni:
                self._optListPiloti= copy.deepcopy(parziale)
                self._minDistAnni= distanza
                return
        #terminazione-
        # indice è maggiore o = a numero di componenti connesse totali o se non ho abbastanza componenti da arrivare a k
        if indexComponente >= len(components) or (len(components) - indexComponente) < (k-len(parziale)):
            return
        #se non esco continuo aggiungo piloti
        componente = components[indexComponente]
        for pilota in componente:
            parziale.append(pilota)
            self._ricorsione(components, k,parziale , indexComponente+1)
            parziale.pop()
        self._ricorsione(components, k, parziale, indexComponente+1)











        pass



    def getAllYears(self):

        self._anni= DAO.getAllYears()
        return self._anni
    def buildGraph(self,anno1, anno2):
        self._grafo.clear()
        self._drivers= DAO.getAllNodes(anno1, anno2)
        self._grafo.add_nodes_from(self._drivers)
        for d in self._drivers:
            self._idMapDrivers[d.driverId]=d
        edges = DAO.getAllEdges(anno1, anno2, self._idMapDrivers)
        for e in edges:
            self._grafo.add_edge(e.d1, e.d2, weight=e.peso)

    def getNumNodes(self):
        return len(self._grafo.nodes)
    def getNumEdges(self):
        return len(self._grafo.edges)

    def getTop3Archi(self):
        archi= self._grafo.edges
        return sorted(archi(data=True), key=lambda x: x[2]["weight"], reverse=True)[:3]
    def getConnessaInfo(self):
        components = list(nx.connected_components(self._grafo))
        largest = max(components, key=len)
        subGrafo= self._grafo.subgraph(largest).copy()
        orderedNodes = sorted(subGrafo.nodes(), key=lambda n: self._grafo.degree(n), reverse=True)
        details = [(n, self._grafo.degree(n)) for n in orderedNodes]
        return len(components), largest,details



        



