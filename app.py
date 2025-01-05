import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import numpy as np

# Define a simple model
model = Sequential([
    Dense(10, activation='relu', input_shape=(3,)),
    Dense(10, activation='relu'),
    Dense(1, activation='sigmoid')
])

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Dummy data
X = np.array([[0, 1, 2], [1, 2, 3], [2, 3, 4]])
y = np.array([0, 1, 0])

# Train the model
model.fit(X, y, epochs=10)

# Make predictions
predictions = model.predict(X)
print(predictions); /bin/activate;  # For Unix or MacOS
.\venv\Scripts\activate   # For Windows+source venv/bin/activate  # For Unix or MacOS
source venv/bin/activate;  # For Unix or MacOS
.\venv\Scripts\activate   # For Windows\venv\Scripts\activatesource venv/bin/activateimport tensorflow as tf as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import numpy as np

# Define a simple model
model = Sequential([
    Dense(10, activation='relu', input_shape=(3,)),
    Dense(10, activation='relu'),
    Dense(1, activation='sigmoid')
])

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Dummy data
X = np.array([[0, 1, 2], [1, 2, 3], [2, 3, 4]])
y = np.array([0, 1, 0])

# Train the model
model.fit(X, y, epochs=10)

# Make predictions
predictions = model.predict(X)
print(predictions)
