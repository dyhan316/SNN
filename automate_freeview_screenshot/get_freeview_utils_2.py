import os
import imageio
import glob
import subprocess
from PIL import Image

##now add names
##also parallizing code 

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-sub_path", type=str, help="Subject path to process")
args = parser.parse_args()

sub_path = args.sub_path




class fs_QA():
    def __init__(self, sub_path):
        self.sub_path = sub_path
        self.total_cmd_list = []
        #self.base_cmd = "freeview -v mri/brainmask.mgz -f surf/lh.white:edgecolor=yellow surf/lh.pial:edgecolor=red surf/rh.white:edgecolor=yellow surf/rh.pial:edgecolor=red -layout 1 -cc -nocursor"
        self.base_cmd = "freeview -v mri/brainmask.mgz mri/wm.mgz:colormap=heat:opacity=0.3 -f surf/lh.white:edgecolor=yellow surf/lh.pial:edgecolor=red surf/rh.white:edgecolor=yellow surf/rh.pial:edgecolor=red -layout 1 -cc -nocursor"
        self.total_cmd_list.append(self.base_cmd)


    def cmd_maker(self,view, idx):
        if view == 'sagittal' : 
            slice_idx = [idx, 127, 127]
        elif view == 'axial' : 
            slice_idx = [127, idx, 127]
        elif view == 'coronal':
            slice_idx = [127, 127, idx]
        else : 
            raise ValueError()
        slice_str = " ".join([str(i) for i in slice_idx])
        return f"-viewport {view} -slice {slice_str} -ss  ./img_save/T1_{view}_{idx:03d}.jpg -noquit"
    
    def create_txt_cmd(self):  
        for i in range(50,200,1):
            self.total_cmd_list.append(self.cmd_maker('sagittal', i))
            self.total_cmd_list.append(self.cmd_maker('axial', i))
            self.total_cmd_list.append(self.cmd_maker('coronal', i))
        self.total_cmd_list.append('-quit')
        self.final_txt = '\n'.join(self.total_cmd_list)
    
        #saving the txt file 
        #import pdb ; pdb.set_trace()
        self.cmd_txt_path = os.path.join(self.sub_path , 'cmd_txt.txt')
        file = open(os.path.join(self.sub_path , 'cmd_txt.txt'), 'w')
        a = file.write(self.final_txt)
        file.close()
        
    def run_freeview(self) :
        os.mkdir(os.path.join(self.sub_path, 'img_save'))
        #subprocess.run('source ~/.bashrc', shell = True) #이걸 해놔야함!
        subprocess.run('freeview -cmd cmd_txt.txt',shell = True)
        
    #>>> from get_freeview_utils import fs_QA
    #>>> sub_path = '/scratch/connectome/dyhan316/sample_infant_fs/sub-111723'
    #>>> aa = fs_QA(sub_path)
    #>>> aa.create_txt_cmd()
    #>>> aa.run_freeview() 

    
#misc func
def get_slice(name):
    return name.replace('.','_').split('_')[-2]
        

    
##running freeview
a = fs_QA(sub_path)

a.create_txt_cmd()

cwd = os.getcwd()
os.chdir(a.sub_path)
a.run_freeview()
os.chdir(cwd) #go back


if True:
    sagittal = glob.glob(f'{a.sub_path}/img_save/*sagittal*jpg')
    axial = glob.glob(f'{a.sub_path}/img_save/*axial*jpg')
    coronal = glob.glob(f'{a.sub_path}/img_save/*coronal*jpg')
    
    sagittal.sort(key = get_slice)
    axial.sort(key = get_slice)
    coronal.sort(key = get_slice)
    
    sagittal_gif = []
    
    
    
    for filename in sagittal:
        sagittal_gif.append(imageio.imread(filename))
    
    axial_gif = []
    for filename in axial:
        axial_gif.append(imageio.imread(filename))
    
    
    coronal_gif = []
    for filename in coronal:
        coronal_gif.append(imageio.imread(filename))
    
    
    imageio.mimsave(f'{a.sub_path}/{sub_path.split("/")[-1]}_sagittal.gif', sagittal_gif)
    imageio.mimsave(f'{a.sub_path}/{sub_path.split("/")[-1]}_axial.gif', axial_gif)
    imageio.mimsave(f'{a.sub_path}/{sub_path.split("/")[-1]}_coronal.gif', coronal_gif)
    
    slices_to_show = list(range(35,120,15))
    crop_pixel = 70
    
    
    images_to_combine = []
    for idx in slices_to_show:
        for view in [sagittal, axial, coronal]: 
            images_to_combine.append(Image.open(view[idx])) #list of opened images 
    
    # Get the size of the images
    w,h = images_to_combine[0].size
    
    ##cropping##
    # Calculate the new dimensions after cropping the 50-pixel boundary
    new_width = w - crop_pixel*2  # 50 pixels from the left and 50 pixels from the right
    new_height = h - crop_pixel*2  # 50 pixels from the top and 50 pixels from the bottom
    
    # cropping the list of pisels 
    images_to_combine = [image.crop((crop_pixel, crop_pixel, new_width, new_height)) for image in images_to_combine]
    ###########
    
    new_image = Image.new('RGB',(len(slices_to_show)*new_width,3*new_height))                     
    
    #paste the images into the new image
    count = 0
    for i in range(len(slices_to_show)):
        for j in range(3):
            new_image.paste(images_to_combine[count], (i*new_width,j*new_height))
            count +=1
            
    new_image.save(f"{a.sub_path}/{sub_path.split('/')[-1]}.jpg") #change this direction 
    
    
    os.makedirs(f'{a.sub_path}/../save_stuff', exist_ok = True)
    subprocess.run(f'cp {a.sub_path}/*.gif {a.sub_path}/*.jpg {a.sub_path}/../save_stuff', shell = True)
    
