import os
import sys
import numpy as np
import nibabel as nib
import pdb

pdb.set_trace() 

from keras.model import * 
try:
    from keras.models import *
except:
    print('---------------------------------------------------------------------------------------------------------------------------------------')
    print('ERROR: Failed to initialize tensorflow-gpu and Keras. Please ensure that this module is installed and a GPU is readily accessible.')
    print('---------------------------------------------------------------------------------------------------------------------------------------')
    sys.exit(1)

from defacer_utils import resize_img, dice_coefficient, resample_image, pre_process_image, get_available_gpus


def deface_3D_MRI():

    if len(sys.argv) < 2:
        print('----------------------------------------------------------------------------------------------------')
        print(
            "usage: Please specify the filepath of a MRI image for defacing....(e.g deepdefacer <path of MRI>")
        print('----------------------------------------------------------------------------------------------------')
        sys.exit(1)

    if not get_available_gpus():
        print('---------------------------------------------------------------------------------------------------------------------------------------')
        print("WARNING: Could not find an available GPU on your system. Defaulting to CPU")
        print('---------------------------------------------------------------------------------------------------------------------------------------')
        os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID" 
        os.environ['CUDA_VISIBLE_DEVICES'] = '-1' 
        sys.exit(1)

    MRI_image_path = sys.argv[1]
    if '.nii' not in MRI_image_path or '.nii.gz' not in MRI_image_path:
        print('------------------------------------------------------------------------')
        print("ERROR: Please ensure that input MRI file is in .nii or .nii.gz format")
        print('------------------------------------------------------------------------')

    print('Preproessing input MRI image...')

    MRI_image_shape = np.squeeze(nib.load(MRI_image_path).get_data()).shape

    if len(MRI_image_shape) != 3:
        print('------------------------------------------------------------------------')
        print("ERROR: Unable to deface MRI: Please ensure that input dimensions are in 3D.")
        print('------------------------------------------------------------------------')

    MRI_image_data, MRI_unnormalized_data = pre_process_image(MRI_image_path)

    deepdeface_model = load_model(
        'deepdefacer/model.hdf5', custom_objects={'dice_coefficient': dice_coefficient})

    print('-------------------------------------------------')
    print('Masking %s ....' % (MRI_image_path))

    mask_prediction = deepdeface_model.predict(MRI_image_data)

    mask_prediction[mask_prediction < 0.5] = 0
    mask_prediction[mask_prediction >= 0.5] = 1

    mask_prediction = np.squeeze(mask_prediction)

    masked_image = np.multiply(MRI_unnormalized_data, mask_prediction)

    masked_image_save = nib.Nifti1Image(
        masked_image, nib.load(MRI_image_path).affine)

    masked_image_resampled = resample_image(
        masked_image_save, orig=MRI_image_shape, get_nifti=True)

    output_file = os.path.splitext(os.path.splitext(
        os.path.basename(MRI_image_path))[0])[0] + '_defaced.nii.gz'

    print('Completed! Saving to %s...' % (output_file))

    nib.save(masked_image_resampled, output_file)

    print('Saved.')
    print('----------')
