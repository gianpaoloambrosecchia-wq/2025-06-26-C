import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleBuildGraph(self, e):
        year1 = self._view._ddYear1.value
        year2 = self._view._ddYear2.value
        if year1 is None or year2 is None:
            self._view._txtGraphDetails.controls.clear()
            self._view._txtGraphDetails.controls.append(
                ft.Text("Seleziona due anni dai menu", color="red")
            )
            self._view.update_page()
            return
        if year1 > year2:
            self._view._txtGraphDetails.controls.clear()
            self._view._txtGraphDetails.controls.append(
                ft.Text("Il primo anno deve essere inferiore al secondo", color="red")
            )
            self._view.update_page()
            return

        self._model.buildGraph(year1,year2)
        self._view._txtGraphDetails.controls.clear()
        self._view._txtGraphDetails.controls.append(
            ft.Text("Grafo correttamente creato", color="green")
        )
        self._view._btnPrintDetails.disabled = False
        numNodes, numEdges = self._model.getNumNodesEdges()
        self._view._txtGraphDetails.controls.append(
            ft.Text(f"Il grafo ha {numNodes} nodi e {numEdges} archi")
        )
        self._view.update_page()


    def handlePrintDetails(self, e):
        largest_cc = self._model.getGraphDetails()
        for nodo, peso in largest_cc:
            self._view._txtGraphDetails.controls.append(
                ft.Text(f"{nodo} -- {peso}")
            )
        self._view.update_page()


    def handleCercaTeamSfortunati(self, e):
        k = self._view._txtInSoglia.value
        m = self._view._txtInNumDiEdizioni.value
        if k =="" or m == "":
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(
                ft.Text("Inserisci un valore nei campi indicati", color="red")
            )
            self._view.update_page()
            return
        try:
            kInt = int(k)
        except ValueError:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(
                ft.Text("Inserisci un valore numerico di k", color="red")
            )
            self._view.update_page()
            return
        try:
            mInt = int(m)
        except ValueError:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(
                ft.Text("Inserisci un valore numeri di m", color="red")
            )
            self._view.update_page()
            return
        if kInt<0 or mInt<0:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(
                ft.Text("Inserisci un valore positivo di k e/o m", color="red")
            )
            self._view.update_page()
            return

        self._model.getPath(k,m)


    def fillDDYears(self):
        years = self._model.getAllYears()
        for y in years:
            self._view._ddYear1.options.append(
                ft.dropdown.Option(y)
            )
            self._view._ddYear2.options.append(
                ft.dropdown.Option(y)
            )
        self._view.update_page()
