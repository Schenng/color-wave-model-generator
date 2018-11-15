# How to generate models

## Create the dataset

In order to create the dataset, you need image pairs of Edge + Color. Find a suitable dataset of images then do the following.

1. Generate the Edge image by using the edge-detector scripts. Make sure to place images within a test folder. 

```python run.py --input_dir colored_images/bracelet/train/ --output_dir edge_images/bracelet/train/```

2. Combine the Edge and Colored images. This will generate a datasets/edges2bracelets/test folder, do not specify test.

``` python combine_A_and_B.py --fold_A edge-detection/colored_images/bracelet/ --fold_B edge-detection/edge_images/bracelet/ --fold_AB datasets/edges2bracelets```


## 2. Train the model with pix2pix

1. Start the visdom server 
``` python -m visdom.server```

2. Train the model. May need to switch the direction
``` python train.py --dataroot ./datasets/edges2bracelets --name edges2bracelets_pix2pix --model pix2pix --direction BtoA ```

## 3. Test and export the model with pix2pix

At this stage, we are testing and exporting the ENTIRE model (not state dict). 

1. Create a folder the test folder within `datasets/edges2bracelets/test(create this directory)` with a test image.

2. Run the following to ensure the model works.

```python test.py --dataroot ./datasets/edges2bracelets --name edges2bracelets_pix2pix --model test --netG unet_256 --direction BtoA --dataset_mode aligned --norm batch```

3. View the results in  `/results/edges2bracelets_pix2pix/test_latest/images`

4. The model will be exported to FINAL_MODELS

## 3b. Test the model with backend code

1. Copy the model from FINAL_MODELS to the input_model folder
2. Edit the test.py to correspond with model name + image input name
3. See results in results folder.

## 4. Upload model to prod

1. gsutil cp edges2bracelets_pix2pix gs://color-wave-bucket/edges2bracelets_pix2pix
2. Go edit backend code + android code 
