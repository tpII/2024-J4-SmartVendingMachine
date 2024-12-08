import time
import cv2
import numpy as np
import onnxruntime as ort
import yaml
import os

def load_classes_from_yaml(file_path):
    """
    Carga las clases desde un archivo YAML.
    
    Args:
        file_path (str): Ruta del archivo YAML.

    Returns:
        dict: Diccionario de clases.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Archivo YAML no encontrado: {file_path}")
    try:
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        raise ValueError(f"Error en el archivo YAML: {e}")
    return data["names"]

class YOLOv8:
    def __init__(self, onnx_model, confidence_thres, iou_thres, print_thres=0.1):
        self.onnx_model = onnx_model
        self.confidence_thres = confidence_thres
        self.iou_thres = iou_thres
        self.print_thres = print_thres  # Nuevo umbral para mostrar resultados en consola

        # Cargar los nombres de las clases del modelo
        self.classes = load_classes_from_yaml("data.yaml")
        self.color_palette = np.random.uniform(0, 255, size=(len(self.classes), 3))

        # Inicializar sesión ONNX
        self.session = ort.InferenceSession(self.onnx_model, providers=["CPUExecutionProvider"])
        model_inputs = self.session.get_inputs()
        input_shape = model_inputs[0].shape
        self.input_width = input_shape[2]
        self.input_height = input_shape[3]
        self.model_input_name = model_inputs[0].name

        # Inicializar cámara
        self.camera = cv2.VideoCapture(0)
        if not self.camera.isOpened():
            raise RuntimeError("No se pudo inicializar la cámara.")
        print("Cámara inicializada correctamente.")

    def capture_and_infer(self):
        # Asegurarse de descartar frames antiguos
        for _ in range(5):  # Leer varios frames para asegurarse de que el buffer se limpia
            self.camera.grab()
        
        # Capturar un nuevo frame
        ret, frame = self.camera.read()
        if not ret:
            raise RuntimeError("Error al capturar la imagen de la cámara.")

        # Guardar la imagen original
        timestamp = int(time.time())
        original_image_path = f"original_{timestamp}.jpg"
        cv2.imwrite(original_image_path, frame)
        print(f"Imagen capturada y guardada como {original_image_path}")

        # Redimensionar la imagen a 640x640
        resized_frame = cv2.resize(frame, (640, 640))

        # Realizar inferencia en la imagen redimensionada
        try:
            output_image = self.run_inference_from_frame(resized_frame)

            # Guardar la imagen con detecciones
            processed_image_path = f"processed_{timestamp}.jpg"
            cv2.imwrite(processed_image_path, output_image)
            print(f"Imagen procesada guardada como {processed_image_path}")
        except Exception as e:
            print(f"Error durante la inferencia: {e}")

    def preprocess(self, frame):
        self.img_height, self.img_width = frame.shape[:2]
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (self.input_width, self.input_height))
        image_data = np.array(img) / 255.0
        image_data = np.transpose(image_data, (2, 0, 1))
        return np.expand_dims(image_data, axis=0).astype(np.float32)

    def postprocess(self, input_frame, output):
        outputs = np.transpose(np.squeeze(output[0]))
        rows = outputs.shape[0]
        boxes, scores, class_ids = [], [], []

        x_factor = self.img_width / self.input_width
        y_factor = self.img_height / self.input_height

        for i in range(rows):
            classes_scores = outputs[i][4:]
            max_score = np.amax(classes_scores)
            class_id = np.argmax(classes_scores)

            # Construcción de listas para NMS
            if max_score >= self.confidence_thres:
                x, y, w, h = outputs[i][0], outputs[i][1], outputs[i][2], outputs[i][3]
                left = int((x - w / 2) * x_factor)
                top = int((y - h / 2) * y_factor)
                width = int(w * x_factor)
                height = int(h * y_factor)

                class_ids.append(class_id)
                scores.append(max_score)
                boxes.append([left, top, width, height])

        # Aplicar NMS para eliminar cuadros redundantes
        indices = cv2.dnn.NMSBoxes(boxes, scores, self.confidence_thres, self.iou_thres)

        for i in indices:
            box = boxes[i]
            score = scores[i]
            class_id = class_ids[i]

            # Ahora imprimimos solo las detecciones finales
            if score >= self.print_thres:
                print(f"Clase: {self.classes[class_id]}, Puntuación: {score:.2f}")

            self.draw_detections(input_frame, box, score, class_id)

        return input_frame

    def draw_detections(self, frame, box, score, class_id):
        """
        Dibuja las detecciones en el frame.
        """
        x1, y1, w, h = box
        color = self.color_palette[class_id]
        cv2.rectangle(frame, (x1, y1), (x1 + w, y1 + h), color, 2)
        label = f"{self.classes[class_id]}: {score:.2f}"
        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    def run_inference_from_frame(self, frame):
        img_data = self.preprocess(frame)
        outputs = self.session.run(None, {self.model_input_name: img_data})
        return self.postprocess(frame, outputs)

    def __del__(self):
        if hasattr(self, 'camera') and self.camera.isOpened():
            self.camera.release()
            print("Cámara liberada.")

def setup(onnx_model, confidence_thres=0.5, iou_thres=0.5, print_thres=0.1):
    return YOLOv8(onnx_model, confidence_thres, iou_thres, print_thres)
