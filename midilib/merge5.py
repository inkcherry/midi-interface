import os.path
import argparse
from pypianoroll import Multitrack, Track
import tensorflow as tf
import numpy as np

TRACK_INFO = (
    ('Drums', 0),
    ('Piano', 0),
    ('Guitar', 24),
    ('Bass', 32),
    ('Strings', 48),
)



def get_merged(multitrack):
    """Merge the multitrack pianorolls into five instrument families and
    return the resulting multitrack pianoroll object."""
    track_lists_to_merge = [[] for _ in range(5)]
    for idx, track in enumerate(multitrack.tracks):
        if track.is_drum:
            track_lists_to_merge[0].append(idx)
        elif track.program//8 == 0:
            track_lists_to_merge[1].append(idx)
        elif track.program//8 == 3:
            track_lists_to_merge[2].append(idx)
        elif track.program//8 == 4:
            track_lists_to_merge[3].append(idx)

        elif track.program < 96 or 104 <= track.program < 112:
            track_lists_to_merge[4].append(idx)

    tracks = []
    for idx, track_list_to_merge in enumerate(track_lists_to_merge):
        if track_list_to_merge:
            merged = multitrack[track_list_to_merge].get_merged_pianoroll('max')
            print("3c3c3c")
            print(merged.shape)
            pr = get_bar_piano_roll(merged)

            tracks.append(Track(merged, TRACK_INFO[idx][1], (idx == 0),
                                TRACK_INFO[idx][0]))
        else:
            tracks.append(Track(None, TRACK_INFO[idx][1], (idx == 0),
                                TRACK_INFO[idx][0]))
    return Multitrack(None, tracks, multitrack.tempo, multitrack.downbeat,
                      multitrack.beat_resolution, multitrack.name)



def get_bar_piano_roll(piano_roll,last_bar_mode='remove'):
    if int(piano_roll.shape[0] % 64) is not 0:
        if last_bar_mode == 'fill':
            piano_roll = np.concatenate((piano_roll, np.zeros((64 - piano_roll.shape[0] % 64, 128))), axis=0)
        elif last_bar_mode == 'remove':
            piano_roll = np.delete(piano_roll,  np.s_[-int(piano_roll.shape[0] % 64):], axis=0)
    piano_roll = piano_roll.reshape(-1, 64, 128)
    return piano_roll

multitrack =Multitrack("example.mid")
merged=get_merged(multitrack)
print(merged.shape)


# data=merged.get_stacked_pianoroll()

#
# print(tf.shape(data))
#
# print(type(merged))
# merged.save("/home/liumingzhi/projectfile/pratice/data-processing/nn")




# data=piano_roll.get_stacked_pianoroll()
