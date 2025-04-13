from ultralytics import YOLO
import supervision as sv

class InferenceEngine:
    def __init__(self, model_path):
        self.model = YOLO(model_path, verbose=False)
        self.box_annotator = sv.BoundingBoxAnnotator()
        self.label_annotator = sv.LabelAnnotator()

    def run(self, frame):
        results = self.model(frame)[0]
        detections = sv.Detections.from_ultralytics(results)
        return detections

    def annotate(self, frame, detections):
        frame = self.box_annotator.annotate(scene=frame, detections=detections)
        frame = self.label_annotator.annotate(scene=frame, detections=detections)
        return frame
