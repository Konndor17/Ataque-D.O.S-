import os
import sys
import platform
import subprocess
import time
import threading
# pip install os-sys
# pip install platform
# pip install subprocess
# pip install time
# pip install threading
# En resumen, este script permite enviar una gran cantidad de pings a un host en paralelo utilizando
# múltiples hilos. Los resultados de cada ping se muestran en la consola. Ten en cuenta que este código genera una
# gran cantidad de tráfico de red y consumo de recursos de CPU, por lo que debe usarse con responsabilidad y con la 
# debida autorización. Además, ten en cuenta que la precisión de la simulación de "ping" puede variar según el 
# sistema operativo y las configuraciones de red.
def ping(host, count, timeout):
    try:
        # Comando de ping dependiendo del sistema operativo
        if platform.system().lower() == "windows":
            cmd = ["ping", "-n", str(count), "-w", str(timeout * 1000), host]
        else:
            cmd = ["ping", "-c", str(count), "-W", str(timeout), host]

        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        while True:
            try:
                output = process.stdout.readline()
                if not output:
                    break
                print(output.strip())
            except KeyboardInterrupt:
                process.terminate()
                break

        process.wait()
        return process.returncode

    except Exception as e:
        print(f"Error: {str(e)}")
        return 1

if __name__ == "__main__":
    host = input("Ingrese la dirección IP o nombre de host: ")
    count = int(input("Ingrese el número de paquetes a enviar (presione Enter para usar 1000): ") or 1000)
    timeout = int(input("Ingrese el tiempo de espera en segundos (presione Enter para usar 1 segundo): ") or 1)
    num_threads = int(input("Ingrese el número de hilos para enviar pings simultáneos: "))

    print(f"\nRealizando {count} pings simultáneos a {host} con un tiempo de espera de {timeout} segundos...\n")

    def ping_thread():
        for _ in range(count):
            ping(host, 1, timeout)

    threads = []

    for _ in range(num_threads):
        thread = threading.Thread(target=ping_thread)
        thread.start()
        threads.append(thread)

    try:
        for thread in threads:
            thread.join()
    except KeyboardInterrupt:
        print("\nPing detenido por el usuario.")

    print(f"\nPing completo a {host}.")
