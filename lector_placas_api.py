# Api : https://api.platerecognizer.com/v1/plate-reader
import uvicorn
import cv2
import requests
from fastapi import FastAPI


#funcion para leer la placa
def leer_placa(img):
    regions = ['ec', 'us-ca'] # estos parametros depende del tipo de placa a leer segun el pais
    with open(img, 'rb') as fp:
        #se pide la consulta al servidor
        response = requests.post(
            'https://api.platerecognizer.com/v1/plate-reader/',
            data=dict(regions=regions),  # Opcional
            # se sube la foto al servidor
            # Se le envia el token a la APi de la web http://docs.platerecognizer.com/
            # Aqui tienes que colocar tu propio Token suscribiendote a la pagina
            files=dict(upload=fp),
            headers={'Authorization': 'Token 793ffb34b7a6c3aaeef70e48db8c176ea80a9530 '})
    return response.json() #retorna el json con los datos procesados



app = FastAPI()
@app.get("/leer_placa")




def index():
        cap = cv2.VideoCapture("rtsp://admin:001122Admin@192.168.10.89")
        recording = True
        while True:
                ret, frame = cap.read()
                print("Empezó a leer")
                foto="temp.jpg" # nombre de la imagen temporal a guardar
                # se guarda la imagen capturada por el video
                cv2.imwrite(foto,frame)
                # se llama a la funcion leer placa
                data=leer_placa(foto)
                print("Terminó de leer y retorna")
                return data



if __name__ == '__main__':
   uvicorn.run(app, host="0.0.0.0", port=5555)