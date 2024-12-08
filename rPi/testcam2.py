from util_inf_cam2 import setup

# Configuración inicial del modelo YOLOv8 con umbral de impresión adicional
detection_model = setup("best.onnx", confidence_thres=0.5, iou_thres=0.5, print_thres=0.1)

print("Presiona '1' para capturar una imagen y realizar inferencia, o 'salir' para terminar.")

while True:
    user_input = input("Ingresa '1' para capturar o 'salir' para salir: ").strip()
    
    if user_input.lower() == 'salir':
        print("Saliendo del programa.")
        break
    elif user_input == '1':
        try:
            detection_model.capture_and_infer()
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("Comando no reconocido. Intenta nuevamente.")
