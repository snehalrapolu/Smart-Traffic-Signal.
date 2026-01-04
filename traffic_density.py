"""
Traffic Density Estimation Module
Uses classical computer vision techniques to estimate traffic density from images.
"""
import cv2
import numpy as np


def estimate_traffic_density(image_path):
    """
    Estimates traffic density from an image using foreground occupancy estimation.
    
    Steps:
    1. Convert image to grayscale
    2. Apply thresholding to detect vehicles (foreground)
    3. Count occupied pixels
    4. Return density score
    
    Args:
        image_path: Path to the input image
        
    Returns:
        float: Density score (0.0 to 1.0, where 1.0 is maximum density)
    """
    try:
        # Read the image
        image = cv2.imread(image_path)
        
        if image is None:
            raise ValueError(f"Could not read image from {image_path}")
        
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply adaptive thresholding to detect vehicles
        # This separates foreground (vehicles) from background (road)
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Alternative: Use adaptive thresholding for better results with varying lighting
        # binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        #                                cv2.THRESH_BINARY, 11, 2)
        
        # Count white pixels (foreground/vehicles)
        # In binary image, white pixels (255) represent detected objects
        total_pixels = binary.shape[0] * binary.shape[1]
        white_pixels = np.sum(binary == 255)
        
        # Calculate density as ratio of occupied pixels
        density = white_pixels / total_pixels
        
        # Normalize to 0-1 range (clamp to prevent outliers)
        density = min(1.0, max(0.0, density))
        
        return float(density)
        
    except Exception as e:
        print(f"Error processing image {image_path}: {str(e)}")
        return 0.0


def estimate_density_from_array(image_array):
    """
    Estimates traffic density from an image array (numpy array).
    
    Args:
        image_array: numpy array representing the image (BGR format)
        
    Returns:
        float: Density score (0.0 to 1.0)
    """
    try:
        # Convert to grayscale
        if len(image_array.shape) == 3:
            gray = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)
        else:
            gray = image_array
        
        # Apply thresholding
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Count white pixels
        total_pixels = binary.shape[0] * binary.shape[1]
        white_pixels = np.sum(binary == 255)
        
        # Calculate density
        density = white_pixels / total_pixels
        density = min(1.0, max(0.0, density))
        
        return float(density)
        
    except Exception as e:
        print(f"Error processing image array: {str(e)}")
        return 0.0

