import pretty_midi as pm
import os
import sys
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
import  math
SMALLEST_NOTE = 16 #set this to 16, if you want to include 16th notes as smallest notes. has to be a multiple of 4



def load_rolls(name):
    # try loading the midi file
    # if it fails, return all None objects

    midata = pm.PrettyMIDI(name)
    tempo_change_times, tempo_change_bpm = midata.get_tempo_changes()
    song_start = 0
    song_end = midata.get_end_time()
    # print(tempo_change_times)
    # print("-------")
    # print(tempo_change_bpm)



    #找出音乐最长的一段，分析那一段的bmp，作为整个音乐的tempo
    if len(tempo_change_times) > 1:
        longest_part = 0
        longest_part_start_time = 0
        longest_part_end_time = song_end
        longest_part_tempo = 0
        for i, tempo_change_time in enumerate(tempo_change_times):
            if i == len(tempo_change_times) - 1:
                end_time = song_end
            else:
                end_time = tempo_change_times[i+1]
            current_part_length = end_time - tempo_change_time
            if current_part_length > longest_part:
                longest_part = current_part_length
                longest_part_start_time = tempo_change_time
                longest_part_end_time = end_time
                longest_part_tempo = tempo_change_bpm[i]
        song_start = longest_part_start_time
        song_end = longest_part_end_time
        tempo = longest_part_tempo
    else:
        tempo = tempo_change_bpm[0]
    print(tempo)

    for instrument in midata.instruments:
        # print(instrument)
        new_notes = [] #list for the notes that survive the cutting
        for note in instrument.notes:
            # print(note)
            #check if it is in the given range of the longest part where the tempo is steady
            if note.start >= song_start and note.end <= song_end:
                #adjust to new times
                note.start -= song_start
                note.end -= song_start
                new_notes.append(note)
        instrument.notes = new_notes
    number_of_notes = []


    #按包含的非空音符排列pianoroll
    piano_rolls = [i.get_piano_roll(fs=100) for i in midata.instruments]
    # print(piano_rolls)
    for piano_roll in piano_rolls:
        number_of_notes.append(np.count_nonzero(piano_roll))

    permutation = np.argsort(number_of_notes)[::-1]
    # print(permutation)
    midata.instruments = [midata.instruments[i] for i in permutation]

    quarter_note_length = 1. / (tempo / 60.)

    # fs is is the frequency for the song at what rate notes are picked
    # the song will by sampled by (0, song_length_in_seconds, 1./fs)
    # fs should be the inverse of the length of the note, that is to be sampled
    # the value should be in beats per seconds, where beats can be quarter notes or whatever...
    fs = 1. / (quarter_note_length * 4. / SMALLEST_NOTE)
    print(song_end)
    total_ticks = math.ceil(song_end * fs)
    #total_ticks是时间下标范围
    print(total_ticks)

    piano_rolls = []
    velocity_rolls = []
    held_note_rolls = []


    max_concurrent_notes_per_track_list = []
    for instrument in midata.instruments:
        piano_roll = np.zeros((total_ticks, 128))

        # counts how many notes are played at maximum for this instrument at any given tick
        # this is used to determine the depth of the velocity_roll and held_note_roll
        concurrent_notes_count = np.zeros((total_ticks,))

        # keys is a tuple of the form (tick_start_of_the_note, pitch)
        # this uniquely identifies a note since there can be no two notes playing on the same pitch for the same instrument
        note_to_velocity_dict = dict()

        # keys is a tuple of the form (tick_start_of_the_note, pitch)
        # this uniquely identifies a note since there can be no two notes playing on the same pitch for the same instrument
        note_to_duration_dict = dict()
        #这一段就是算了 V和D连个数组
        for note in instrument.notes:
            note_tick_start = note.start * fs
            note_tick_end = note.end * fs
            absolute_start = int(round(note_tick_start))
            absolute_end = int(round(note_tick_end))
            decimal = note_tick_start - absolute_start
            # see if it starts at a tick or not
            # if it doesn't start at a tick (decimal > 10e-3) but is longer than one tick, include it anyways
            if decimal < 10e-3 or absolute_end - absolute_start >= 1:
                piano_roll[absolute_start:absolute_end, note.pitch] = 1

                concurrent_notes_count[absolute_start:absolute_end] += 1
                #所有轨道共有的音符

                # save information of velocity and duration for later use
                # this can not be done right now because there might be no ordering in the notes
                note_to_velocity_dict[(absolute_start, note.pitch)] = note.velocity
                note_to_duration_dict[(absolute_start, note.pitch)] = absolute_end - absolute_start
        #统计与最多的共点音符
        max_concurrent_notes = int(np.max(concurrent_notes_count))

        max_concurrent_notes_per_track_list.append(max_concurrent_notes)

        print("Max concurrent notes: ", max_concurrent_notes)

        velocity_roll = np.zeros((total_ticks, max_concurrent_notes))
        held_note_roll = np.zeros((total_ticks, max_concurrent_notes))

        for step, note_vector in enumerate(piano_roll):
            # print("fsfsdf",note_vector)

            pitches = list(note_vector.nonzero()[0])
            print("afdsf",pitches)
            sorted_pitches_from_highest_to_lowest = sorted(pitches)[::-1]
            for voice_number, pitch in enumerate(sorted_pitches_from_highest_to_lowest):
                if (step, pitch) in note_to_velocity_dict.keys():
                    velocity_roll[step, voice_number] = note_to_velocity_dict[(step, pitch)]
                if (step, pitch) not in note_to_duration_dict.keys():
                    #if the note is in the dictionary, it means that it is the start of the note
                    #if its not the start of a note, it means it is held
                    held_note_roll[step, voice_number] = 1

        piano_rolls.append(piano_roll)
        velocity_rolls.append(velocity_roll)
        held_note_rolls.append(held_note_roll)

load_rolls('example.mid')