import yaml
import glob
import os
import numpy as np

_keys_ = np.array([
    'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B',
])

_numerals_ = np.array([
    'I', 'bII', 'II', 'bIII', 'III', 'IV', 'bV', 'V', 'bVI', 'VI', 'bVII', 'VII'
])


def metronome(bpm=120, time_signature='4/4'):
    if time_signature == '2/4':
        time_signature = 0
    elif time_signature == '3/4':
        time_signature = 1
    elif time_signature == '4/4':
        time_signature = 2
    elif time_signature == '5/8':
        time_signature = 3
    elif time_signature == '6/8':
        time_signature = 4
    elif time_signature == '7/8':
        time_signature = 5
    elif time_signature == '8/8':
        time_signature = 6
    elif time_signature == '9/8':
        time_signature = 7
    elif time_signature == '10/8':
        time_signature = 8
    elif time_signature == '11/8':
        time_signature = 9
    elif time_signature == '12/8':
        time_signature = 10
    elif time_signature == '13/8':
        time_signature = 11
    else:
        raise AssertionError('No such time signature: ' + str(time_signature))
                             
    return '<iframe src="https://guitarapp.com/metronome-embed.html?tempo='+ str(bpm) + '&timeSignature=' + str(time_signature) + '2&pattern=1" title="Metronome" style="width: 360px; height:520px; border-style: none; border-radius: 4px;"> </iframe>'


def transpose(degree, key):
    if key == 'Roman Numeral':
        return degree
    return _keys_[(np.argwhere(_numerals_ == degree).flatten()[0] + np.argwhere(_keys_ == key).flatten()[0]) % 12]

with open('mkdocs.yml', 'r') as file:
    mkdocs_yaml = yaml.safe_load(file)

songs = []
for f in glob.glob('songs/*.y?ml'):
    with open(f, 'r') as file:
        song = yaml.safe_load(file)

    outfile = os.path.splitext(f)[0] + '.md'
    songs.append({song['title'] : outfile})
    with open('docs/' + outfile, 'w') as docfile:
        docfile.write('# ' + song['title'] + os.linesep)
        docfile.write('' + song['description'] + os.linesep)
        docfile.write(os.linesep)
                             
        docfile.write(metronome(song['tempo'], song['time_signature']) + os.linesep)

        docfile.write('##  ' + 'Videos' + os.linesep)
        for i in song['similar']:
            docfile.write('- ' + i['link'] + os.linesep)
            docfile.write(' ' + i['description'] + os.linesep)
        docfile.write(os.linesep)

        docfile.write('##  ' + 'Backing Tracks' + os.linesep)
        for i in song['backtracks']:
            docfile.write('- ' + i['link'] + os.linesep)
            docfile.write(' ' + i['description'] + os.linesep)
        docfile.write(os.linesep)

        docfile.write('#  ' + 'Keys' + os.linesep)
        docfile.write('Common keys:' + os.linesep)
        for k in song['commonkeys']:
            docfile.write(' - ' + '['+k+'](#'+k+')' + os.linesep)

        for key in ['Roman Numeral'] + _keys_.tolist():
            docfile.write('## ' + key + os.linesep)
            for part in song['chords']:
                lines = song['chords'][part].split('\n')
                # print table header
                for i in range(len(lines[0].split())):
                    if i==0:
                        docfile.write(' | ' + part + '\t')
                    else:
                        docfile.write(' |  \t')
                docfile.write('|' + os.linesep)
                for i in range(len(lines[0].split())):
                    docfile.write(' |----------\t')
                docfile.write('|' + os.linesep)

                for line in lines:
                    print(line)
                    for tag in line.split():
                        extensions_str = ''
                        quality = ''
                        bassnote = ''
                        tokens = tag.split(',')
                        degree = tokens[0]
                        if degree != '%':
                            degree = transpose(degree, key)
                        if len(tokens) > 1:   
                            quality = tokens[1]
                        if len(tokens) > 2:
                            bassnote = tokens[2]
                            bassnote = '<sub>' + bassnote + '</sub>'
                        if len(tokens) > 3:
                            extensions = tokens[3:]
                            extensions_str = '<sup>'
                            for i, e in enumerate(extensions):
                                extensions_str += e
                                if i != len(extensions)-1:
                                    extensions_str += ','
                            extensions_str += '</sup>'
                        docfile.write(' | ' + degree + quality + ' ' + bassnote + extensions_str + '\t')
                    docfile.write(' |' + os.linesep)
                docfile.write(os.linesep)
            docfile.write(os.linesep)

mkdocs_yaml['nav'][1]['Songs'] = songs

with open('mkdocs.yml', 'w') as file:
    yaml.dump(mkdocs_yaml, file)

