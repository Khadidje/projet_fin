
# -*- coding: utf-8 -*-
"""ANN.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1FwnwnuLu0ILhI6viwuxlU9lXsIauNX_F
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# Shows plots in jupyter notebook
# %matplotlib inline

from google.colab import drive
drive.mount('/content/drive')

df = pd.read_csv("./drive/MyDrive/input/mitbih_train.csv", header = None)

df.head()

df.info()

df.describe()

df.isnull().values.sum()

df[187].value_counts()

plt.figure(figsize=(7,7))
plt.pie(df[187].value_counts(), labels = ["Normal","Inconnu","Ventriculaire","Supraventriculaire","Fusion "],colors= ['blue','purple','green','red','yellow'],autopct='%3.1f%%')

color = ['blue','red','green','yellow','purple']
label = ["Normal","Inconnu","Ventriculaire","Supraventriculaire","Fusion "]

fig, ax = plt.subplots(6, figsize=(10, 10))

for i in range(5):
    t = sns.lineplot((df[df[187] == i].iloc[0])[:-1], label=label[i], color=color[i], ax=ax[i])
    t = sns.lineplot((df[df[187] == i].iloc[0])[:-1], label=label[i], color=color[i], ax=ax[5])

fig, ax = plt.subplots(5,  sharex=True, sharey=True,figsize=(10,10))
for j in range(5):
    for i in range(100):
        t = ax[j].plot((df[df[187] == j].iloc[i])[:-1], color=color[j], alpha = 0.1)
    ax[j].title.set_text(label[j])

df.shape

df.drop_duplicates(keep=False, inplace=True)
df.shape

from sklearn.model_selection import StratifiedShuffleSplit
split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
for train_index, valid_index in split.split(df, df[187]):
    X = df.iloc[train_index]
    X_valid = df.iloc[valid_index]

X[187].value_counts() / len(X)

X_valid[187].value_counts() / len(X_valid)

y = X[187]
y_valid = X_valid[187]
X.pop(187)
X_valid.pop(187)

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import f_classif

scaler=StandardScaler()
X = scaler.fit_transform(X)
X = pd.DataFrame(X)
X_valid = scaler.transform(X_valid)
X_valid = pd.DataFrame(X_valid)

import tensorflow 
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense, Flatten
from keras import optimizers
import math


model = keras.models.Sequential()
model.add(keras.layers.Flatten(input_shape=X.shape[1:]))
model.add(keras.layers.Dense(50,
                                 kernel_initializer="lecun_normal",
                                 activation="selu"))
model.add(keras.layers.Dense(50,
                                 kernel_initializer="lecun_normal",
                                 activation="selu"))

model.add(keras.layers.Dense(5, activation="softmax"))

optimizer=keras.optimizers.SGD(learning_rate=1e-2, momentum=0.9)
model.compile(loss="sparse_categorical_crossentropy", optimizer=optimizer, metrics=["accuracy"])

import keras.callbacks
early_stopping_cb = keras.callbacks.EarlyStopping(patience=10,
                                                  restore_best_weights=True)
#onecycle = OneCycleScheduler(math.ceil(len(X) / 32) * 32, max_rate=0.05)


history=model.fit(X, y, epochs=100,
          validation_data=(X_valid,y_valid),
          callbacks = early_stopping_cb, batch_size=32)# class_weight=class_weights)

plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.legend(["accuracy","val_accuracy"])
plt.xlabel('Epoch')
plt.ylabel('Accuracy')

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.legend(["loss","val_loss"])
plt.xlabel('Epoch')
plt.ylabel('Loss')

predictions = model.predict(X_valid)

predictions=np.argmax(predictions, axis=1)
predictions

from sklearn.metrics import classification_report
print(classification_report(y_valid, predictions))

model.evaluate(X_valid, y_valid)

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.decomposition import PCA

class PCA_97_Selector(BaseEstimator, TransformerMixin):
    
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X_reduced = pca_fit.transform(X)
        X=pd.DataFrame(X_reduced)
        return X

pca = PCA(n_components=0.97)
pca_fit = pca.fit(X)

pipeline =  Pipeline([
        ("scaler", StandardScaler()),
        ("PCA", PCA_97_Selector())
])
X = pipeline.fit_transform(X)
X = pd.DataFrame(X)
X_valid = pipeline.fit_transform(X_valid)
X_valid = pd.DataFrame(X_valid)
X.shape

model = keras.models.Sequential()
model.add(keras.layers.Flatten(input_shape=X.shape[1:]))
model.add(keras.layers.Dense(50,
                                 kernel_initializer="lecun_normal",
                                 activation="selu"))
model.add(keras.layers.Dense(50,
                                 kernel_initializer="lecun_normal",
                                 activation="selu"))

model.add(keras.layers.Dense(5, activation="softmax"))

optimizer=keras.optimizers.SGD(learning_rate=1e-2, momentum=0.9)
model.compile(loss="sparse_categorical_crossentropy", optimizer=optimizer, metrics=["accuracy"])

history=model.fit(X, y, epochs=100,
          validation_data=(X_valid,y_valid),
          callbacks = early_stopping_cb, batch_size=32)

predictions = model.predict(X_valid)
predictions=np.argmax(predictions, axis=1)

from sklearn.metrics import classification_report
print(classification_report(y_valid, predictions))

model.evaluate(X_valid, y_valid)

pip install scikit-learn

!pip install scikeras

from sklearn.model_selection import  PredefinedSplit
split_index = [-1]*len(X)+[0]*len(X_valid)
X_split = pd.concat([X, X_valid], axis=0)
Y_split = pd.concat([y, y_valid], axis=0)
pds = PredefinedSplit(test_fold=split_index)
print(pd.DataFrame(split_index).value_counts())

from scikeras.wrappers import KerasClassifier
from sklearn.model_selection import GridSearchCV
keras.backend.clear_session()
def create_model(neurons, layers):
 # create model
   model = Sequential()
   model.add(keras.layers.Flatten(input_shape=X.shape[1:]))
   for i in range(layers):
    model.add(keras.layers.Dense(neurons,
                                 kernel_initializer="lecun_normal",
                                 activation="selu"))

   model.add(keras.layers.Dense(5, activation="softmax"))
   optimizer=keras.optimizers.SGD(learning_rate=1e-2, momentum=0.9)
   model.compile(loss="sparse_categorical_crossentropy", optimizer=optimizer, metrics=["accuracy"])
   return model
 
model = KerasClassifier(model=create_model, epochs=20, verbose=0)
neurons = [50, 75, 100, 150]
layers = [2, 3, 4]

param_grid = dict(model__neurons=neurons, model__layers=layers)
grid = GridSearchCV(estimator=model, param_grid=param_grid, n_jobs=1, cv=3)
grid_result = grid.fit(X_split, Y_split, callbacks = early_stopping_cb, batch_size = 32)
print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))
means = grid_result.cv_results_['mean_test_score']
stds = grid_result.cv_results_['std_test_score']
params = grid_result.cv_results_['params']
for mean, stdev, param in zip(means, stds, params):
    print("%f (%f) with: %r" % (mean, stdev, param))

from scikeras.wrappers import KerasClassifier
from sklearn.model_selection import RandomizedSearchCV
from tensorflow import keras
from tensorflow.keras import optimizers
from tensorflow.keras.optimizers import schedules
from tensorflow.keras.optimizers.schedules import ExponentialDecay
from keras.optimizers import schedules
keras.backend.clear_session()
def create_model(learning_rate, momentum, decay, nesterov):
 # create model
   model = Sequential()
   model.add(keras.layers.Flatten(input_shape=X.shape[1:]))
   for i in range(3):
    model.add(keras.layers.Dense(150,
                                 kernel_initializer="lecun_normal",
                                 activation="selu"))

   model.add(keras.layers.Dense(5, activation="softmax"))
   s = 20 * len(X) // 32
   learning_schedule = keras.optimizers.schedules.ExponentialDecay(learning_rate, s, decay)
   optimizer=keras.optimizers.SGD(learning_rate=learning_schedule, momentum=momentum, nesterov=nesterov)
   model.compile(loss="sparse_categorical_crossentropy", optimizer=optimizer, metrics=["accuracy"])
   return model
 
model = KerasClassifier(model=create_model, epochs=25, verbose=0)
nesterov=[True, False]
learning_rate = [1e-2, 5e-3, 1e-3]
decay =[0.1, 5e-2, 1e-2]
momentum = [0.8, 0.9, 0.95]

param_grid = dict(model__learning_rate=learning_rate, model__momentum=momentum, model__decay=decay, model__nesterov=nesterov)
grid = RandomizedSearchCV(estimator=model, param_distributions=param_grid, n_jobs=1, cv=3, n_iter=15)
grid_result = grid.fit(X_split, Y_split, callbacks = early_stopping_cb, batch_size =32)
print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))
means = grid_result.cv_results_['mean_test_score']
stds = grid_result.cv_results_['std_test_score']
params = grid_result.cv_results_['params']
for mean, stdev, param in zip(means, stds, params):
    print("%f (%f) with: %r" % (mean, stdev, param))

model_alpha = keras.models.Sequential()
model_alpha.add(keras.layers.Flatten(input_shape=X.shape[1:]))
for i in range(3):
    model_alpha.add(keras.layers.Dense(150,
                                 kernel_initializer="lecun_normal",
                                 activation="selu"))
    model_alpha.add(keras.layers.AlphaDropout(rate=0.1))

model_alpha.add(keras.layers.Dense(5, activation="softmax"))
s = 20 * len(X) // 32
learning_schedule = keras.optimizers.schedules.ExponentialDecay(0.01, s, 0.1)
optimizer=keras.optimizers.SGD(learning_rate=learning_schedule, momentum=0.95, nesterov=False)

model_alpha.compile(loss="sparse_categorical_crossentropy", optimizer=optimizer, metrics=["accuracy"])

history=model_alpha.fit(X, y, epochs=100,
          validation_data=(X_valid,y_valid),
          callbacks = early_stopping_cb, batch_size=32)

# summarize history for acc
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='lower right')
plt.show()
# summarize history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper right')
plt.show()

predictions = model_alpha.predict(X_valid)
predictions=np.argmax(predictions, axis=1)
print(classification_report(y_valid, predictions))
model_alpha.evaluate(X_valid, y_valid)

model_batch = keras.models.Sequential()
model_batch.add(keras.layers.Flatten(input_shape=X.shape[1:]))
model_batch.add(keras.layers.BatchNormalization())
for i in range(3):
    model_batch.add(keras.layers.Dense(150,
                                 kernel_initializer="he_normal",
                                 activation="elu"))
    model_batch.add(keras.layers.BatchNormalization())

model_batch.add(keras.layers.Dense(5, activation="softmax"))
s = 20 * len(X) // 32
learning_schedule = keras.optimizers.schedules.ExponentialDecay(0.01, s, 0.1)
optimizer=keras.optimizers.SGD(learning_rate=learning_schedule, momentum=0.95, nesterov=False)

model_batch.compile(loss="sparse_categorical_crossentropy", optimizer=optimizer, metrics=["accuracy"])

history=model_batch.fit(X, y, epochs=100,
          validation_data=(X_valid,y_valid),
          callbacks = early_stopping_cb, batch_size=32)

# summarize history for acc
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='lower right')
plt.show()
# summarize history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper right')
plt.show()

predictions = model_batch.predict(X_valid)
predictions=np.argmax(predictions, axis=1)
print(classification_report(y_valid, predictions))
model_batch.evaluate(X_valid, y_valid)

keras.backend.clear_session()
model = keras.models.Sequential()
model.add(keras.layers.Flatten(input_shape=X.shape[1:]))
for i in range(3):
    model.add(keras.layers.Dense(150,
                                 kernel_initializer="lecun_normal",
                                 activation="selu"))


model.add(keras.layers.Dense(5, activation="softmax"))
s = 20 * len(X) // 32
learning_schedule = keras.optimizers.schedules.ExponentialDecay(0.01, s, 0.1)
optimizer=keras.optimizers.SGD(learning_rate=learning_schedule, momentum=0.95, nesterov=False)

model.compile(loss="sparse_categorical_crossentropy", optimizer=optimizer, metrics=["accuracy"])

history=model.fit(X, y, epochs=50, batch_size=32, callbacks = early_stopping_cb, validation_data=(X_valid,y_valid))

# summarize history for acc
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='lower right')
plt.show()
# summarize history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper right')
plt.show()

df_test = pd.read_csv("./drive/MyDrive/input/mitbih_test.csv", header = None)

df_test.head()

y_test = df_test[187]

X_test = df_test.drop(columns=[187])
X_test

X_test = pipeline.fit_transform(X_test)
X_test

predictions = model.predict(X_test)
predictions=np.argmax(predictions, axis=1)
print(classification_report(y_test, predictions))
model.evaluate(X_test, y_test)

predictions = model.predict(X_test)
predictions

plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.legend(["accuracy","val_accuracy"])
plt.xlabel('Epoch')
plt.ylabel('Accuracy')

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.legend(["loss","val_loss"])
plt.xlabel('Epoch')
plt.ylabel('Loss')
