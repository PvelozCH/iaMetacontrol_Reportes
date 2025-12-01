from Service.UnifierService import uniController
import traceback,sys

def operaUnifierUDR():
    try:

        print("Se cargara reporte Unifier")
        token = uniController.getTokenUnifier()
        print("Se cargará y creará base de datos sql a partir de reporte UDR")
        nomReporte = input("Ingresa el nombre del reporte : ")
        a,b,c = uniController.loadReportUnifierV2(token,nomReporte)
        uniController.creacionDbUnifier(a,b,c)
    except Exception as e:
        print("Error completo : ",traceback.format_exc())
        print("Error : ",e)

def main():
    print("### Ejecución del programa ###")
    print(operaUnifierUDR())




if __name__ == "__main__":
    main()