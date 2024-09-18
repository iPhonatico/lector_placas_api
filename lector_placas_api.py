import uvicorn
import cv2
import requests
from fastapi import FastAPI
from decouple import config


# Función para leer la placa
def leer_placa(img):
    regions = ['ec', 'us-ca']  # Depende del tipo de placa a leer según el país
    with open(img, 'rb') as fp:
        # Se pide la consulta al servidor
        response = requests.post(
            'https://api.platerecognizer.com/v1/plate-reader/',
            data=dict(regions=regions),  # Opcional
            # Se sube la foto al servidor
            headers={'Authorization': 'Token ' + config('SECRET_TOKEN')},
            files=dict(upload=fp)
        )
    return response.json()  # Retorna el JSON con los datos procesados


# Función para enviar el POST
def enviar_post(plate, vehicle_type):
    url = config('SECRET_API')
    payload = {
        "plate": plate,
        "color": vehicle_type,  # El "color" será asignado con el atributo "type"
        "parking": 1,
        "automatic": True
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    print("Respuesta del servidor:", response.text)

    if response.status_code == 200:
        try:
            return response.status_code, response.json()
        except ValueError:
            return response.status_code, {"message": "No se recibió un cuerpo JSON válido."}
    else:
        return response.status_code, {"message": "Error al hacer el POST.", "response_text": response.text}


app = FastAPI()


@app.get("/leer_placa")
def index():
    cap = cv2.VideoCapture(config('SECRET_CAM_URL'))
    recording = True
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("No se pudo leer el video.")
                break
            print("Empezó a leer")
            foto = "temp.jpg"  # Nombre de la imagen temporal a guardar
            # Se guarda la imagen capturada por el video
            cv2.imwrite(foto, frame)
            # Se llama a la función leer placa
            data = leer_placa(foto)

            # Validar si no hay resultados en "results"
            if not data['results']:
                print("No se encontró un vehículo en la imagen.")
                return {"message": "No se encontró un vehículo en la imagen."}

            # Extrae la placa y el tipo de vehículo del JSON
            plate = data['results'][0]['plate']  # Obtiene la placa
            vehicle_type = data['results'][0]['vehicle']['type']  # Obtiene el tipo de vehículo

            print(f"Placa: {plate}, Tipo de vehículo: {vehicle_type}")

            # Envía los datos extraídos en el POST
            status_code, response_data = enviar_post(plate, vehicle_type)
            print(f"POST enviado. Código de estado: {status_code}")

            return {"status_code": status_code, "response": response_data}
    except KeyboardInterrupt:
        print("Interrupción por teclado, cerrando...")
    finally:
        cap.release()


if __name__ == '__main__':
    try:
        uvicorn.run(app, host="0.0.0.0", port=5555)
    except KeyboardInterrupt:
        print("El servidor ha sido interrumpido con Control+C.")
