# How to generate models

## Create the dataset

In order to create the dataset, you need image pairs of Edge + Color. Find a suitable dataset of images then do the following.

1. Generate the Edge image by using the edge-detector scripts. Make sure to place images within a test folder. 

```python run.py --input_dir colored_images/bracelet/train/ --output_dir edge_images/bracelet/train/```

2. Combine the Edge and Colored images. This will generate a datasets/edges2bracelets/test folder, do not specify test.

``` python combine_A_and_B.py --fold_A edge-detection/colored_images/bracelet/ --fold_B edge-detection/edge_images/bracelet/ --fold_AB datasets/edges2bracelets```


## 2. Train the model with pix2pix

## 3. Test and export the model with pix2pix

## 3b. Test the model with process
