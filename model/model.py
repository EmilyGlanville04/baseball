import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph=nx.Graph()
        self._idMapSquadre={}
        self._idMapSalario = {}

    def getAllYears(self):
        return DAO.getAllYears()

    def getTeamsByYear(self,year):
        return DAO.getAllTeamsByYear(year)

    def buildGraph(self,year):
        self._graph.clear()
        self._idMapSquadre.clear()
        self._idMapSalario.clear()
        squadre = DAO.getAllTeamsByYear(year)
        for s in squadre:
            self._idMapSquadre[s.ID]=s
        self._graph.add_nodes_from(squadre)
        self._idMapSalario = DAO.getSalariesByTeam(year, self._idMapSquadre)
        for i in range(len(squadre)):
            for j in range(i+1,len(squadre)):
                nodoA=squadre[i]
                nodoB = squadre[j]
                pesoA = self._idMapSalario.get(nodoA,0)
                pesoB=self._idMapSalario.get(nodoB,0)
                peso = pesoA +pesoB
                self._graph.add_edge(nodoA,nodoB,weight=peso)

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getVicini(self,nodo):
        risultati = []
        for nodoA, nodoB, dati in self._graph.edges(nodo, data=True):
            risultati.append((nodoB, dati["weight"]))
        risultati.sort(key=lambda x: x[1], reverse=True)
        return risultati

    def getSquadraById(self, idSquadra):
        return self._idMapSquadre[int(idSquadra)]

    def trovaCammino(self,nodoStart):
        self._best_cammino = []
        self._best_peso =0
        cammino_parziale = [nodoStart]
        self.ricorsione(cammino_parziale,0, float("inf"))
        return self._best_cammino, self._best_peso

    def ricorsione(self,parziale,peso_attuale,peso_precedente):
        ultimo = parziale[-1]
        if peso_attuale>self._best_peso:
            self._best_peso=peso_attuale
            self._best_cammino=parziale.copy()
        for vicino in self._graph.neighbors(ultimo):
            if vicino not in parziale:
                peso_arco = self._graph[ultimo][vicino]["weight"]
                if peso_arco < peso_precedente:
                    parziale.append(vicino)
                    self.ricorsione(parziale,peso_attuale+peso_arco,peso_arco)
                parziale.pop()


