

from p2m.py import  p_2_mmat,mmat_2_mmidi


track=p_2_mmat('chorus_nokey.mid')
print(track.shape)
mmat_2_mmidi(track,'testfile.mid')