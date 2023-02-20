import os
import imageio
import glob
import subprocess



class fs_QA():
    def __init__(self, sub_path):
        self.sub_path = sub_path
        self.total_cmd_list = []
        self.base_cmd = "freeview -v mri/brainmask.mgz -f surf/lh.white:edgecolor=yellow surf/lh.pial:edgecolor=red surf/rh.white:edgecolor=yellow surf/rh.pial:edgecolor=red -layout 1 -cc -nocursor"
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
        subprocess.run(f'freeview -cmd {self.cmd_txt_path}',shell = True)
        
    #>>> from get_freeview_utils import fs_QA
    #>>> sub_path = '/scratch/connectome/dyhan316/sample_infant_fs/sub-111723'
    #>>> aa = fs_QA(sub_path)
    #>>> aa.create_txt_cmd()
    #>>> aa.run_freeview() 
        
        
        
    def get_slice(name):
        return name.replace('.','_').split('_')[-2]
    
    
    def save_gif():
        pass
        
    def save_imgs():
        pass 
