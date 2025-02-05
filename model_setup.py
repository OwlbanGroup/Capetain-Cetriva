import tensorflow as tf  # Ensure this import is added
from tensorflow.keras.models import Sequential 
from tensorflow.keras.layers import Dense, Dropout  # type: ignore
from tensorflow.keras.regularizers import L1, L1L2
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import CategoricalCrossentropy
from tensorflow.keras.metrics import Accuracy
import numpy as np
import logging  # Import logging
from web3 import Web3  # Ensure this import is added
import requests  # Import requests for API calls

# Define an enhanced model for investment predictions with early stopping and dropout
model = Sequential([
    Dense(128, activation='relu', input_shape=(3,), kernel_regularizer=L1L2(l1=0.01, l2=0.01), bias_regularizer=L1(0.01)),
    Dropout(0.2),
    Dense(64, activation='relu', kernel_regularizer=L1(0.01)),
    Dropout(0.2),
    Dense(32, activation='relu', kernel_regularizer=L1(0.01)),
    Dropout(0.2),
    Dense(16, activation='relu', kernel_regularizer=L1(0.01)),
    Dropout(0.2),
    Dense(3, activation='softmax')  # Output layer for 3 asset classes
])

model.compile(optimizer=Adam(lr=0.001), loss=CategoricalCrossentropy(), metrics=[Accuracy()])

early_stopping = EarlyStopping(monitor='val_loss', patience=10, min_delta=0.001)
model_checkpoint = ModelCheckpoint('best_model.h5', monitor='val_loss', save_best_only=True, mode='min')


# Function to train the model on historical investment data with early stopping
def train_model(historical_data, labels):
    """
    Train the model on historical investment data.
    Args:
        historical_data: Numpy array of historical investment data
        labels: Numpy array of corresponding labels
    """
    logging.info("Training model...")
    model.fit(historical_data, labels, epochs=50, batch_size=32, validation_split=0.2, callbacks=[early_stopping, model_checkpoint])
    logging.info("Model training completed.")

# Function to make predictions on new investment data
def make_prediction(new_data):
    """
    Make predictions on new investment data.
    Args:
        new_data: Numpy array of new investment data
    """
    logging.info("Making predictions...")
    predictions = model.predict(new_data)
    logging.info("Predictions completed.")
    return predictions

# Function to evaluate the model on test data
def evaluate_model(test_data, test_labels):
    """
    Evaluate the model on test data.
    Args:
        test_data: Numpy array of test data
        test_labels: Numpy array of corresponding test labels
    """
    logging.info("Evaluating model...")
    loss, accuracy = model.evaluate(test_data, test_labels)
    logging.info("Model evaluation completed.")
    return loss, accuracy

# Example usage
if __name__ == "__main__":
    # Initialize logging
    logging.basicConfig(level=logging.INFO)

    # Initialize Web3 connection (replace with your Infura or local node URL)
    w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/YOUR_NEW_INFURA_PROJECT_ID'))  # Replace with your actual Infura project ID

    # Check if connected to Ethereum
    if not w3.is_connected():
        logging.error("Failed to connect to Ethereum network.")
        raise Exception("Ethereum connection error.")
    else:
        logging.info("Connected to Ethereum network")

        # Load historical investment data and labels
        historical_data = np.load("historical_data.npy")
        labels = np.load("labels.npy")

        # Train the model
        train_model(historical_data, labels)

        # Make predictions on new investment data
        new_data = np.load("new_data.npy")
        predictions = make_prediction(new_data)

        # Evaluate the model on test data
        test_data = np.load("test_data.npy")
        test_labels = np.load("test_labels.npy")
        loss, accuracy = evaluate_model(test_data, test_labels)
        logging.info("Model evaluation completed.")
    
# Define an enhanced model for investment predictions with early stopping and dropout
model = Sequential([
    Dense(128, activation='relu', input_shape=(3,), kernel_regularizer=L1L2(l1=0.01, l2=0.01), bias_regularizer=L1(0.01)),
    Dropout(0.2),
    Dense(64, activation='relu', kernel_regularizer=L1(0.01)),
    Dropout(0.2),
    Dense(32, activation='relu', kernel_regularizer=L1(0.01)),
    Dropout(0.2),
    Dense(16, activation='relu', kernel_regularizer=L1(0.01)),
    Dropout(0.2),
    Dense(3, activation='softmax')  # Output layer for 3 asset classes
])

model.compile(optimizer=Adam(lr=0.001), loss=CategoricalCrossentropy(), metrics=[Accuracy()])

early_stopping = EarlyStopping(monitor='val_loss', patience=10, min_delta=0.001)
model_checkpoint = ModelCheckpoint('best_model.h5', monitor='val_loss', save_best_only=True, mode='min')

# Function to train the model on historical investment data with early stopping
def train_model(historical_data, labels):
    """
    Train the model on historical investment data.
    Args:
        historical_data: Numpy array of historical investment data
        labels: Numpy array of corresponding labels
    """
    logging.info("Training model...")
    model.fit(historical_data, labels, epochs=50, batch_size=32, validation_split=0.2, callbacks=[early_stopping, model_checkpoint])
    logging.info("Model training completed.")

# Function to make predictions on new investment data
def make_prediction(new_data):
    """
    Make predictions on new investment data.
    Args:
        new_data: Numpy array of new investment data
    """
    logging.info("Making predictions...")
    predictions = model.predict(new_data)
    logging.info("Predictions completed.")
    return predictions

# Function to evaluate the model on test data
def evaluate_model(test_data, test_labels):
    """
    Evaluate the model on test data.
    Args:
        test_data: Numpy array of test data
        test_labels: Numpy array of corresponding test labels
    """
    logging.info("Evaluating model...")
    loss, accuracy = model.evaluate(test_data, test_labels)
    logging.info("Model evaluation completed.")
    return loss, accuracy

# Example usage
if __name__ == "__main__":
    # Initialize logging
    logging.basicConfig(level=logging.INFO)

    # Initialize Web3 connection (replace with your Infura or local node URL)
    w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/YOUR_NEW_INFURA_PROJECT_ID'))  # Replace with your actual Infura project ID

    # Check if connected to Ethereum
    if not w3.is_connected():
        logging.error("Failed to connect to Ethereum network.")
        raise Exception("Ethereum connection error.")
    else:
        logging.info("Connected to Ethereum network")

    # Load historical investment data and labels
    historical_data = np.load("historical_data.npy")
    labels = np.load("labels.npy")

    # Train the model
    train_model(historical_data, labels)

    # Make predictions on new investment data
    new_data = np.load("new_data.npy")
    predictions = make_prediction(new_data)

    # Evaluate the model on test data
    test_data = np.load("test_data.npy")
    test_labels = np.load("test_labels.npy")
    loss, accuracy = evaluate_model(test_data, test_labels)
    logging.info("Model evaluation completed.")
    Dense(64, activation='relu', input_shape=(3,), kernel_regularizer=tf.keras.regularizers.L1(0.01)),
    tf.keras.layers.Dropout(0.2),
    Dense(32, activation='relu', kernel_regularizer=tf.keras.regularizers.L1(0.01)),
    tf.keras.layers.Dropout(0.2),
    Dense(16, activation='relu', kernel_regularizer=tf.keras.regularizers.L1(0.01)),
    tf.keras.layers.Dropout(0.2),
    Dense(3, activation='softmax')  # Output layer for 3 asset classes
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=5, min_delta=0.001)
model_checkpoint = tf.keras.callbacks.ModelCheckpoint('best_model.h5', monitor='val_loss', save_best_only=True, mode='min')

def train_model(historical_data, labels):
    logging.info("Training model...")
    model.fit(historical_data, labels, epochs=50, batch_size=32, validation_split=0.2, callbacks=[early_stopping, model_checkpoint])
def evaluate_model(test_data, test_labels):
    logging.info("Evaluating model...")
    loss, accuracy = model.evaluate(test_data, test_labels)
    logging.info("Model evaluation completed.")
    return loss, accuracyom tensorflow.keras.layers import Dense  # type: ignore
import numpy as np
import logging  # Import logging
from web3 import Web3  # Ensure this import is added
import requests  # Import requests for API calls
# Define an enhanced model for investment predictions with early stopping and dropout
model = Sequential([
Dense(128, activation='relu', input_shape=(3,), kernel_regularizer=tf.keras.regularizers.L1L2(l1=0.01, l2=0.01), bias_regularizer=tf.keras.regularizers.L2(0.01))    tf.keras.layers.Dropout(0.2),
    Dense(32, activation='relu', kernel_regularizer=tf.keras.regularizers.L1(0.01)),
    tf.keras.layers.Dropout(0.2),
    Dense(16, activation='relu', kernel_regularizer=tf.keras.regularizers.L1(0.01)),
    tf.keras.layers.Dropout(0.2),
    Dense(3, activation='softmax')  # Output layer for 3 asset classes
])

# Compile the model for investment predictions with early stopping
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Define early stopping callback
early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=5, min_delta=0.001)

# Function to train the model on historical investment data with early stopping
def train_model(historical_data, labels):
    """
    Train the model on historical investment data.
    Args:
        historical_data: Numpy array of historical investment data
        labels: Numpy array of corresponding labels
    """
    logging.info("Training model...")
    model.fit(historical_data, labels, epochs=50, batch_size=32, validation_split=0.2, callbacks=[early_stopping])
    logging.info("Model training completed.")# Define an enhanced model for investment predictions with early stopping and dropout
# Define an enhanced model for investment predictions with early stopping and dropout
model = Sequential([
    Dense(64, activation='relu', input_shape=(3,), kernel_regularizer=tf.keras.regularizers.L1(0.01)),
    tf.keras.layers.Dropout(0.2),
    Dense(32, activation='relu', kernel_regularizer=tf.keras.regularizers.L1(0.01)),
    tf.keras.layers.Dropout(0.2),
    Dense(16, activation='relu', kernel_regularizer=tf.keras.regularizers.L1(0.01)),
    tf.keras.layers.Dropout(0.2),
    Dense(3, activation='softmax')  # Output layer for 3 asset classes
])

# Compile the model for investment predictions with early stopping
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Define early stopping callback
early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=5, min_delta=0.001)

# Define model checkpoint callback
model_checkpoint = tf.keras.callbacks.ModelCheckpoint('best_model.h5', monitor='val_loss', save_best_only=True, mode='min')

# Function to train the model on historical investment data with early stopping
def train_model(historical_data, labels):
    """
    Train the model on historical investment data.
    Args:
        historical_data: Numpy array of historical investment data
        labels: Numpy array of corresponding labels
    """
    logging.info("Training model...")
    model.fit(historical_data, labels, epochs=50, batch_size=32, validation_split=0.2, callbacks=[early_stopping, model_checkpoint])
    logging.info("Model training completed.")

# Function to make predictions on new investment data
def make_prediction(new_data):
    """
    Make predictions on new investment data.
    Args:
        new_data: Numpy array of new investment data
    """
    logging.info("Making predictions...")
    predictions = model.predict(new_data)
    logging.info("Predictions completed.")
    return predictions

# Function to evaluate the model on test data
def evaluate_model(test_data, test_labels):
    """
    Evaluate the model on test data.
    Args:
        test_data: Numpy array of test data
        test_labels: Numpy array of corresponding test labels
    """
    logging.info("Evaluating model...")
    loss, accuracy = model.evaluate(test_data, test_labels)
    logging.info("Model evaluation completed.")
    return loss, accuracy

# Example usage
if __name__ == "__main__":
    # Initialize logging
    logging.basicConfig(level=logging.INFO)

    # Initialize Web3 connection (replace with your Infura or local node URL)
    w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/YOUR_NEW_INFURA_PROJECT_ID'))  # Replace with your actual Infura project ID

    # Check if connected to Ethereum
    if not w3.is_connected():
        logging.error("Failed to connect to Ethereum network.")
        raise Exception("Ethereum connection error.")
    else:
        logging.info("Connected to Ethereum network")

    # Load historical investment data and labels
    historical_data = np.load("historical_data.npy")
    labels = np.load("labels.npy")

    # Train the model
    train_model(historical_data, labels)

    # Make predictions on new investment data
    new_data = np.load("new_data.npy")
    predictions = make_prediction(new_data)

    # Evaluate the model on test data
    test_data = np.load("test_data.npy")
    test_labels = np.load("test_labels.npy")
    loss, accuracy = evaluate_model(test_data, test_labels)
    logging.info("Connected to Ethereum network")
else:
    logging.info("Connected to Ethereum network")# Define an enhanced model for investment predictions with early stopping and dropout
model = Sequential([
    Dense(64, activation='relu', input_shape=(3,), kernel_regularizer=tf.keras.regularizers.L1(0.01)),
    tf.keras.layers.Dropout(0.2),
    Dense(32, activation='relu', kernel_regularizer=tf.keras.regularizers.L1(0.01)),
    tf.keras.layers.Dropout(0.2),
    Dense(16, activation='relu', kernel_regularizer=tf.keras.regularizers.L1(0.01)),
    tf.keras.layers.Dropout(0.2),
    Dense(3, activation='softmax')  # Output layer for 3 asset classes
])

# Compile the model for investment predictions with early stopping
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Define early stopping callback
early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=5, min_delta=0.001)

# Function to train the model on historical investment data with early stopping
def train_model(historical_data, labels):
    """
    Train the model on historical investment data.
    Args:
        historical_data: Numpy array of historical investment data
        labels: Numpy array of corresponding labels
    """
    logging.info("Training model...")
    model.fit(historical_data, labels, epochs=50, batch_size=32, validation_split=0.2, callbacks=[early_stopping])
    logging.info("Model training completed.")

# Function to make predictions on new investment data
def make_prediction(new_data):
    """
    Make predictions on new investment data.
    Args:
        new_data: Numpy array of new investment data
    """
    logging.info("Making predictions...")
    predictions = model.predict(new_data)
    logging.info("Predictions completed.")
    return predictions

# Function to evaluate the model on test data
def evaluate_model(test_data, test_labels):
    """
    Evaluate the model on test data.
    Args:
        test_data: Numpy array of test data
        test_labels: Numpy array of corresponding test labels
    """
    logging.info("Evaluating model...")
    loss, accuracy = model.evaluate(test_data, test_labels)
    logging.info("Model evaluation completed.")
    return loss, accuracy

# Example usage
if __name__ == "__main__":
    # Initialize logging
    logging.basicConfig(level=logging.INFO)

    # Initialize Web3 connection (replace with your Infura or local node URL)
    w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/YOUR_NEW_INFURA_PROJECT_ID'))  # Replace with your actual Infura project ID

    # Check if connected to Ethereum
    if not w3.is_connected():
        logging.error("Failed to connect to Ethereum network.")
        raise Exception("Ethereum connection error.")
    else:
        logging.info("Connected to Ethereum network")

    # Load historical investment data and labels
    historical_data = np.load("historical_data.npy")
    labels = np.load("labels.npy")

    # Train the model
    train_model(historical_data, labels)

    # Make predictions on new investment data
    new_data = np.load("new_data.npy")
    predictions = make_prediction(new_data)

    # Evaluate the model on test data
    test_data = np.load("test_data.npy")
    test_labels = np.load("test_labels.npy")
    loss, accuracy = evaluate_model(test_data, test_labels)
    logging.info("Connected to Ethereum network")
else:
    logging.info("Connected to Ethereum network")
