# Keras Experiment Recorder

This is a set of utilities (mostly a keras Callback) that help store various aspects of an
experiment (e.g. model information, results of training etc) in firebase backend.

## Prerequisites

You will need the service account of a firebase app.

## Usage

```python
from keras_experiment_recorder import ExperimentInfo, FirebaseInfo
from keras_experiment_recorder import ExperimentRecorder

# below three lines setup the instance of ExperimentRecorder
fb_info = FirebaseInfo(bucket_name=bucket_name,
                           credential_path=credential_path)
experiment_info = ExperimentInfo(name='first exp', fb_info=fb_info)
recorder = ExperimentRecorder(experiment_info)

callbacks = [recorder]

history = model.fit(x_train, y_train,
                    batch_size=batch_size,
                    epochs=epochs,
                    verbose=1,
                    callbacks=callbacks,    # pass the callbacks
                    validation_split=0.1)

```

### Running the example included in this repository

```bash
python examples/simple.py --bucket-name keras-experiment-recorder.appspot.com --credential-path ~/Desktop/Dev/keys/keras-experimen
t-recorder-firebase.json
```
