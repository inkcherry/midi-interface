import  numpy as np
import  tensorflow as tf
from p2m import  p_2_mmat,mmat_2_mmidi
import  interval2onehot as i2o
dataset_mat=np.load("eligiblemidii.npy")
print("tomidi",dataset_mat.shape)
mmat_2_mmidi(dataset_mat,"ffcc.mid")
