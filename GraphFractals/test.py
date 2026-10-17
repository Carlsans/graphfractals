import numpy as np
from scipy.stats import entropy


def image_entropy(image):
    # Convert image to grayscale if it's not already
    if len(image.shape) == 3:
        image = np.mean(image, axis=2)

    # Calculate histogram of pixel intensities
    hist, _ = np.histogram(image, bins=256, range=(0, 255))

    # Normalize histogram to obtain probabilities
    prob = hist / np.sum(hist)

    # Compute entropy
    ent = entropy(prob, base=2)

    return ent


# Example usage
image = np.random.randint(0, 256, size=(100, 100))
entropy_value = image_entropy(image)
print("Entropy:", entropy_value)