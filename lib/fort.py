

from p2m import  p_2_mmat,mmat_2_mmidi

def t_p2m():
    track=p_2_mmat('chorus_nokey.mid')
    print(track.shape)
    mmat_2_mmidi(track,'woqu1fsd.mid')

t_p2m()