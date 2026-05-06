import serial
import csv
import time

# --- Configuración ---
puerto_serial = 'COM10' 
baudios = 9600
nombre_archivo = "datos_lab4_instru_lux.csv"
muestras_por_lux = 20 

luxes = [1, 5, 10, 25, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 600, 700, 800, 900, 1000]

try:
    arduino = serial.Serial(puerto_serial, baudios, timeout=1)
    time.sleep(2)
    
 
    with open(nombre_archivo, mode='w', newline='') as archivo:
        escritor = csv.writer(archivo, delimiter=',')
        escritor.writerow(["Luminancia_lux", "Voltaje_Promedio_V"])
        archivo.flush() 
    
        
        for l in luxes:
            input(f"\n Coloca {l} lx y presiona ENTER para medir...")
            
            arduino.reset_input_buffer()
            lecturas = []
            
            while len(lecturas) < muestras_por_lux:
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
            escritor.writerow([l, round(promedio, 4)])
            print(f"\n {l}g -> {promedio:.4f} V")
            archivo.flush() 
            

    print("\n Proceso completado")

except Exception as e:
    print(f"\nError: {e}")
finally:
    if 'arduino' in locals(): 
        arduino.close()
        print("Puerto serial cerrado.")