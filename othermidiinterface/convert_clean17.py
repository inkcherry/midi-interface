from __future__ import print_function
import os
import json
import errno
from pypianoroll import Multitrack, Track
import pretty_midi
import shutil
import numpy as np
import write_midi
import tensorflow as tf
ROOT_PATH = '/home/liumingzhi/projectfile/midi-interface/filedir'
converter_path = os.path.join(ROOT_PATH, 'MIDI/pop/pop_test/converter')
cleaner_path = os.path.join(ROOT_PATH, 'MIDI/pop/pop_test/cleaner')





def make_sure_path_exists(path):
    """Create all intermediate-level directories if the given path does not
    exist"""
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


def get_midi_path(root):
    """Return a list of paths to MIDI files in `root` (recursively)"""
    filepaths = []
    for dirpath, _, filenames in os.walk(root):
        for filename in filenames:
            if filename.endswith('.mid'):
                filepaths.append(os.path.join(dirpath, filename))
    return filepaths


def get_midi_info(pm):
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


def midi_filter(midi_info):
    """Return True for qualified midi files and False for unwanted ones"""
    if midi_info['first_beat_time'] > 0.0:
        return False
    elif midi_info['num_time_signature_change'] > 1:
        return False
    elif midi_info['time_signature'] not in ['4/4']:
        return False
    return True


def get_merged(multitrack):
    """Return a `pypianoroll.Multitrack` instance with piano-rolls merged to
    five tracks (Bass, Drums, Guitar, Piano and Strings)"""
    category_list = {'Drums': [], 'Piano': [], 'Chromatic Percussion': [], 'Organ': [], 'Guitar': [], 'Bass': [],
                     'Strings': [], 'Ensemble': [],
                     'Brass': [], 'Reed': [], 'Pipe': [], 'Synth Lead': [], 'Synth Pad': [],
                     'Synth Effects': [], 'Ethnic': [], 'Percussive': [], 'Sound Effects': []}

    program_dict = {'Drums': 0, 'Piano': 0, 'Chromatic Percussion': 8, 'Organ': 16, 'Guitar': 24, 'Bass': 32,
                    'Strings': 40,
                    'Ensemble': 48, 'Brass': 56, 'Reed': 64, 'Pipe': 72, 'Synth Lead': 80, 'Synth Pad': 88,
                    'Synth Effects': 96,
                    'Ethnic': 104, 'Percussive': 112, 'Sound Effects': 120
                    }
    track_info = (
        'Drums', 'Piano', 'Chromatic Percussion', 'Organ', 'Guitar', 'Bass', 'Strings', 'Ensemble',
        'Brass', 'Reed', 'Pipe', 'Synth Lead', 'Synth Pad',
        'Synth Effects', 'Ethnic', 'Percussive', 'Sound Effects'
    )

    for idx, track in enumerate(multitrack.tracks):
        if track.is_drum:
            category_list['Drums'].append(idx)
        else:
            category_list[track.program//8 + 1].append(idx)
        # elif track.program//8 == 0:
        #     category_list['Piano'].append(idx)
        # elif track.program//8 == 3:
        #     category_list['Guitar'].append(idx)
        # elif track.program//8 == 4:
        #     category_list['Bass'].append(idx)
        # else:
        #     category_list['Strings'].append(idx)
    print("kkksdf")
    tracks = []
    for key in category_list:
        if category_list[key]:
            merged = multitrack[category_list[key]].get_merged_pianoroll()
            tracks.append(Track(merged, program_dict[key], key == 'Drums', key))
        else:
            tracks.append(Track(None, program_dict[key], key == 'Drums', key))
    print("kkksdf")
    print("trackshape ",tf.shape(track))
    return Multitrack(None, tracks, multitrack.tempo, multitrack.downbeat, multitrack.beat_resolution, multitrack.name)


def converter(filepath):
    """Save a multi-track piano-roll converted from a MIDI file to target
    dataset directory and update MIDI information to `midi_dict`"""
    try:
        midi_name = os.path.splitext(os.path.basename(filepath))[0]
        multitrack = Multitrack(beat_resolution=24, name=midi_name)

        pm = pretty_midi.PrettyMIDI(filepath)
        midi_info = get_midi_info(pm)
        multitrack.parse_pretty_midi(pm)
        merged = get_merged(multitrack)

        make_sure_path_exists(converter_path)
        merged.save(os.path.join(converter_path, midi_name + '.npz'))

        return [midi_name, midi_info]

    except:
        return None
def get_bar_piano_roll(piano_roll,last_bar_mode='remove'):
    if int(piano_roll.shape[0] % 64) is not 0:
        if last_bar_mode == 'fill':
            piano_roll = np.concatenate((piano_roll, np.zeros((64 - piano_roll.shape[0] % 64, 128))), axis=0)
        elif last_bar_mode == 'remove':
            piano_roll = np.delete(piano_roll,  np.s_[-int(piano_roll.shape[0] % 64):], axis=0)
    piano_roll = piano_roll.reshape(-1, 64, 128)
    return piano_roll


def save_midis(bars, file_path, tempo=80.0):
    padded_bars = np.concatenate((np.zeros((bars.shape[0], bars.shape[1], 24, bars.shape[3])), bars,
                                  np.zeros((bars.shape[0], bars.shape[1], 20, bars.shape[3]))), axis=2)
    pause = np.zeros((bars.shape[0], 64, 128, bars.shape[3]))
    images_with_pause = padded_bars
    images_with_pause = images_with_pause.reshape(-1, 64, padded_bars.shape[2], padded_bars.shape[3])
    images_with_pause_list = []
    for ch_idx in range(padded_bars.shape[3]):
        images_with_pause_list.append(images_with_pause[:, :, :, ch_idx].reshape(images_with_pause.shape[0],
                                                                                 images_with_pause.shape[1],
                                                                                 images_with_pause.shape[2]))
    # write_midi.write_piano_rolls_to_midi(images_with_pause_list, program_nums=[33, 0, 25, 49, 0],
    #                                      is_drum=[False, True, False, False, False], filename=file_path, tempo=80.0)
    # print('fjfjjf')
    write_midi.write_piano_rolls_to_midi(images_with_pause_list, program_nums=[0], is_drum=[False], filename=file_path,
                                         tempo=tempo, beat_resolution=4)



##test---------------------------------------------
# filepath="../filedir/example.mid"
# midi_name = os.path.splitext(os.path.basename(filepath))[0]
# multitrack = Multitrack(beat_resolution=24, name=midi_name)
#
# pm = pretty_midi.PrettyMIDI(filepath)
# midi_info = get_midi_info(pm)
# multitrack.parse_pretty_midi(pm)
# merged = get_merged(multitrack)
#
# make_sure_path_exists(converter_path)
# merged.save(os.path.join(converter_path, midi_name + '.npz'))
##test-----------------------------------------------



# ROOT_PATH = '/home/liumingzhi/projectfile/midi-interface/filedir'

multitrack = Multitrack(beat_resolution=4, name='example')
x = pretty_midi.PrettyMIDI('example.mid')
multitrack.parse_pretty_midi(x)

category_list = {'Piano': [], 'Drums': []}
program_dict = {'Piano': 0, 'Drums': 0}

for idx, track in enumerate(multitrack.tracks):
    if track.is_drum:
        category_list['Drums'].append(idx)
    else:
        category_list['Piano'].append(idx)
tracks = []
merged = multitrack[category_list['Piano']].get_merged_pianoroll()

# print(merged.shape)



pr = get_bar_piano_roll(merged)
# print(pr.shape)
pr_clip = pr[:, :, 24:108]
# print(pr.shape)
# print(pr_clip.shape)
if int(pr_clip.shape[0] % 4) != 0:
    pr_clip = np.delete(pr_clip, np.s_[-int(pr_clip.shape[0] % 4):], axis=0)
pr_re = pr_clip.reshape(-1, 64, 84, 1)
# print(pr_re.shape)


save_midis(pr_re,"/home/liumingzhi/projectfile/midi-interface/17.mid")

# print("fsdfa")

# pr = get_bar_piano_roll(merged)
# print(pr.shape)
# pr_clip = pr[:, :, 24:108]
# print(pr_clip.shape)
# if int(pr_clip.shape[0] % 4) != 0:
#     pr_clip = np.delete(pr_clip, np.s_[-int(pr_clip.shape[0] % 4):], axis=0)
# pr_re = pr_clip.reshape(-1, 64, 84, 1)
# print(pr_re.shape)
# save_midis(pr_re, os.path.join(ROOT_PATH, 'MIDI/pop/pop_test/cleaner_midi_gen', os.path.splitext(l[i])[0] +
#                                '.mid'))
# np.save(os.path.join(ROOT_PATH, 'MIDI/pop/pop_test/cleaner_npy', os.path.splitext(l[i])[0] + '.npy'), pr_re)
# except:
# count += 1
# print('Wrong', l[i])
# continue

