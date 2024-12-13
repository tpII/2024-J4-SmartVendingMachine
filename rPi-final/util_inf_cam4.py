import time
import cv2
import numpy as np
import onnxruntime as ort
import yaml
import os

def load_classes_from_yaml(file_path):
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
        self.print_thres = print_thres

        self.classes = load_classes_from_yaml("data.yaml")
        self.color_palette = np.random.uniform(0, 255, size=(len(self.classes), 3))

        self.session = ort.InferenceSession(self.onnx_model, providers=["CPUExecutionProvider"])
        model_inputs = self.session.get_inputs()
        input_shape = model_inputs[0].shape
        self.input_width = input_shape[2]
        self.input_height = input_shape[3]
        self.model_input_name = model_inputs[0].name

        print("Ejecutando inferencia de calentamiento...")
        dummy_input = np.zeros((1, 3, self.input_height, self.input_width), dtype=np.float32)
        self.session.run(None, {self.model_input_name: dummy_input})
        print("Inferencia de calentamiento completada.")

        self.camera = cv2.VideoCapture(0)
        if not self.camera.isOpened():
            raise RuntimeError("No se pudo inicializar la cámara.")
        print("Cámara inicializada correctamente.")

    def capture_and_infer(self, detection_counts):
        print("Capturando imagen e iniciando inferencia...")
        for _ in range(10):
            self.camera.grab()

        ret, frame = self.camera.read()
        if not ret:
            raise RuntimeError("Error al capturar la imagen de la cámara.")

        resized_frame = cv2.resize(frame, (self.input_width, self.input_height))
        try:
            img_data = self.preprocess(resized_frame)
            outputs = self.session.run(None, {self.model_input_name: img_data})
            detections = self.postprocess_counts(outputs)

            print("Detecciones realizadas:")
            for class_name, count in detections.items():
                print(f" - {class_name}: {count}")

            for class_name, count in detections.items():
                detection_counts[class_name] = detection_counts.get(class_name, 0) + count

            print("Inferencia completada. Resultados actualizados en el diccionario.")
        except Exception as e:
            print(f"Error durante la inferencia: {e}")

    def preprocess(self, frame):
        self.img_height, self.img_width = frame.shape[:2]
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (self.input_width, self.input_height))
        image_data = np.array(img) / 255.0
        image_data = np.transpose(image_data, (2, 0, 1))
        return np.expand_dims(image_data, axis=0).astype(np.float32)

    def postprocess_counts(self, outputs):
        outputs = np.transpose(np.squeeze(outputs[0]))
        rows = outputs.shape[0]
        boxes, scores, class_ids = [], [], []

        for i in range(rows):
            classes_scores = outputs[i][4:]
            max_score = np.amax(classes_scores)
            class_id = np.argmax(classes_scores)

            if max_score >= self.confidence_thres:
                x, y, w, h = outputs[i][:4]
                left = int((x - w / 2) * self.img_width / self.input_width)
                top = int((y - h / 2) * self.img_height / self.input_height)
                width = int(w * self.img_width / self.input_width)
                height = int(h * self.img_height / self.input_height)

                boxes.append([left, top, width, height])
                scores.append(float(max_score))
                class_ids.append(class_id)

        indices = cv2.dnn.NMSBoxes(boxes, scores, self.confidence_thres, self.iou_thres)

        counts = {}
        for i in indices.flatten():
            class_name = self.classes[class_ids[i]]
            counts[class_name] = counts.get(class_name, 0) + 1

        return counts

    def __del__(self):
        if hasattr(self, 'camera') and self.camera.isOpened():
            self.camera.release()
            print("Cámara liberada.")

def setup(onnx_model, confidence_thres=0.5, iou_thres=0.5, print_thres=0.1):
    return YOLOv8(onnx_model, confidence_thres, iou_thres, print_thres)
