from options.test_options import TestOptions
from data import CreateDataLoader
from models import create_model
import ntpath
from util import util
import os
import torch
import torchvision
from PIL import Image
import torchvision.transforms as transforms

def save_images(visuals, image_path, aspect_ratio=1.0, width=256):
    short_path = ntpath.basename(image_path[0])

    for label, im_data in visuals.items():
        im = util.tensor2im(im_data)
        image_name = '%s.png' % (label)
        h, w, _ = im.shape
        if aspect_ratio > 1.0:
            im = imresize(im, (h, int(w * aspect_ratio)), interp='bicubic')
        if aspect_ratio < 1.0:
            im = imresize(im, (int(h / aspect_ratio), w), interp='bicubic')
        util.save_image(im, './results/' + image_name) # Save this to google bucket

if __name__ == '__main__':
    #data_loader = CreateDataLoader(opt)
    #dataset = data_loader.load_data()
    # model = create_model(opt)
    # model.setup(opt)
    
    # Read in image RGB image 

    #Convert to greyscale using their method
    A_path = './images/img_0001.jpg'
    A_img = Image.open(A_path).convert('RGB')

    #Optional resize

    # transform
    transform_list = [transforms.Resize((256,256)), transforms.ToTensor(),
                       transforms.Normalize((0.5, 0.5, 0.5),
                                            (0.5, 0.5, 0.5))]
    allTransforms = transforms.Compose(transform_list)
    
    A_img = allTransforms(A_img)
    A_img = A_img[0, ...] * 0.299 + A_img[1, ...] * 0.587 + A_img[2, ...] * 0.114

    A_img = torch.stack([A_img] * 3, dim = 0).unsqueeze(0)

    print(A_img.shape)

    model = torch.load('./final_model/model')
    model.set_input({'A': A_img, 'A_paths' : ''})
    model.test()

    visuals = model.get_current_visuals()
    img_path = model.get_image_paths()        
    save_images(visuals, './results/', aspect_ratio=1.0, width=256)