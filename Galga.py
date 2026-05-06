import serial
import csv
import time

# --- Configuración ---
puerto_serial = 'COM10' 
baudios = 9600
nombre_archivo = "datos_lab4_instru.csv"
muestras_por_peso = 20 

pesos = [71, 81, 91, 100, 150, 200, 253, 303, 353, 400, 450, 500, 554]

try:
    arduino = serial.Serial(puerto_serial, baudios, timeout=1)
    time.sleep(2)
    
 
    with open(nombre_archivo, mode='w', newline='') as archivo:
        escritor = csv.writer(archivo, delimiter=',')
        escritor.writerow(["Peso_g", "Voltaje_Promedio_V"])
        archivo.flush() 
    
        
        for p in pesos:
            input(f"\n Coloca {p}g y presiona ENTER para medir...")
            
            arduino.reset_input_buffer()
            lecturas = []
            
            while len(lecturas) < muestras_por_peso:
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
            escritor.writerow([p, round(promedio, 4)])
            
            archivo.flush() 
            

    print("\n Proceso completado")

except Exception as e:
    print(f"\nError: {e}")
finally:
    if 'arduino' in locals(): 
        arduino.close()
        print("Puerto serial cerrado.")