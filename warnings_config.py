# Warnings Configuration for AI Travel Planner
# This file suppresses common warnings from ML libraries

import warnings
import os

# Suppress TensorFlow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
warnings.filterwarnings('ignore', category=FutureWarning, module='tensorflow')
warnings.filterwarnings('ignore', category=DeprecationWarning, module='tensorflow')

# Suppress Transformers warnings
warnings.filterwarnings('ignore', category=FutureWarning, module='transformers')
warnings.filterwarnings('ignore', category=UserWarning, module='transformers')

# Suppress Keras warnings
warnings.filterwarnings('ignore', category=FutureWarning, module='keras')
warnings.filterwarnings('ignore', category=DeprecationWarning, module='keras')

# Suppress general warnings for cleaner output
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', category=DeprecationWarning)

print("🔇 Warnings suppressed for clean output") 