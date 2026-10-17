import numpy as np
from PIL import Image
from matplotlib import cm, pyplot as plt
from scipy.stats import entropy
from io import BytesIO
import os
def create_image_comparision_tensor(input):
    global image_comparison_tensor
    compare_image_path = os.path.dirname(os.path.realpath(__file__))+ "/compareme.jpg"
    print(input.shape)
    img = Image.open(compare_image_path)
    # Convert the image to grayscale
    img = img.convert('L')
    # Resize the image
    img = img.resize(input.shape)
    img.save(os.path.dirname(os.path.realpath(__file__))+ "/comparemeresized.jpg")
    # Convert the image to a numpy array
    img_array = np.array(img)
    # Normalize the array (scale pixel values to the range 0-1)
    image_comparison_tensor = img_array / 255.0
def image_comparision_loss(input):
    global image_comparison_tensor
    if not 'image_comparison_tensor' in globals():
        create_image_comparision_tensor(input)
    #print(image_comparison_tensor)
    if not image_comparison_tensor.shape == input.shape:
        return 0
    imagemin, imagemax = np.min(input), np.max(input)
    if imagemin == imagemax:
        print("Image contain only 1 value")
        return 0
    normalized_input = (input - imagemin) / (imagemax - imagemin)
    comparedtensor = np.mean((np.abs(image_comparison_tensor - normalized_input)))
    print("comparedtensor",comparedtensor)
    return 1 - comparedtensor
def image_compression_based_information(image):
    print(image.shape)
    if len(image.shape) == 3:
        image = np.mean(image, axis=2)
    print(image)
    imagemin,imagemax = np.min(image),np.max(image)
    if imagemin == imagemax:
        print("Image contain only 1 value")
        return 0
    np_image = (image - imagemin)/(imagemax-imagemin)

    #print(imagemin,imagemax,np_image)
    img_file = BytesIO()
    #plt.imsave(img_file, np_image, cmap='Greys')
    img = Image.fromarray(np_image, mode='I')
    img.save(img_file, format='PNG',optimize=True)
    #image.save(img_file, 'png', quality='keep')
    image_file_size = img_file.tell()
    informationcontentbypixel = image_file_size/(np_image.shape[0]*np_image.shape[1])
    print("informationcontentbypixel",informationcontentbypixel)
    return informationcontentbypixel
def image_entropy(image):
    # Convert image to grayscale if it's not already
    # if image.shape[0] > 1000 or image.shape[1] > 1000:
    #     print("Image to big for entropy mesure")
    #     return 0
    if len(image.shape) == 3:
        image = np.mean(image, axis=2)
    print(image.shape)
    splittedimagelist = [image[0:image.shape[0]//2][:],image[image.shape[0]//2+1:][:],image[:][0:image.shape[1]//2],image[:][image.shape[1]//2+1:]]
    mixedentropy = 1
    relucut = 2
    # Calculate histogram of pixel intensities
    for splittedimage in splittedimagelist:
        try:
            hist, _ = np.histogram(splittedimage, bins=256, range=(0, 255))
        except Exception:
            print(image)
            raise
        # Normalize histogram to obtain probabilities
        prob = hist / np.sum(hist)

        # Compute entropy
        ent = entropy(prob, base=2)
        mixedentropy = np.abs(ent-relucut) * mixedentropy

    return ent
