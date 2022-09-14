import yaml
import glob
import os
import numpy as np

_keys_ = np.array([
    'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Bb', 'B', 'Cb'
])

_numerals_ = np.array([
    'I', 'bII', 'II', 'bIII', 'III', 'IV', 'bV', 'V', 'vVI', 'VI', 'bVII', 'VII'
])


def transpose(degree, key):
    if key == 'Roman Numeral':
        return degree
    return _keys_[(np.argwhere(_numerals_ == 'I').flatten()[0] + np.argwhere(_keys_ == 'C').flatten()[0])%12]

with open('mkdocs.yml', 'r') as file:
    mkdocs_yaml = yaml.safe_load(file)

songs = []
for f in glob.glob('songs/*.y?ml'):
    with open(f, 'r') as file:
        song = yaml.safe_load(file)
        print(song)

    outfile = os.path.splitext(f)[0] + '.md'
    songs.append({song['title'] : outfile})
    with open('docs/' + outfile, 'w') as docfile:
        docfile.write('# ' + song['title'] + os.linesep)
        docfile.write('' + song['description'] + os.linesep)
        docfile.write(os.linesep)

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
                    for tag in line.split():
                        tokens = tag.split(',')
                        degree = tokens[0]
                        if degree == '%':
                            if len(tokens)>1:
                                # quality doesn't change
                                quality = ''
                                extensions = tokens[1:]
                        else:
                            degree = transpose(degree, key)
                            quality = tokens[1]
                            if len(tokens) > 2:
                                extensions = tokens[2:]
                        docfile.write(' | ' + degree + quality + ' ' + str(extensions) + '\t')
                    docfile.write(' |' + os.linesep)
                docfile.write(os.linesep + os.linesep)

mkdocs_yaml['nav'][1]['Songs'] = songs

with open('mkdocs.yml', 'w') as file:
    yaml.dump(mkdocs_yaml, file)

