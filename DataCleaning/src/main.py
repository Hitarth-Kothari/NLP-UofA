import os
import re
import shutil

# Check if the clean and transformed directories exist, and remove them if so
if os.path.isdir('clean'):
    shutil.rmtree('clean')

if os.path.isdir('transformed'):
    shutil.rmtree('transformed')

if os.path.isfile('unfound.txt'):
    os.remove('unfound.txt')

os.mkdir('clean')

# Initialize a dictionary to store the CMU dictionary pronounciations
cmudictionary = {}

foundwords = 0
unfoundwords = 0

foundtrans = 0
unfoundtrans = 0

# Method to clean the data and write it to the 'clean' directory
def clean(path_to_clean, path_to_read, cmu_dictionary):

    # Opening the required files to read from/write to
    datafile = open(path_to_read, 'r', encoding="utf8")
    writtenfile = open(path_to_clean, 'w', encoding="utf8")
    unfoundfile = open('unfound.txt', 'a', encoding="utf8")

    found_words = 0
    unfound_words = 0

    for line in datafile:
        if line[0] == '*':
            # Using regex to extract text after a tab and before the end of the line markers(. ! ?)
            store = re.search(r'\t(.+)[\s.?!]$', line)
            if store is not None:
                # Using regex to remove everything but spaces, apostrophes, and alphabets
                firstclean = re.sub(r'[^a-zA-Z\s\']+', '', store.group(1)) #chatGPT
                tokens = firstclean.split()
                for token in tokens:
                    if token.upper() in cmu_dictionary:
                        writtenfile.write(token + '\n')
                        found_words += 1
                    else:
                        # Words with apostrophes are split, then rejoined and added to the CMU dictionary file along with its pronounciation
                        if re.search(r'\'', token):
                            newtokens = re.split(r'\'', token)
                            appostophied = "'" + newtokens[1]
                            if newtokens[0].upper() in cmu_dictionary:
                                if appostophied.upper() in  cmu_dictionary:
                                    found_words += 1
                                    writtenfile.write(token)
                                    cmu_dictionary[token.upper()] = cmu_dictionary[newtokens[0].upper()] + ' ' + cmu_dictionary[appostophied.upper()]
                            writtenfile.write('\n')
                        else:
                            split_point = 0
                            past_index = 0
                            current_word = None
                            word_found = False
                            words_found = []
                            DEBUG_WORDS = []
                            # Words that exist in CMUdict but have no space between them - look for the best place to split the word so that both of them exist in the dict.
                            for i in range(2, len(token)+1):
                                word = token[split_point:i]
                                if token[split_point:i].upper() in cmu_dictionary:
                                    if len(words_found) > 0 and words_found[-1].upper() + token[split_point:i].upper() in cmu_dictionary:
                                        current_word = None
                                        words_found[-1] = words_found[-1] + token[split_point:i]
                                        split_point = i
                                    elif len(words_found) > 0 and words_found[-1][:-1].upper() in cmu_dictionary and words_found[-1][-1].upper() + token[split_point:i].upper() in cmu_dictionary:
                                        current_word = words_found[-1][-1] + token[split_point:i]
                                        words_found[-1] = words_found[-1][:-1]
                                        split_point -= 1
                                    else:
                                        current_word = token[split_point:i]
                                    past_index = i
                                elif len(words_found) > 0 and words_found[-1].upper() + token[split_point:i].upper() in cmu_dictionary:
                                    current_word = words_found[-1] + token[split_point:i]
                                    words_found[-1] = current_word
                                    current_word = None
                                    split_point = i
                                elif current_word is not None:
                                    word_found = True
                                    if  i == len(token) and len(words_found) > 0 and words_found[-1][-1].upper() + token[split_point:i].upper() in cmu_dictionary:
                                        if words_found[-1][:-1] in cmu_dictionary:
                                            current_word = words_found[-1][-1] + token[split_point:i]
                                            words_found[-1] = words_found[-1][:-1]
                                    words_found.append(current_word)
                                    split_point = past_index
                                    current_word = None
                            if current_word is not None:
                                words_found.append(current_word)
                            if token != "".join(words_found):
                                words_found = []
                                word_found = False
                            if token == "".join(words_found):
                                unfoundfile.write(token + ' : ')
                            if word_found == True:
                                cmu_dictionary[token.upper()] = '' #Store the incorrect compounded word in the dictionary for easier access
                            i = 0
                            while i < len(words_found)+1:
                                # Check if the wrods can be joinned to form bigger words that exist in the dictionary
                                joined = "".join(words_found[0:len(words_found)-i])
                                i += 1
                                if joined.upper() in cmu_dictionary and joined != token:
                                    writtenfile.write(joined)
                                    unfoundfile.write(joined + ' ')
                                    cmu_dictionary[token.upper()] += cmu_dictionary[joined.upper()]
                                    DEBUG_WORDS.append(joined)
                                    words_found = words_found[len(words_found)-i+1:]
                                    found_words += 1
                                    if len(words_found) > 1:
                                        i = 0
                            if len(words_found) == 1:
                                writtenfile.write(words_found[0] + "\n")
                                unfoundfile.write(words_found[0])
                                DEBUG_WORDS.append(words_found[0])
                                found_words += 1                   
                            if word_found is not True:
                                # For checking accuracy
                                if token not in {'xxx', 'yyy', 'www'}and len(token)>2:
                                    unfound_words += 1
                                    # unfoundfile.write(token + '\n')
                            if word_found is True:
                                writtenfile.write('\n')
                                unfoundfile.write('\n')
    # Close the files
    datafile.close()
    writtenfile.close()
    unfoundfile.close()
    return found_words, unfound_words

# Method to transform the data and write it to the 'transformed' directory
def transform(path_to_transform, path_to_clean, cmu_dictionary):
    # Opening the required files to read from/write to
    datafile = open(path_to_clean, 'r', encoding="utf8")
    writtenfile = open(path_to_transform, 'w', encoding="utf8")
    found_words = 0
    unfound_words = 0
    for line in datafile:
        if line != '\n':
            line = line.rstrip()
            if line.upper() in cmu_dictionary:
                writtenfile.write(cmu_dictionary[line.upper()] + '\n')
                found_words += 1
            else:
                print(line)
                unfound_words +=1
    # Close the files
    datafile.close()
    writtenfile.close()
    return found_words, unfound_words

# Including only the necessary lines in the cmuDict
def createlibrary(cmu_dictionary):
    dictionary = open('cmudictionary.txt', 'r', encoding="utf8")
    line_counter = 0
    for line in dictionary:
        line_counter += 1
        if line_counter in range (0, 70) or line_counter in range (92, 127):
            continue
        split = line.split('  ', 1)
        cmu_dictionary[split[0]] = split[1][:-1]
    dictionary.close()
createlibrary(cmudictionary)

# Create all the file/folder paths and call all the methods from here in the right order.
for dirpath, dirnames, filenames in os.walk('Data'):
    if not dirnames:
        cleanpath = re.sub('Data', 'clean', dirpath)
        transformedpath = re.sub('Data', 'transformed', dirpath)
        os.makedirs(cleanpath)
        os.makedirs(transformedpath)
        for filename in os.listdir(dirpath):
            if filename.endswith('.cha'):
                newfilename = re.sub('.cha', '.txt', filename)
                pathtoclean = os.path.join(cleanpath, newfilename)
                pathtoread = os.path.join(dirpath, filename)
                pathtotransformed = os.path.join(transformedpath, newfilename)
                x, y = clean(pathtoclean, pathtoread, cmudictionary)
                a, b = transform(pathtotransformed, pathtoclean, cmudictionary)
                foundwords += x
                unfoundwords += y
                foundtrans += a
                unfoundtrans += b
print("Words retained after cleaning: " , foundwords)
print("Words lost during cleaning: " , unfoundwords) #These words can be found in unfound.txt after running the code.
print("Words successfully transformed: " , foundtrans)
print("Words not transformed: " , unfoundtrans)