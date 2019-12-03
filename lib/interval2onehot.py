import  numpy as np
import  tensorflow as tf
from tensorflow.keras.utils import to_categorical
from p2m import  p_2_mmat,mmat_2_mmidi
np.set_printoptions(threshold=np.inf)
value_for_blank_not=84   #use 85 to represent blank pitch
def d4onehot_to_real(onehotmat):
    onehotmat=onehotmat.reshape((onehotmat.shape[0],onehotmat.shape[1],onehotmat.shape[2]))
    # patch_blank_onehot=np.zeros(onehotmat.shape[0],onehotmat.shape[1],1)
    #use 85 to represent blank note
    real_data = np.argmax(onehotmat, axis=2)
    print(real_data.shape)
    for i in range(real_data.shape[0]):
        for j in range(real_data.shape[1]):
            if real_data[i][j]==0:  #是否argmax取得是默认的 即one-hot全0
                if(onehotmat[i][j][0]==0):    #argmax取默认的
                    real_data[i][j]=84
                # patch_blank_onehot[i][j][0]=1


    #to midi just cut this

    # np.concatenate(onehotmat,)


    return real_data

def real_to_d4onehot(real_mat):

    d3onehot = to_categorical(real_mat,85)
    #change to d4
    d4onehot=np.expand_dims(d3onehot[:,:,0:84],axis=3)
    return d4onehot


def tes_t():
    # ------------test code -------------------
    m = np.load("10midi.npy")  # one hot use 100
    # print(m)

    f = d4onehot_to_real(m)
    d4 = real_to_d4onehot(f)
    d4_100 = d4 * 100

    # g=(d4==m)
    # for i in range (g.shape[0]):
    #     for j in range(g.shape[1]):
    #         for k in range(g.shape[2]):
    #             for l in range(g.shape[3]):
    #                 if(g[i][j][k][l]==False):
    #                     print (i,j,k,l)
    #                     print(d4[i][j][k][l],m[i][j][k][l])
    # 0 0 0 0
    # 0 1 0 0

    if ((d4_100 - m).any()):
        print("not same")
    else:
        print("same")

    mmat_2_mmidi(d4, "de.mid")
    mmat_2_mmidi(m, "m.mid")
    mmat_2_mmidi(d4_100, "d4_100.mid")



