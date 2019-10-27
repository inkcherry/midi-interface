from pypianoroll import Multitrack, Track
import pretty_midi
import os
import errno
import matplotlib.pyplot as plt
import librosa.display
import tensorflow as tf
# import mir_eval.display
import numpy as np
def make_sure_path_exists(path):
    """Create all intermediate-level directories if the given path does not
    exist"""
    try:
        print("no path here ,create new path")
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
#
def get_info_of_midi(filename):
    pm=pretty_midi.PrettyMIDI(filename)
    for inst_num in range(len(pm.instruments)):  # 打印所有乐器的信息
        print(inst_num)
        print(pm.instruments[inst_num])





def plot_piano_roll(pm, start_pitch, end_pitch, fs=100):
                    librosa.display.specshow(pm.get_piano_roll(fs)[start_pitch:end_pitch],
                    hop_length=1, sr=fs, x_axis='time',
                    y_axis='cqt_note',fmin=pretty_midi.note_number_to_hz(start_pitch))



def show_midi(filepath):
    pm = pretty_midi.PrettyMIDI(filepath)

    plt.figure(figsize=(12, 4))
    plot_piano_roll(pm, 24, 84)
    plt.show()


def get_info_of_pm(pm):
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


def get_merged(multitrack):
    return


def convert2npy():
    return



def get_pm(filename):
    multitrack=Multitrack(beat_resolution=24, name=filename)
    midi_name = os.path.splitext(filename)[0]
    pm = pretty_midi.PrettyMIDI("example.mid")
    return pm



# pm = pretty_midi.PrettyMIDI("example.mid")
# t=get_info_of_pm(get_pm("example.mid"))
# print(t)
#test





#test
#--------------------------------------------
# midi_name="example"

multitrack = Multitrack(beat_resolution=24, name="example")
x=pretty_midi.PrettyMIDI("example.mid")
multitrack.parse_pretty_midi(x)

category_list = {'Drums': [], 'Piano': [],  'Guitar': [], 'Bass': [], 'Strings': []}
program_dict = {'Drums': 0,'Piano': 0,  'Guitar': 24, 'Bass': 32, 'Strings': 48}
for idx, track in enumerate(multitrack.tracks):

    if track.is_drum:
        category_list['Drums'].append(idx)
    elif track.program//8 == 0:
        category_list['Piano'].append(idx)
    elif track.program//8 == 3:
        category_list['Guitar'].append(idx)
    elif track.program//8 == 4:
        category_list['Bass'].append(idx)
    else:
        category_list['Strings'].append(idx)

    print(type(category_list))
    print(tf.shape(category_list['Drums']))
    print(category_list['Drums'])

    tracks = []
    for key in category_list:  # Bass\Drums\Guitar\Piano\Strings
        if category_list[key]:
            merged = multitrack[category_list[key]].get_merged_pianoroll()
            # print(merged.shape) #(14088, 128)
            tracks.append(Track(merged, program_dict[key], key == 'Drums', key))
        # print("tracks:",tracks)
        else:
            tracks.append(Track(None, program_dict[key], key == 'Drums', key))

    multitrack = Multitrack(None, tracks, multitrack.tempo, multitrack.downbeat, multitrack.beat_resolution,
                            multitrack.name)



# print(tf.shape(category_list))
#
# # midi_name = os.path.splitext(os.path.basename(filepath))[0]
#
# pm = pretty_midi.PrettyMIDI("example.mid")
# multitrack.parse_pretty_midi(pm)
# print(multitrack.tracks)
# for intrument in pm.instruments:
#     print(intrument)

# # mergerd=get_merged()










#test
#-------------------------------------------------
# # Load MIDI file into PrettyMIDI object
# midi_data = pretty_midi.PrettyMIDI('example.mid')
# # Print an empirical estimate of its global tempo
# print( midi_data.estimate_tempo())
# # Compute the relative amount of each semitone across the entire song,
# # a proxy for key
# total_velocity = sum(sum(midi_data.get_chroma()))
#
# for semitone in midi_data.get_chroma():
#     print(sum(semitone)/total_velocity)
#
#
#
# print("midi instruments")
# print(midi_data.instruments)
# # Shift all notes up by 5 semitones
# for instrument in midi_data.instruments:
#     # Don't want to shift drum notes
#     if not instrument.is_drum:
#         for note in instrument.notes:
#             note.pitch += 5


