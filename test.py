import torch
import torchvision
import numpy as np
from PIL import Image
import torchvision.transforms as transforms

def tensor2im(input_image, imtype=np.uint8):
    if isinstance(input_image, torch.Tensor):
        image_tensor = input_image.data
    else:
        return input_image
    image_numpy = image_tensor[0].cpu().float().numpy()
    if image_numpy.shape[0] == 1:
        image_numpy = np.tile(image_numpy, (3, 1, 1))
    image_numpy = (np.transpose(image_numpy, (1, 2, 0)) + 1) / 2.0 * 255.0
    return image_numpy.astype(imtype)

def save_images(visuals, image_path, aspect_ratio=1.0, width=256):

    for label, im_data in visuals.items():
        im = tensor2im(im_data)
        image_name = '%s.png' % (label)
        h, w, _ = im.shape
        if aspect_ratio > 1.0:
            im = imresize(im, (h, int(w * aspect_ratio)), interp='bicubic')
        if aspect_ratio < 1.0:
            im = imresize(im, (int(h / aspect_ratio), w), interp='bicubic')

        image_pil = Image.fromarray(im)
        image_pil.save('./results/' + image_name)

if __name__ == '__main__':

    A_path = './images/img_0003.jpg'
    A_img = Image.open(A_path).convert('RGB')
    ratio = A_img.width / A_img.height

    transform_list = [transforms.Resize((256,256)), transforms.ToTensor(),
                       transforms.Normalize((0.5, 0.5, 0.5),
                                            (0.5, 0.5, 0.5))]
    allTransforms = transforms.Compose(transform_list)
    
    A_img = allTransforms(A_img)
    A_img = A_img[0, ...] * 0.299 + A_img[1, ...] * 0.587 + A_img[2, ...] * 0.114

    A_img = torch.stack([A_img] * 3, dim = 0).unsqueeze(0)

    model = torch.load('./final_model/edges2handbags')
    print model
    model.set_input({'A': A_img, 'A_paths' : ''})
    model.test()

    visuals = model.get_current_visuals()
    img_path = model.get_image_paths()        

    save_images(visuals, './results/', aspect_ratio=1.0, width=256)