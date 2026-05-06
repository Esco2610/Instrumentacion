import serial
import csv
import time

# --- Configuración ---
puerto_serial = 'COM3' 
baudios = 9600
nombre_archivo = "datos_lab4_instru_temperatura.csv"
muestras_por_grado = 20 

temperatura = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]

try:
    arduino = serial.Serial(puerto_serial, baudios, timeout=1)
    time.sleep(2)
    
 
    with open(nombre_archivo, mode='w', newline='') as archivo:
        escritor = csv.writer(archivo, delimiter=',')
        escritor.writerow(["Temperatura_Celcius", "Voltaje_Promedio_V"])
        archivo.flush() 
    
        
        for c in temperatura:
            input(f"\n Coloca {c} grados y presiona ENTER para medir...")
            
            arduino.reset_input_buffer()
            lecturas = []
            
            while len(lecturas) < muestras_por_grado:
                linea = arduino.readline().decode('utf-8').strip()
                if linea:
                    try:
                        # Etapa D: Conversión de digital a voltaje
                        v = float(linea)
                        lecturas.append(v)
                        if len(lecturas) % 5 == 0: print(".", end="")
                    except ValueError: continue
            
            promedio = sum(lecturas) / len(lecturas)
            
            # Escribimos el dato promediado
            escritor.writerow([c, round(promedio, 4)])
            print(f"\n {c} celcius -> {promedio:.4f} V")
            archivo.flush() 
            

    print("\n Proceso completado")

except Exception as e:
    print(f"\nError: {e}")
finally:
    if 'arduino' in locals(): 
        arduino.close()
        print("Puerto serial cerrado.")