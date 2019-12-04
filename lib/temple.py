import  numpy as np
import  tensorflow as tf
from p2m import  p_2_mmat,mmat_2_mmidi
from interval2onehot import  d4onehot_to_real,real_to_d4onehot
from file_batch import beat_resolution


dataset_mat=np.load("pixel4.npy")
# print("tomidi",dataset_mat.shape)
# mmat_2_mmidi(dataset_mat,"2beat"+str(beat_resolution)+".mid",beat_reselution=beat_resolution)
real_one =d4onehot_to_real(dataset_mat)
print(real_one.shape)
np.save("dataset.npy",real_one)

# print(real_one)
# red4=real_to_d4onehot(real_one)
# mmat_2_mmidi(red4,"rebeat2.mid",beat_reselution=2)



