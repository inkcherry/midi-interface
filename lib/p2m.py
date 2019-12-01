import os.path
import argparse

#this file just for Specific datasets,one track represent melody





from pypianoroll import Multitrack, Track
import tensorflow as tf
import numpy as np
import  pretty_midi
import write_midi
bar_length=32
def get_bar_piano_roll(piano_roll,last_bar_mode='remove'):
    if int(piano_roll.shape[0] % bar_length) is not 0:
        if last_bar_mode == 'fill':
            piano_roll = np.concatenate((piano_roll, np.zeros((bar_length - piano_roll.shape[0] % bar_length, 128))), axis=0)
        elif last_bar_mode == 'remove':
            piano_roll = np.delete(piano_roll,  np.s_[-int(piano_roll.shape[0] % bar_length):], axis=0)
    piano_roll = piano_roll.reshape(-1, bar_length, 128)
    return piano_roll




# f=x.get_beats()
# f=x.estimate_tempo()
# print(f)

# print(x.resolution)
# print(f)
# print(f.shape)
# print(f)


# exit()

















#some code four future layer bar
# idx=0
#
# print("merges shape is ")
# print(merges.shape)
# print("-----------")
#
# ac=merges[0]
#
# dd=ac.reshape(1,ac.shape[0],ac.shape[1],ac.shape[2])
# print(dd.shape)




def p_2_mmat(filename):
    x = pretty_midi.PrettyMIDI('chorus_nokey.mid')
    multitrack = Multitrack(beat_resolution=4, name='test')
    multitrack.parse_pretty_midi(x)
    melody_track = []
    melody_track.append(Track(multitrack.tracks[0].get_pianoroll_copy(), 0, False, 'Piano'))
    pr = get_bar_piano_roll(melody_track[0].pianoroll)
    pr_clip = pr[:, :, 24:108]
    if int(pr_clip.shape[0] % 4) != 0:
        pr_clip = np.delete(pr_clip, np.s_[-int(pr_clip.shape[0] % 4):], axis=0)
    pr_re = pr_clip.reshape(-1, bar_length, 84, 1)
    track = pr_re
    return track


def mmat_2_mmidi(track,filename):
    write_midi.save_singletrck_midis(track,"filename")













