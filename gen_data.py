from roboflow import Roboflow

rf = Roboflow(api_key="<insert_key_here>")
project = rf.workspace("watchtower").project("ttr-obj-detect")
dataset = project.version(2).download("yolov8")