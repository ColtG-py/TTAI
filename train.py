from ultralytics import YOLO

model = YOLO("yolov8n.pt")  # load a pretrained model (recommended for training)
results = model.train(data="datasets/ttr-obj-detect-2/data.yaml", epochs=10)  # train the model
results = model.val()
success = model.export(format="onnx")  # export the model to ONNX format