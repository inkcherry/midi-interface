import os
from p2m import  p_2_mmat,mmat_2_mmidi
import  numpy as np
root_path = '/home/liumingzhi/inkcpro/midilib/lib'
mididata_path = 'data1'

file_list = [f for f in os.listdir(os.path.join(root_path, mididata_path))]


count=0
concat_mat=[]
for i in range(len(file_list)):
    cur_filename = os.path.join(root_path, mididata_path, file_list[i])
    concat_mat = p_2_mmat(cur_filename)



print ("concat_mat shape",concat_mat.shape)

for i in range(len(file_list)):

    cur_filename=os.path.join(root_path,mididata_path,file_list[i])
    cur_mmat=p_2_mmat(cur_filename)
    print(cur_filename)
    print(cur_mmat.shape)
    concat_mat=np.concatenate((concat_mat,cur_mmat),axis=0)
    count+=1
    if(count==10):
        break


print("concat_mat shape",concat_mat.shape)


exit()
# for root, dirs, files in os.walk(filepath):

