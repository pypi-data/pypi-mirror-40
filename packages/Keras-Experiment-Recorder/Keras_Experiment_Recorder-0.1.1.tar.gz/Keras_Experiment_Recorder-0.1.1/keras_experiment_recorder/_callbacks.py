import os
import time
import glob
import tensorflow as tf
import firebase_admin

from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage


class FirebaseInfo(object):
    def __init__(self, credential_path, bucket_name, collection_name='keras-experiments'):
        self.credential_path = credential_path
        self.collection_name = collection_name
        self.bucket_name = bucket_name


class ExperimentInfo(object):
    def __init__(self, name, fb_info, files_to_upload=[]):
        self.name = name
        self.fb_info = fb_info
        self.files_to_upload = files_to_upload


class ExperimentRecorder(tf.keras.callbacks.Callback):

    def __init__(self, experiment_info):
        self.experiment_info = experiment_info
        self.doc_ref = None
        self.results_per_epoch = []

        # initialize firebase
        cred = credentials.Certificate(experiment_info.fb_info.credential_path)
        firebase_admin.initialize_app(cred)

        super(ExperimentRecorder, self).__init__()

    def on_train_begin(self, logs={}):

        collection_name = self.experiment_info.fb_info.collection_name

        # get the model details
        model_details = self.model.to_json()

        # write initial data
        self.doc_ref = firestore.client().collection(collection_name).document()
        self.doc_ref.set({
            u'name': self.experiment_info.name,
            u'model_params': self.params,
            u'training_start_time': time.time()
        })

        print(f"Firebase document id - {self.doc_ref.id}")

        # upload the model.json to the storage
        model_details_object_name = f"{collection_name}/{self.doc_ref.id}/model.json"
        bucket = storage.bucket(self.experiment_info.fb_info.bucket_name)
        blob = bucket.blob(model_details_object_name)
        blob.upload_from_string(model_details, content_type='application/json')

    def on_train_end(self, logs={}):
        self.doc_ref.update({
            u'training_end_time': time.time()
        })

        self.doc_ref.update({
            u'metrics': self.results_per_epoch
        })

        # upload the files (if any)
        results = list(map(glob.glob, self.experiment_info.files_to_upload))
        # flatten the results
        results = [item for sublist in results for item in sublist]

        collection_name = self.experiment_info.fb_info.collection_name

        for r in results:
            object_name = f"{collection_name}/{self.doc_ref.id}/{os.path.basename(r)}"
            bucket = storage.bucket(self.experiment_info.fb_info.bucket_name)
            blob = bucket.blob(object_name)
            blob.upload_from_filename(r)

    def on_epoch_end(self, epoch, logs=None):
        logs = logs or {}
        metrics_result = {
            'epoch': epoch
        }
        for k in self.params['metrics']:
            if k in logs:
                metrics_result[k] = logs[k]

        self.results_per_epoch.append(metrics_result)
