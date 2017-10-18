import numpy as np

import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Merge
from keras.layers import Conv1D, Conv2D
from keras.layers import MaxPooling2D, MaxPooling1D, GlobalAveragePooling1D
from keras.optimizers import SGD
from sklearn.model_selection import train_test_split


nfreq=16
ntime=250

# Generate dummy data
x_train = np.random.random((100, 100, 100, 3))
y_train = keras.utils.to_categorical(np.random.randint(10, size=(100, 1)), num_classes=10)
x_test = np.random.random((20, 100, 100, 3))
y_test = keras.utils.to_categorical(np.random.randint(10, size=(20, 1)), num_classes=10)

fn = './data/_data_nt250_nf16_dm0_snrmax200.npy'
f = load(fn)
d, y = f[:, :-1], f[:, -1]

d_train, y_train = (f[::10, :-1]).astype(np.float32), (f[::10, -1]).astype(np.int32)
d_test, y_test = (f[1::10, :-1]).astype(np.float32), (f[1::10, -1]).astype(np.int32)

d_train = d_train[..., None].reshape(-1, 16, 250, 1)
d_test = d_test[..., None].reshape(-1, 16, 250, 1)

# Turn these into categorical vectors
y_train_cat = keras.utils.to_categorical(y_train)
y_test_cat = keras.utils.to_categorical(y_test)

train_data, eval_data, train_labels, eval_labels = \
              train_test_split(d, y, train_size=0.75)

train_data = train_data.reshape(-1, nfreq, ntime)[..., None]
eval_data = eval_data.reshape(-1, nfreq, ntime)[..., None]

def construct_conv2d(features_only=False, fit=False):
	model = Sequential()
	# this applies 32 convolution filters of size 3x3 each.
	model.add(Conv2D(32, (5, 5), activation='relu', input_shape=(16, 250, 1)))
	#model.add(Conv2D(32, (3, 3), activation='relu'))
	model.add(MaxPooling2D(pool_size=(2, 2)))
	model.add(Dropout(0.4))

	model.add(Conv2D(64, (5, 5), activation='relu'))
	model.add(MaxPooling2D(pool_size=(2, 2)))
	model.add(Dropout(0.4))
	model.add(Flatten())
	model.add(Dense(1024, activation='relu'))

	if features_only is True:
		return model

	model.add(Dense(1024, activation='relu'))
	model.add(Dropout(0.5))
	model.add(Dense(2, activation='softmax'))

	sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
	model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

	if fit is True:
		model.fit(d_train, y_train, batch_size=32, epochs=10)
	#score = model.evaluate(d_test, y_test, batch_size=32)

	return model 

def construct_conv1d(features_only=False, fit=False):

	model = Sequential()
	model.add(Conv1D(64, 3, activation='relu', input_shape=(250, 1)))
	model.add(Conv1D(64, 3, activation='relu'))
	model.add(MaxPooling1D(3))
	model.add(Conv1D(128, 3, activation='relu'))
	model.add(Conv1D(128, 3, activation='relu'))
	model.add(GlobalAveragePooling1D())

	if features_only is True:
		return model

	model.add(Dropout(0.5))
	model.add(Dense(2, activation='sigmoid'))

	model.compile(loss='binary_crossentropy',
	               optimizer='rmsprop',
	               metrics=['accuracy'])

	if fit is True:
		model.fit(d_train.mean(1), y_train, batch_size=16, epochs=10)
		#score = model.evaluate(d_test.mean(1), y_test, batch_size=16)

	return model

def merge_models(left_branch, right_branch):
	model = Sequential()
	model.add(Merge([left_branch, right_branch], mode = 'concat'))
	#model.add(Dense(256, activation='relu'))
	model.add(Dense(1, init = 'normal', activation = 'sigmoid'))
	sgd = SGD(lr = 0.1, momentum = 0.9, decay = 0, nesterov = False)
	model.compile(loss = 'binary_crossentropy', optimizer = sgd, metrics = ['accuracy'])

	return model

#	seed(2017)
#	model.fit([X1, X2], Y.values, batch_size = 2000, nb_epoch = 100, verbose = 1)


m.fit([d_train.mean(1), d_train], y_train, batch_size = 2000, nb_epoch = 100, verbose = 1)



