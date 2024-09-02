from minisom import MiniSom
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import numpy as np
import matplotlib.pyplot as plt

# Load the extracted features
df = pd.read_csv('C:/Users/lab/Desktop/Git/Mano_prostetica_Labrobcog_CInC/programas/emg_features.csv')
test = pd.read_csv('C:/Users/lab/Desktop/Git/Mano_prostetica_Labrobcog_CInC/programas/test.csv')

# Prepare the data for SOM
X = df[['peak_height']].values
#X = df[['peak_height', 'peak_width']].values
y_train = df['label'].values  # Assumed 'label' is the column for true labels in training data
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# Prepare the data for test
Y = test[['peak_height']].values
#Y = test[['peak_height', 'peak_width']].values
y_test = test['label'].values  # Assumed 'label' is the column for true labels in test data
Y_scaled = scaler.transform(Y)  # Use the same scaler fitted on X

# Encode labels as integers
label_encoder = LabelEncoder()
y_train_encoded = label_encoder.fit_transform(y_train)
y_test_encoded = label_encoder.transform(y_test)

# Initialize and train the SOM
som = MiniSom(x=5, y=5, input_len=1, sigma=0.3, learning_rate=0.5)
som.random_weights_init(X)
som.train_random(data=X, num_iteration=1000)

# Guardar los pesos de la SOM
weights = som.get_weights()
np.save('som_weights.npy', weights)

weights = np.load('som_weights.npy')

# Convierte los pesos a un formato C/C++
weights_c_format = weights.tolist()
#print(weights_c_format)

# Guarda los pesos en un archivo de texto
with open('som_weights.h', 'w') as f:
    f.write('float som_weights[5][5][1] = ' + str(weights_c_format).replace('[', '{').replace(']', '}') + ';')

plt.figure(figsize=(10, 10))
for i, x in enumerate(X):
    w = som.winner(x)
    plt.text(w[0] + 0.5, w[1] + 0.5, df['label'][i],
             ha='center', va='center',
             bbox=dict(facecolor='white', alpha=0.5, lw=0))

temp = som.winner(Y[0])

plt.pcolor(som.distance_map().T, cmap='bone_r')
plt.scatter(temp[0] + 0.25 , temp[1] + 0.25, s=200)
plt.show()


# Map each training sample to its closest neuron
mapped = [tuple(som.winner(x)) for x in X]
labels_map = {}
for i, m in enumerate(mapped):
    if m not in labels_map:
        labels_map[m] = []
    labels_map[m].append(y_train_encoded[i])

# Determine the most frequent label for each neuron
for m in labels_map:
    labels_map[m] = np.argmax(np.bincount(labels_map[m]))

# Predict labels for the test data
predicted_labels = []
for x in Y:
    winner = tuple(som.winner(x))
    predicted_labels.append(labels_map.get(winner, -1))

# Decode predicted labels back to original string labels
predicted_labels = label_encoder.inverse_transform(predicted_labels)

# Calculate the confusion matrix
cm = confusion_matrix(y_test, predicted_labels)

# Display the confusion matrix
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=label_encoder.classes_)
disp.plot(cmap=plt.cm.Greens)
plt.show()
