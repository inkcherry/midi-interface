import os
from p2m import  p_2_mmat,mmat_2_mmidi
import  numpy as np
import  pretty_midi
root_path = '/home/liumingzhi/inkcpro/midilib/lib'
mididata_path = 'data1'
beat_resolution=4
from pypianoroll import Multitrack, Track

file_list = [f for f in os.listdir(os.path.join(root_path, mididata_path))]

def __get_midi_info(pm):
    """Return useful information from a pretty_midi.PrettyMIDI instance"""
    if pm.time_signature_changes:
        pm.time_signature_changes.sort(key=lambda x: x.time)
        first_beat_time = pm.time_signature_changes[0].time
    else:
        first_beat_time = pm.estimate_beat_start()

    tc_times, tempi = pm.get_tempo_changes()

    if len(pm.time_signature_changes) == 1:
        time_sign = '{}/{}'.format(pm.time_signature_changes[0].numerator,
                                   pm.time_signature_changes[0].denominator)
    else:
        time_sign = None

    midi_info = {
        'first_beat_time': first_beat_time,
        'num_time_signature_change': len(pm.time_signature_changes),
        'time_signature': time_sign,
        'tempo': tempi[0] if len(tc_times) == 1 else None
    }

    return midi_info



def get_midi_info(filepath):
    try:
        multitrack = Multitrack(beat_resolution=24)
        pm = pretty_midi.PrettyMIDI(filepath)
        midi_info = __get_midi_info(pm)


        multitrack.parse_pretty_midi(pm)
        return  midi_info
    except:
        return None

def  is_eligible_midi(midi_info):
    #error file
    if midi_info==None:
        return False
    #

    if midi_info['first_beat_time'] > 0.0:
        return False
    elif midi_info['num_time_signature_change'] > 1:
        return False
    elif midi_info['time_signature'] not in ['4/4']:
        return False
    return True

#this code to find monophoic track .
def is_monophonic(cur_mmat):
    onehotmat = cur_mmat.reshape((cur_mmat.shape[0], cur_mmat.shape[1], cur_mmat.shape[2]))

    for i_ in range(onehotmat.shape[0]):
        for j_ in range(onehotmat.shape[1]):
            index = np.argmax(onehotmat[i_][j_])
            onehotmat[i_][j_][index] = 0     #cancel   note of max pitch
            if np.max(onehotmat[i_][j_]) != 0: # another note== polyphonic music
                # print(cur_filename)
                # is_polyphonic = 1
                return False
    return True
#repeat i ?
count=0
concat_mat=[]
for i in range(len(file_list)):
    cur_filename = os.path.join(root_path, mididata_path, file_list[i])
    concat_mat = p_2_mmat(cur_filename,beat_resolution=beat_resolution)
    break



# print ("concat_mat shape",concat_mat.shape)




for i in range(len(file_list)):
    cur_filename=os.path.join(root_path,mididata_path,file_list[i])
    cur_midi_info=get_midi_info(cur_filename)
    if(is_eligible_midi(cur_midi_info)):
        cur_mmat = p_2_mmat(cur_filename,beat_resolution=beat_resolution)
        mat_for_judge=np.copy(cur_mmat)
        if(is_monophonic(mat_for_judge)):
        # ind = np.argpartition(onehotmat, -4)[-4:]
        # patch_blank_onehot=np.zeros(onehotmat.shape[0],onehotmat.shape[1],1)
        # use 85 to represent blank note
        #end
            concat_mat=np.concatenate((concat_mat,cur_mmat),axis=0)
            count+=1
            # print(cur_filename)
    # if (count == 2):
    #     break
print ("eligible_midi number of all midifiles",count,"/",i+1)

print("concat_mat shape",concat_mat.shape)

np.save("pixel4.npy",concat_mat)

# npar=np.load("eligiblemidii.npy")
# print("np ar shape",npar.shape)
# mmat_2_mmidi(npar,"real_midi.mid")
# for root, dirs, files in os.walk(filepath):