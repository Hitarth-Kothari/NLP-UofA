# HELPER FILE

import os, sys
from pathlib import Path


def make_dict(file):
    
    dict = {}

    with open(file, 'r') as file1:
        lines = file1.read().splitlines() 
        correct_tag = None

        for line in lines:
            if line.__contains__('Correct Tag: ') and correct_tag == None:
                correct_tag = line.replace('Correct Tag: ', '')

                if correct_tag not in dict:
                    dict[correct_tag] = []
                    
                    
            elif correct_tag != None and line != '' and line.__contains__('Incorrect Tag:') == True:
                continue
                
            elif correct_tag != None and line != '' and line.__contains__('Incorrect Tag:') == False:
                tag, freq = line.replace('        - ', '').split(': ')[0], int(line.replace('        - ', '').split(': ')[1])
                exist = False
                for x in dict[correct_tag]:
                    if tag in x:
                        x[tag] += freq
                        exist = True
                        
                if exist == False:
                    dict[correct_tag].append({tag: freq})

            elif correct_tag != None and line == '':
                correct_tag = None
                    
    return dict


if __name__ == '__main__':
    
    parent = Path.cwd()

    files = {f'{parent}/output/error_tables/test_brill_table_output.txt': 'Most errors of BRILL (>10) in test.txt\n', f'{parent}/output/error_tables/test_ood_brill_table_output.txt': 'Most errors of BRILL (>10) in test_ood.txt\n',
             f'{parent}/output/error_tables/test_hmm_table_output.txt': 'Most errors of HMM (>10) in test.txt\n', f'{parent}/output/error_tables/test_ood_hmm_table_output.txt': 'Most errors of HMM (>10) in test_ood.txt\n'}
    
    f= open(f'{parent}/output/error_tables/most_incorrect_tags.txt',"w+")
    
    for file in files:
        
        f.write(f'{files[file]}\n')
                
        the_dict = make_dict(file)

        for correct_key, all_incorrects in the_dict.items():
            maxim = 0
            incorrect_tag_most = None
            for incorrect_tags in all_incorrects:
                incorrect_key, freq = list(incorrect_tags.keys())[0], incorrect_tags[list(incorrect_tags.keys())[0]]
                
                if freq > maxim:
                    maxim = freq
                    incorrect_tag_most = incorrect_key

            if maxim > 10:
            
                f.write(f'{correct_key} misclassified most with {incorrect_tag_most} - {maxim}\n')
        
        f.write(f'\n')
         
    f.close()