import logging
from multiprocessing import Process
from sklearn.ensemble import RandomForestClassifier
from joblib import dump
import time
import queue
import numpy as np

class PoseData:
    def __init__(self, name, label):
        self.name = name
        self.label = label
        self.data = []

    def add(self, point):
        self.data.append(np.array(point))

    def to_labels(self):
        return np.repeat(self.label, len(self.data))

    def to_numpy(self):
        return np.array(self.data)

class Trainer(Process):
    def __init__(self, poses, queue, path="classifier.pkl"):
        super(Trainer, self).__init__()
        self.poses = [PoseData(pose, label) for label, pose in enumerate(poses)]
        self.pose_map = {index: name for index, name in enumerate(poses)}
        self.queue = queue
        self.path = path

    def classify(self, p):
        if hasattr(self, "classifier"):
            y = self.classifier.predict(p)
            return pose_map[y]
        return 0

    def record(self, duration, pose):
        start = time.time()
        while time.time() < start + duration:
            try:
                value = self.queue.get(True, 0.5)
                pose.add(value)
            except queue.Empty:
                pass
            except Exception as e:
                logging.error("Error when recording events " + str(e))

    def train(self):
        classifier = RandomForestClassifier()
        logging.info([d.to_numpy().shape for d in self.poses])
        data = np.concatenate([d.to_numpy() for d in self.poses])
        labels = np.concatenate([d.to_labels() for d in self.poses])
        np.save("X", data)
        np.save("Y", labels)
        classifier.fit(data, labels)
        score = classifier.score(data, labels)
        logging.info("Classified with mean accuracy " + str(score))
        dump(classifier, self.path)

    def run(self):
        try: 
            for pose in self.poses:
                logging.info("Assume pose '{}'".format(pose.name))
                time.sleep(1)
                logging.info("... Recording")
                self.record(10, pose)

            self.train()
            logging.info("Training complete")

        except Exception as e:
            logging.error("Error when training myo: " + str(e))

