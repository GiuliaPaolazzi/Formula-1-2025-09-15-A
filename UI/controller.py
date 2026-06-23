import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._k = None
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        #io
        self._choiceAnno1 = None
        self._choiceAnno2 = None


    def handleCreaGrafo(self,e):
        if self._choiceAnno1 is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Attenzione scegliere anno", color= "red"))
            self._view.update_page()
        if self._choiceAnno2 is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Attenzione scegliere anno", color="red"))
            self._view.update_page()
        self._model.buildGraph(self._choiceAnno1, self._choiceAnno2)
        nN=self._model.getNumNodes()
        nE=self._model.getNumEdges()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Grafo creato correttamente con {nN} nodi e {nE} archi", color="green"))
        self._view.update_page()

    def handleDettagli(self, e):
        top3= self._model.getTop3Archi()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Top 3 archi di peso maggiore:"))
        for a in top3:
            self._view.txt_result.controls.append(ft.Text(f"{a[0]}->{a[1]} peso: {a[2]["weight"]}"))
        numero, largest, details = self._model.getConnessaInfo()
        self._view.txt_result.controls.append(ft.Text(f"Il grafo contiene {numero} componenti connesse."
                                                      f"La componente maggiore ha dimensione {len(largest)}"))
        for l in largest:
            self._view.txt_result.controls.append(ft.Text(l))
        self._view.txt_result.controls.append(ft.Text(f"Componente connessa in ordine decrescente di nodi:"))
        for d in details:
            self._view.txt_result.controls.append(ft.Text(f"{d[0]} - grado {d[1]}"))
        self._view.update_page()

    def handleCerca(self, e):
        k= self._view._txtInK.value
        if k == None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text(f"Attenzione, Inserire valore numerico!", color="red"))
            self._view.update_page()
            return
        try:
            kInt = int(k)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Inserire un valore numerico intero!", color="red"))
            self._view.update_page()
            return
            # controllo che sia positivo
        if kInt < 0:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Inserire un valore numerico intero positivo!", color="red"))
            self._view.update_page()
        self._k = kInt
        listaPilotiOttima, minDistanza =self._model.getListaPilotiOttima(self._k)
        self._view.txt_result.controls.clear()
        if listaPilotiOttima == None:

            self._view.txt_result.controls.append(
            ft.Text(f"Non ci sono abbastanza componenti connesse per trovare {k} piloti"))
            self._view.update_page()
            return
        self._view.txt_result.controls.append(
            ft.Text(f"Lista piloti con differenza di età {minDistanza}. NODI {len(listaPilotiOttima)} :"))
        for p in listaPilotiOttima:
            print("AAAAAAAAAAAAAA")
            self._view.txt_result.controls.append(ft.Text(p))

        self._view.update_page()





    def fillDDAnni(self):
        anni = self._model.getAllYears()
        for a in anni:
            self._view._ddAnno1.options.append(ft.dropdown.Option(data=a,
                                                                 key=a,
                                                                 on_click=self._choiceDDAnno1))
            self._view._ddAnno2.options.append(ft.dropdown.Option(data=a,
                                                                  key=a,
                                                                  on_click=self._choiceDDAnno2))
            self._view.update_page()

    def _choiceDDAnno1(self, e):
        self._choiceAnno1 = e.control.data
        print(f"L'anno selezionato è {self._choiceAnno1}")
    def _choiceDDAnno2(self, e):
        self._choiceAnno2 = e.control.data
        print(f"L'anno selezionato è {self._choiceAnno2}")



