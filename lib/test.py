

from p2m import  p_2_mmat,mmat_2_mmidi

def test_p2m():
    track=p_2_mmat('chorus_nokey.mid')
    print(track.shape)
    mmat_2_mmidi(track,'testfile.mid')