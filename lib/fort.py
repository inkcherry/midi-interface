

from p2m import  p_2_mmat,mmat_2_mmidi

def tes_t_p2m():
    track=p_2_mmat('chorus_nokey.mid',beat_resolution=24)
    print(track.shape)
    mmat_2_mmidi(track,'woqu1fsd.mid')
    print(track[10:14,:,:,:].shape)
    mmat_2_mmidi(track[10:14,:,:,:],'testlength.mid')
    track2=p_2_mmat('chorus_nokey.mid',beat_resolution=4)
    print(track2.shape)
    # mmat_2_mmidi(track,'woqu1fsd.mid')

tes_t_p2m()