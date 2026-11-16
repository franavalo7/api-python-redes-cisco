import requests
import json
import csv
from getpass import getpass
from tabulate import tabulate

baseUri = "http://127.0.0.1:58000/api/v1"

# Solicitar Service Ticket
headers = {"Content-Type": "application/json"}

data = json.dumps({
    "username": "cisco",
    "password": getpass("Ingrese la contraseña del controlador: ")
})

resp = requests.post(baseUri + "/ticket", data=data, headers=headers)

print("Status de Solicitud:")
print(resp.status_code)

result = resp.json()

if resp.status_code != 201:
    print(result)
else:
    ticket = result["response"]["serviceTicket"]

    # Consultar dispositivos de red
    headers = {"X-Auth-Token": ticket}
    resp = requests.get(baseUri + "/network-device", headers=headers)

    print("\nStatus de dispositivos:", resp.status_code)

    result = resp.json()

    if resp.status_code == 200:
        print("\nDispositivos de Red:")

        host_list = []
        i = 0

        for item in result["response"]:
            i += 1

            hostname = item.get("hostname", "N/D")
            serial = item.get("serialNumber", "N/D")
            software = item.get("softwareVersion", "N/D")

            host_list.append([i, hostname, serial, software])

        print(tabulate(
            host_list,
            headers=["N°", "Hostname", "Serial Number", "Software Version"],
            tablefmt="rst"
        ))

        # Funcionalidad propia: exportar inventario a CSV
        with open("inventario.csv", "w", newline="", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(["N°", "Hostname", "Serial Number", "Software Version"])
            escritor.writerows(host_list)

        print("\nInventario exportado correctamente a inventario.csv")

        # Consultar hosts
        resp = requests.get(baseUri + "/host", headers=headers)

        print("\nStatus de hosts:", resp.status_code)

        result = resp.json()

        if resp.status_code == 200:
            print("\nHosts de la Red:")

            host_list = []
            i = 0

            for item in result["response"]:
                i += 1

                hostname = item.get("hostName", "N/D")
                host_type = item.get("hostType", "N/D")
                host_ip = item.get("hostIp", "N/D")

                host_list.append([i, hostname, host_type, host_ip])

            print(tabulate(
                host_list,
                headers=["N°", "Hostname", "Tipo", "IP"],
                tablefmt="rst"
            ))
        else:
            print(result)
    else:
        print(json.dumps(result, indent=4))