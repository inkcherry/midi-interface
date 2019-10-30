import  numpy as np
category_list = {'Drums': [], 'Piano': [],'Chromatic Percussion':[],'Organ':[],'Guitar': [],'Bass': [],   'Strings': [], 'Ensemble': [],
                 'Brass': [], 'Reed': [], 'Pipe': [], 'Synth Lead': [], 'Synth Pad': [],
                 'Synth Effects': [], 'Ethnic': [], 'Percussive': [], 'Sound Effects': []}


program_dict = { 'Drums': 0,'Piano': 0, 'Chromatic Percussion': 8, 'Organ': 16, 'Guitar': 24, 'Bass': 32, 'Strings': 40,
                'Ensemble': 48, 'Brass': 56, 'Reed': 64, 'Pipe': 72, 'Synth Lead': 80, 'Synth Pad': 88,
                'Synth Effects': 96,
                'Ethnic': 104, 'Percussive': 112, 'Sound Effects': 120
                }
track_info= (
    'Drums', 'Piano','Chromatic Percussion', 'Organ','Guitar', 'Bass' ,'Strings', 'Ensemble',
    'Brass', 'Reed', 'Pipe', 'Synth Lead', 'Synth Pad',
    'Synth Effects', 'Ethnic', 'Percussive', 'Sound Effects'
)
for i in range(128):
    k=i//8+1
    a=np.zeros(1)
    a[0]=k
    print(category_list[track_info[i//8+1]].append(a))
    print(k)
for key in category_list:
    print(category_list[key])
