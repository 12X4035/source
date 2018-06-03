import numpy as np
import matplotlib.pyplot as plt
from keras import models


def layer_vis(model, x_test, layer_num, images_per_row, img_num):
    
    layer_num = layer_num
    img_num = img_num
    
    layer_outputs = [layer.output for layer in model.layers[:layer_num]]
    activation_model = models.Model(inputs=model.input, outputs=layer_outputs)
    select_img = x_test[img_num]
    img = np.expand_dims(select_img, axis=0)
    activations = activation_model.predict(img)
    first_layer_activation = activations[0]
    
    # These are the names of the layers, so can have them as part of our plot
    layer_names = []
    for layer in model.layers[:layer_num]:
        layer_names.append(layer.name)

    images_per_row = images_per_row

    # Now let's display our feature maps
    for layer_name, layer_activation in zip(layer_names, activations):
    # This is the number of features in the feature map
        n_features = layer_activation.shape[-1]

    # The feature map has shape (1, size, size, n_features)
        size = layer_activation.shape[1]

    # We will tile the activation channels in this matrix
        n_cols = n_features // images_per_row
        display_grid = np.zeros((size * n_cols, images_per_row * size))

    # We'll tile each filter into this big horizontal grid
        for col in range(n_cols):
            for row in range(images_per_row):
                channel_image = layer_activation[0,
                                                 :, :,
                                                 col * images_per_row + row]
            # Post-process the feature to make it visually palatable
                channel_image -= channel_image.mean()
                channel_image /= channel_image.std()
                channel_image *= 64
                channel_image += 128
                channel_image = np.clip(channel_image, 0, 255).astype('uint8')
                display_grid[col * size : (col + 1) * size,
                             row * size : (row + 1) * size] = channel_image

    # Display the grid
        scale = 1. / size
        plt.figure(figsize=(scale * display_grid.shape[1],
                            scale * display_grid.shape[0]))
        plt.title(layer_name)
        plt.grid(False)
        plt.imshow(display_grid, aspect='auto', cmap='viridis')

    plt.show()

    return select_img