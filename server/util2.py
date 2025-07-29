import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np

__image_model = None

def load_image_model():
    global __image_model
    if __image_model is None:
        # Corrected line without the extra assignment
        __image_model = tf.keras.models.load_model(r"C:\pro\server\artifacts\wall_damage_model.keras")  
        print("Image model loaded successfully.")

def predict_damage(images):
    damage_predictions = []

    for img_path in images:
        img = image.load_img(img_path, target_size=(224, 224))  # Resize as needed for your model
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension

        predictions = __image_model.predict(img_array)
        damage_class = predictions.argmax()  # Assuming class labels are integers

        # Example damage classes - adjust as per your model's classes
        damage_classes = ['No Damage', 'Cracks', 'Mold', 'Peeling Paint','Water damage']
        damage_prediction = damage_classes[damage_class]
        
        # Debugging: print prediction details
        print(f"Prediction for {img_path}: {damage_prediction}")
        
        damage_predictions.append({
            'image_url': img_path,
            'damage_prediction': damage_prediction
        })

    return damage_predictions

if __name__ == '__main__':
    load_image_model()
    # Test with multiple images
    print(predict_damage(['sample_image1.jpg', 'sample_image2.jpg']))
