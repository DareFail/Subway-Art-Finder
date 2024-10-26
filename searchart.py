
import numpy as np
import tensorflow as tf
import cv2
import os
import sys
import pickle
import csv
from annoy import AnnoyIndex

# Load a pre-trained EfficientNet model
efficientnet_model = tf.keras.applications.EfficientNetB4(
    include_top=False, weights='imagenet', input_shape=(224, 224, 3))
model = tf.keras.Sequential([
    efficientnet_model,
    tf.keras.layers.GlobalAveragePooling2D(),
])

def extract_features(image):
    img = tf.keras.preprocessing.image.load_img(image, target_size=(224, 224))
    img = tf.keras.preprocessing.image.img_to_array(img)
    img = tf.keras.applications.efficientnet.preprocess_input(img)
    img = np.expand_dims(img, axis=0)
    features = model.predict(img)
    features /= np.linalg.norm(features, axis=-1, keepdims=True)
    return features

database_directory = sys.argv[1]
index_file = "my_index.ann"
features_file = "database_features.pkl"
filenames_file = "database_filenames.pkl"

# Check if index file exists
if os.path.exists(index_file):
    # Load the index, features and filenames
    with open(features_file, 'rb') as f:
        database_features = pickle.load(f)
    with open(filenames_file, 'rb') as f:
        database_filenames = pickle.load(f)
        
    feature_dim = len(database_features[0])
    annoy_index = AnnoyIndex(feature_dim, 'angular')
    annoy_index.load(index_file)
else:
    # Create the index and save features and filenames
    database_features = []
    database_filenames = []
    for filename in os.listdir(database_directory):
        if filename.endswith(".jpg"):
            image_path = os.path.join(database_directory, filename)
            features = extract_features(image_path)
            database_features.append(features.flatten())
            database_filenames.append(filename)
    
    num_trees = 200 
    feature_dim = len(database_features[0])
    annoy_index = AnnoyIndex(feature_dim, 'angular')

    for i, feature in enumerate(database_features):
        annoy_index.add_item(i, feature)
    
    annoy_index.build(num_trees)
    
    # Save the index, features and filenames
    annoy_index.save(index_file)
    with open(features_file, 'wb') as f:
        pickle.dump(database_features, f)
    with open(filenames_file, 'wb') as f:
        pickle.dump(database_filenames, f)

query_image_path = sys.argv[2]
query_features = extract_features(query_image_path).flatten()
top_n = 5

similar_indices = annoy_index.get_nns_by_vector(query_features, top_n)

query_image = cv2.imread(query_image_path)
predicted_art = False
predited_art_distance = 0
for i, index in enumerate(similar_indices):
    similar_image_filename = database_filenames[index]
    similar_image_path = os.path.join(database_directory, similar_image_filename)
    similar_image = cv2.imread(similar_image_path)
    distance = np.linalg.norm(query_features - database_features[index])
    if abs(1.0 - distance) < 0.15:
        if predicted_art:
            if abs(1.0 - distance) < predited_art_distance:
                predicted_art = similar_image_path
                predited_art_distance = distance
        else:
            predicted_art = similar_image_path
            predited_art_distance = distance
    cv2.imshow(f"Potential Art {i + 1}", similar_image)


if not predicted_art:
    print("Your photo was not close enough to any existing art.")
else:
    unique_id = predicted_art.split('/')[1].split('_')[0]

    # Open mta.csv
    with open('mta.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)  # get the header of the csv

        # Find Unique ID and return the whole row
        for row in reader:
            if row[0] == unique_id:
                print("")
                print("This is '" + row[5] + "' by " + row[4] + " made with " + row[7] + " in " + row[6])
                print("at station " + row[2] + "with subway lines " + row[3])
                print("")
                print("More information: " + row[8])
                break


cv2.waitKey(20000)
cv2.destroyAllWindows()
    

