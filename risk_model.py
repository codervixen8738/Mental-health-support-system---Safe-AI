# Mental Health Risk Prediction Model using TensorFlow
import pandas as pd
import tensorflow as tf
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import os

# Set random seeds for reproducibility
np.random.seed(42)
tf.random.set_seed(42)

try:
    print("Loading and preprocessing data...")
    # Load data
    data = pd.read_csv(r'C:\Users\vaish\OneDrive\Desktop\Early detection of mental health\processed_real_data.csv')
    
    # Remove rows with missing values in key columns
    data = data.dropna(subset=['Age', 'IMC', 'risk_level'])
    print(f"Data shape after removing missing values: {data.shape}")
    
    # Features and target
    X = data[['Age', 'IMC']]
    y = data['risk_level']
    
    print(f"Feature columns: {X.columns.tolist()}")
    print(f"Target distribution: {y.value_counts().to_dict()}")
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"Training set shape: {X_train.shape}")
    print(f"Test set shape: {X_test.shape}")
    
    # Create TensorFlow model
    print("\nBuilding TensorFlow model...")
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(X_train.shape[1],)),
        tf.keras.layers.Dense(64, activation='relu', name='hidden_layer_1'),
        tf.keras.layers.Dropout(0.3, name='dropout_1'),
        tf.keras.layers.Dense(32, activation='relu', name='hidden_layer_2'),
        tf.keras.layers.Dropout(0.2, name='dropout_2'),
        tf.keras.layers.Dense(16, activation='relu', name='hidden_layer_3'),
        tf.keras.layers.Dense(3, activation='softmax', name='output_layer')
    ])
    
    # Compile model
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    print("\nModel Architecture:")
    model.summary()
    
    # Add callbacks
    callbacks = [
        tf.keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=10,
            restore_best_weights=True
        ),
        tf.keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=5,
            min_lr=0.0001
        )
    ]
    
    # Train model
    print("\nTraining model...")
    history = model.fit(
        X_train, y_train,
        epochs=100,
        batch_size=32,
        validation_data=(X_test, y_test),
        callbacks=callbacks,
        verbose=1
    )
    
    # Evaluate model
    print("\nEvaluating model...")
    test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=0)
    print(f"Test Accuracy: {test_accuracy:.4f}")
    print(f"Test Loss: {test_loss:.4f}")
    
    # Make predictions
    y_pred = model.predict(X_test, verbose=0)
    y_pred_classes = np.argmax(y_pred, axis=1)
    
    # Print classification report
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred_classes))
    
    # Print confusion matrix
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred_classes))
    
    # Save model and scaler
    print("\nSaving model and scaler...")
    model.save('mental_health_risk_model.keras')
    joblib.dump(scaler, 'scaler.pkl')
    
    print("\n" + "="*50)
    print("MODEL TRAINING COMPLETED SUCCESSFULLY!")
    print("="*50)
    print(f"Model saved as: mental_health_risk_model.keras")
    print(f"Scaler saved as: scaler.pkl")
    print(f"Final Accuracy: {test_accuracy:.2%}")
    print("="*50)
    
except Exception as e:
    print(f"Error during training: {str(e)}")
    exit(1)

# Function to make predictions on new data
def predict_risk(age, imc, model_path='mental_health_risk_model.keras', scaler_path='scaler.pkl'):
    """
    Predict mental health risk for given age and IMC values
    """
    try:
        # Load model and scaler
        if not os.path.exists(model_path) or not os.path.exists(scaler_path):
            raise FileNotFoundError("Model or scaler file not found")
            
        model = tf.keras.models.load_model(model_path)
        scaler = joblib.load(scaler_path)
        
        # Prepare input data
        input_data = np.array([[age, imc]])
        input_scaled = scaler.transform(input_data)
        
        # Make prediction
        prediction = model.predict(input_scaled, verbose=0)
        risk_level = np.argmax(prediction, axis=1)[0]
        confidence = np.max(prediction, axis=1)[0]
        
        risk_labels = {0: 'Low Risk', 1: 'Medium Risk', 2: 'High Risk'}
        
        return {
            'risk_level': risk_labels[risk_level],
            'confidence': float(confidence),
            'probabilities': {
                'Low Risk': float(prediction[0][0]),
                'Medium Risk': float(prediction[0][1]),
                'High Risk': float(prediction[0][2])
            }
        }
    except Exception as e:
        return {'error': str(e)}

# Test prediction function
if __name__ == "__main__":
    print("\nTesting prediction function...")
    example_result = predict_risk(25, 22.5)
    
    if 'error' not in example_result:
        print(f"Age: 25, IMC: 22.5")
        print(f"Predicted Risk: {example_result['risk_level']}")
        print(f"Confidence: {example_result['confidence']:.2%}")
        print("Probabilities:")
        for risk, prob in example_result['probabilities'].items():
            print(f"  {risk}: {prob:.2%}")
        print("\nModel is ready for deployment!")
    else:
        print(f"Prediction error: {example_result['error']}")