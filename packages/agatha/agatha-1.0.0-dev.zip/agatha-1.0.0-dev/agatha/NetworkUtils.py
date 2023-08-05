from sklearn.metrics import mean_squared_error
import math
import os
import gc
import numpy as np
from keras.layers import Dense, LSTM, Activation, Dropout, ActivityRegularization, TimeDistributed, AveragePooling1D, Flatten
from keras.models import Sequential, model_from_json

os.environ['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'
os.environ['CUDA_VISIBLE_DEVICES'] = '1'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# fix random seed for reproducibility purposes
np.random.seed(7)

def getModel(trainX, trainY, testX, testY, model_path, weights_path, epochs=100, batch_size=16, look_back=1):
	'''
	If the model and weights already exist, load them from the cache
	If the model and weights DO NOT exist, then create and fit the model, saving the weights and model
	to the specified model_path and weights_path
	:param trainX: The train data along the x axis
	:param trainY: The train data along the y axis
	:param testX: The test data along the x axis
	:param testY: The test data along the y axis
	:param model_path: The path to either read or save the model
	:param weights_path: The path to either read or save the weights
	:param epochs: The number of epochs used for training (default is 100)
	:param batch_size: The batch size (default is 32)
	:param look_back: The look back value (default 1, should always be the same as the  dimenstion of your trainX data)
	:return:  The model
	'''
	if os.path.exists(model_path):
		json_file = open(model_path, 'r')
		loaded_model_json = json_file.read()
		json_file.close()
		model = model_from_json(loaded_model_json)
		model.load_weights(weights_path)
		print("Loaded model from {}".format(model_path))
	else:
		model = Sequential()
		model.add(LSTM(64, input_shape=(1, look_back), return_sequences=True, implementation=1))
		# model.add(LSTM(16, input_shape=(1, look_back), return_sequences=True, implementation=1))
		# model.add(LSTM(8, input_shape=(1, look_back), return_sequences=True, implementation=1))
		model.add(LSTM(8, input_shape=(1, look_back), return_sequences=False, implementation=1, activation='tanh'))
		model.add(Dense(1, kernel_initializer='normal', activation='tanh'))
		model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
		print(trainX.shape)
		model.fit(trainX, trainY, epochs=epochs, batch_size=batch_size, validation_data=(testX, testY), verbose=2)

		if not os.path.exists(model_path):
			# serialize model to JSON
			model_json = model.to_json()
			with open(model_path, "w") as json_file:
				json_file.write(model_json)
			# serialize weights to HDF5
			model.save_weights(weights_path)
			print("Saved model to {}".format(model_path))

		print("Collecting garbage.")
		gc.collect()

	return model


def invert_predictions(trainPredict, testPredict, trainY, testY, scaler):
	trainPredict = scaler.inverse_transform(trainPredict)
	trainY = scaler.inverse_transform([trainY])
	testPredict = scaler.inverse_transform(testPredict)
	testY = scaler.inverse_transform([testY])
	return trainPredict, testPredict, trainY, testY


def scorePrediction(trainPredict, testPredict, trainY, testY):
	# calculate root mean squared error
	trainScore = math.sqrt(mean_squared_error(trainY[0], trainPredict[:, 0]))
	print('Train Score: %.2f RMSE' % (trainScore))
	testScore = math.sqrt(mean_squared_error(testY[0], testPredict[:, 0]))
	print('Test Score: %.2f RMSE' % (testScore))
	return trainPredict, testPredict


def predictFuture(model, initialPredictionData, num_days, scaler):
	predictionXData = initialPredictionData
	predictions = []
	for i in range(0, num_days):
		futurePredict = model.predict(predictionXData)
		predictions.append(scaler.inverse_transform(futurePredict)[0])
		# shift everything to the right
		predictionXData = np.roll(predictionXData, 1)
		# place future predict at beginning of array
		predictionXData[0][0][0] = futurePredict[0][0]

	return predictions

def getOptimalNumHiddenNeurons(training_data_size, num_input_neurons, num_output_neurons):
	return math.floor(training_data_size/(5*(num_input_neurons + num_output_neurons)))



def calculatePercentChange(future_price, current_price):
	if future_price > current_price:
		percent_change = current_price / future_price[0]
	elif future_price < current_price:
		percent_change = -(current_price / future_price[0])
	else:
		percent_change = 0
	return percent_change


def calculateMomentum(future_data, historic_data):
	return future_data - historic_data


def determineAction(momentum, threshold):
	if momentum <= threshold and momentum >= -threshold:
		return 'HOLD'
	elif momentum > 0:
		return 'BUY'
	elif momentum < 0:
		return 'SELL'