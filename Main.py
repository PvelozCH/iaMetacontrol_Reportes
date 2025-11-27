from Service.UnifierService import uniController

def operaUnifierUDR():
    print("Se cargara reporte Unifier")
    token = uniController.getTokenUnifier()
    nomReporte = input("Ingresa el nombre del reporte : ")
    jsonUnifier = uniController.loadReportUnifier(token,nomReporte)
    return jsonUnifier

def main():
    print("### Ejecución del programa ###")
    print(operaUnifierUDR())




if __name__ == "__main__":
    main()