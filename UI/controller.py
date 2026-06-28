import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choiceTeam = None


    def handleCreaGrafo(self, e):
        self._view._txt_result.controls.clear()
        anno = self._view._ddAnno.value
        if anno is None:
            self._view.create_alert("Selezionare un anno")
            return
        self._model.buildGraph(anno)
        n,m = self._model.getGraphDetails()
        self._view._txt_result.controls.append(ft.Text(f"Grafo correttamente creato con {n} nodi e {m} archi"))
        self._view.update_page()


    def handleDettagli(self, e):
        self._view._txt_result.controls.clear()
        idSquadra = self._view._ddSquadra.value
        if idSquadra is None:
            self._view.create_alert("Selezionare una squadra")
            return
        nodo = self._model.getSquadraById(idSquadra)
        vicini = self._model.getVicini(nodo)
        self._view._txt_result.controls.append(ft.Text(f"Stampo i vicini di {nodo.name} con i relativi pesi"))
        for nodoB, peso in vicini:
            self._view._txt_result.controls.append(ft.Text(f"{nodoB.name} ---> {peso}"))
        self._view.update_page()


    def handlePercorso(self, e):
        self._view._txt_result.controls.clear()
        idSquadra = self._view._ddSquadra.value
        if idSquadra is None:
            self._view.create_alert("Selezionare una squadra")
            return
        nodoStart = self._model.getSquadraById(idSquadra)
        cammino, pesoTot = self._model.trovaCammino(nodoStart)
        self._view._txt_result.controls.append(
            ft.Text(f"Percorso migliore da {nodoStart}:")
        )
        for i in range(len(cammino) - 1):
            peso = self._model._graph[cammino[i]][cammino[i + 1]]["weight"]
            self._view._txt_result.controls.append(
                ft.Text(f"{cammino[i]} -> {cammino[i + 1]} | peso: {peso}")
            )
        self._view._txt_result.controls.append(
            ft.Text(f"Peso totale: {pesoTot}")
        )
        self._view.update_page()


    def fillDdAnno(self):
        anni = self._model.getAllYears()
        for a in anni:
            self._view._ddAnno.options.append(ft.dropdown.Option(a))
        self._view.update_page()


    def handleYearSelection(self,e):
        self._view._txtOutSquadre.controls.clear()
        year = self._view._ddAnno.value
        squadre = self._model.getTeamsByYear(year)
        self._view._txtOutSquadre.controls.clear()
        self._view._txtOutSquadre.controls.append(ft.Text(f"Ho trovato {len(squadre)} che hanno giocato nel {year}"))
        for s in squadre:
            self._view._txtOutSquadre.controls.append(ft.Text(str(s)))
        for s in squadre:
            self._view._ddSquadra.options.append(ft.dropdown.Option(key=str(s.ID), text=s.teamCode))
        self._view.update_page()



