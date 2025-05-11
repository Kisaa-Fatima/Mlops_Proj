import pickle
import numpy as np
import sys
import os

def resave_model():
    try:
        print(f"Python version: {sys.version}")
        print(f"Numpy version: {np.__version__}")
        
        # Load the existing model
        print("Attempting to load model...")
        with open("weather_model.pkl", 'rb') as f:
            model = pickle.load(f)
        print("Model loaded successfully")
        print(f"Model type: {type(model)}")
        print(f"Model shape: {model.shape if hasattr(model, 'shape') else 'N/A'}")
        print(f"Model dtype: {model.dtype if hasattr(model, 'dtype') else 'N/A'}")
        
        # Create a new numpy array preserving the original dtype
        if isinstance(model, np.ndarray):
            print("Converting numpy array to ensure compatibility...")
            # Keep the original dtype instead of forcing float64
            new_model = np.array(model)
        else:
            print("Converting to numpy array...")
            new_model = np.array(model)
        
        print(f"New model dtype: {new_model.dtype}")
        
        # Save with protocol 4 for better compatibility
        print("Saving new model...")
        with open("weather_model_new.pkl", 'wb') as f:
            pickle.dump(new_model, f, protocol=4)
        
        print("Model successfully resaved as weather_model_new.pkl")
        
        # Verify the saved model can be loaded
        print("Verifying saved model...")
        with open("weather_model_new.pkl", 'rb') as f:
            test_load = pickle.load(f)
        print("Verification successful!")
        print(f"Verified model dtype: {test_load.dtype}")
        
    except Exception as e:
        print(f"Error resaving model: {str(e)}")
        print(f"Error type: {type(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    resave_model() 