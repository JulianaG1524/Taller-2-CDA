import os
import pandas as pd
import requests

# Ruta de la carpeta principal
carpeta_principal = path + 'iconic-images-and-descriptions'

# Lista para almacenar los resultados
resultados = []

# Lista para guardar los errores
errores = []

# Recorremos la carpeta principal y todos los subdirectorios
for root, dirs, files in os.walk(carpeta_principal):
    for file in files:
        if file.endswith("_Information.txt"):
            # Ruta completa del archivo
            file_path = os.path.join(root, file)
            
            # Abrimos y leemos el archivo
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    res = {}
                    if line.startswith("Title:"):
                        # Extraer el título después de "Title:"
                        title = line.strip().split("Title:")[1].strip()

                    if line.startswith("URL:"):
                        # Extraer la URL después de "URL:"
                        url = line.strip().split("URL:")[1].strip()
                        
                        # Separar la URL por "-" y tomar el último pedazo como ID
                        id = url.split("-")[-1]
                        
                        # Realizar la petición GET
                        api_url = f"https://www.hemkop.se/axfood/rest/p/{id}"
                        try:
                            response = requests.get(api_url)
                            response.raise_for_status()  # Verifica si la petición fue exitosa
                            data = response.json()      # Parseamos la respuesta como JSON
                            
                            # Obtener el precio
                            price_value = data.get("priceValue", None)
                            
                            # Guardar el resultado en la lista
                            resultados.append({"code": id, "title": title, "url": url, "priceValue": price_value})
                        except requests.RequestException as e:
                            print(f"Error al realizar la petición para ID {id}: {e}")
                            errores.append({"code": id, "title": title, "url": url, "error": str(e)})
                        except ValueError:
                            print(f"Error al parsear la respuesta para ID {id}: {response.text}")

# Crear un DataFrame con los resultados
df = pd.DataFrame(resultados)

df_errores = pd.DataFrame(errores)

# Guardar el DataFrame en un archivo CSV
output_file = "resultados.csv"
df.to_csv(output_file, index=False, encoding='utf-8')
df_errores.to_csv("errores.csv", index=False, encoding='utf-8')
print(f"Resultados guardados en {output_file}")