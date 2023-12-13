import nltk
from nltk.tag import hmm
from nltk.tag import brill, BrillTaggerTrainer, RegexpTagger
from nltk.probability import LaplaceProbDist, ELEProbDist, WittenBellProbDist
import sys
from pathlib import Path
from sklearn.model_selection import KFold

# Function to read data from a file
def read_data(file_path):
    sentences = []
    current_sentence = []
    with open(file_path, 'r') as file:
        for line in file:
            if line.strip():  # Non-empty line
                word, tag = line.split()
                current_sentence.append((word, tag))
            elif current_sentence:
                sentences.append(current_sentence)
                current_sentence = []

    # Add the last sentence if the file doesn't end with a blank line
    if current_sentence:
        sentences.append(current_sentence)

    return sentences

def laplace_estimator(fd, bins):
    return LaplaceProbDist(fd, bins)

def ele_estimator(fd, bins):
    return ELEProbDist(fd, bins)

def witten_bell_estimator(fd, bins):
    return WittenBellProbDist(fd, bins)

def test_hmm(output_path, training_data, test_data):

    num_states_range = range(2, 10)
    estimators = {ele_estimator: "ele estimator", laplace_estimator: "laplace estimator", witten_bell_estimator: "witten bell estimator"}  # List of estimators
    best_accuracy = 0
    best_hmm_model = None
    best_estimator = None
    best_num_states = None

    for num_states in num_states_range:
        for estimator in estimators:
            states_list = list(range(num_states))
            trainer = hmm.HiddenMarkovModelTrainer(states=states_list)
            hmm_model = trainer.train_supervised(training_data, estimator=estimator)
            accuracy = hmm_model.accuracy(test_data)

            if accuracy > best_accuracy:
                best_accuracy = accuracy
                best_hmm_model = hmm_model
                best_num_states = num_states
                best_estimator = estimators[estimator]

    correct = 0
    total = 0
    with open(output_path, 'w') as output_file:
        for sentence in test_data:
            words = [word for word, tag in sentence]
            tagged = best_hmm_model.tag(words)

            for ((word, actual_tag), (predicted_word, predicted_tag)) in zip(sentence, tagged):
                output_file.write(f"{predicted_word} {predicted_tag}\n")
                if actual_tag == predicted_tag:
                    correct += 1
                total += 1
            if sentence != test_data[-1]:
                output_file.write("\n")

    test_accuracy = correct / total if total > 0 else 0
    print(f"Test accuracy for HMM: {test_accuracy}, with best number of hidden states {best_num_states} and best estimator {best_estimator}")


# Inside the cross_validate_brill and test_brill functions

def cross_validate_brill(data, num_folds):
    kf = KFold(n_splits=num_folds)
    scores = []

    for train_index, test_index in kf.split(data):
        train_data = [data[i] for i in train_index]
        test_data = [data[i] for i in test_index]

        # Edge Case taggers
        # Initiall found on https://www.nltk.org/api/nltk.tag.brill_trainer.html, then was further editted
        baseline_tagger = RegexpTagger([
        (r'.*\d.*', 'CD'),                 # cardinal numbers
        (r'(The|the|A|a|An|an)$', 'AT'),   # articles
        (r'.*able$', 'JJ'),                # adjectives
        (r'.*ful$', 'JJ'),                 # adjectives
        (r'.*al$', 'JJ'),                  # adjectives
        (r'.*ic$', 'JJ'),                  # adjectives
        (r'.*ious$', 'JJ'),                # adjectives
        (r'.*-.*', 'JJ'),                  # adjectives
        (r'.*ian$', 'JJ'),                 # adjectives
        (r'.*tive$', 'JJ'),                # adjectives
        (r'.*self$', 'PRP'),               # Perposition
        (r'.*ness$', 'NN'),                # nouns formed from adjectives
        (r'.*ly$', 'RB'),                  # adverbs
        (r'.*s$', 'NNS'),                  # plural nouns
        (r'.*ing$', 'VBG'),                # gerunds
        (r'.*ed$', 'VBD'),                 # past tense verbs
        (r'.*\'d$', 'VBD'),                # past tense verbs
        (r'.*', 'NN')                      # nouns (default)
        ])

        # Ngram taggers
        unigram_tagger = nltk.UnigramTagger(training_data, backoff=baseline_tagger)
        bigram_tagger = nltk.BigramTagger(training_data, backoff=unigram_tagger)
        trigram_tagger = nltk.TrigramTagger(training_data, backoff=bigram_tagger)

        # Experiment with different templates
        templates = brill.brill24()

        # Experiment with the max_rules parameter
        brill_trainer = BrillTaggerTrainer(trigram_tagger, templates, trace=0)
        brill_tagger = brill_trainer.train(train_data, max_rules=10)  # Adjust max_rules as needed

        accuracy = brill_tagger.accuracy(test_data)
        scores.append(accuracy)

    average_score = sum(scores) / len(scores)
    return average_score

def test_brill(output_path, training_data, test_data):
    num_folds = 5

    # Experiment with different templates and max_rules
    cross_val_score = cross_validate_brill(training_data, num_folds)
    print(f"Cross-validated Brill Tagger Accuracy: {cross_val_score}")

    # Edge Case taggers
    # Initiall found on https://www.nltk.org/api/nltk.tag.brill_trainer.html, then was further editted
    # Used to be just NN , with accurace 0.80~
    baseline_tagger = RegexpTagger([
    (r'.*\d.*', 'CD'),                 # cardinal numbers
    (r'(The|the|A|a|An|an)$', 'AT'),   # articles
    (r'.*able$', 'JJ'),                # adjectives
    (r'.*ful$', 'JJ'),                 # adjectives
    (r'.*al$', 'JJ'),                  # adjectives
    (r'.*ic$', 'JJ'),                  # adjectives
    (r'.*ious$', 'JJ'),                # adjectives
    (r'.*-.*', 'JJ'),                  # adjectives
    (r'.*ian$', 'JJ'),                 # adjectives
    (r'.*tive$', 'JJ'),                # adjectives
    (r'.*self$', 'PRP'),               # Perposition
    (r'.*ness$', 'NN'),                # nouns formed from adjectives
    (r'.*ly$', 'RB'),                  # adverbs
    (r'.*s$', 'NNS'),                  # plural nouns
    (r'.*ing$', 'VBG'),                # gerunds
    (r'.*ed$', 'VBD'),                 # past tense verbs
    (r'.*\'d$', 'VBD'),                # past tense verbs
    (r'.*', 'NN')                      # nouns (default)
    ])

    # Ngram taggers
    unigram_tagger = nltk.UnigramTagger(training_data, backoff=baseline_tagger) # used to be just this
    bigram_tagger = nltk.BigramTagger(training_data, backoff=unigram_tagger)
    trigram_tagger = nltk.TrigramTagger(training_data, backoff=bigram_tagger) # This helped

    # Experiment with different templates and max_rules
    templates = brill.brill24()
    brill_trainer = BrillTaggerTrainer(trigram_tagger, templates, trace = 0)
    brill_tagger = brill_trainer.train(training_data, max_rules=100)  # changed from 10 to 100, anymore is same

    correct = 0
    total = 0
    with open(output_path, 'w') as output_file:
        for sentence in test_data:
            words = [word for word, tag in sentence]
            tagged = brill_tagger.tag(words)

            for ((word, actual_tag), (predicted_word, predicted_tag)) in zip(sentence, tagged):
                output_file.write(f"{predicted_word} {predicted_tag}\n")
                if actual_tag == predicted_tag:
                    correct += 1
                total += 1
            if sentence != test_data[-1]:
                output_file.write("\n")

    test_accuracy = correct / total if total > 0 else 0
    print(f"Test accuracy: {test_accuracy}")

def generate_diff_table(file1_path, file2_path, table_path):
    # Read the contents of the files
    with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
        correct_tags = file1.readlines()
        wrong_tags = file2.readlines()

    # Ensuring both files have the same number of lines
    assert(len(correct_tags) == len(wrong_tags))

    # Initialize the dictionary to store tag frequencies
    tag_frequency = {}

    # Process each line and populate the dictionary
    for correct, wrong in zip(correct_tags, wrong_tags):
        correct_parts = correct.strip().split()
        wrong_parts = wrong.strip().split()

        # Skip lines that don't have the expected format
        if len(correct_parts) < 1 or len(wrong_parts) < 1:
            continue

        correct_tag = correct_parts[-1]
        
        wrong_tag = wrong_parts[-1]

        if correct_tag != wrong_tag:
            if correct_tag not in tag_frequency:
                tag_frequency[correct_tag] = {}

            if wrong_tag in tag_frequency[correct_tag]:
                tag_frequency[correct_tag][wrong_tag] += 1
            else:
                tag_frequency[correct_tag][wrong_tag] = 1

    # Writing the dictionary to the table file in the specified format
    with open(table_path, 'w+') as table_file:
        for correct_tag, wrong_tags_dict in tag_frequency.items():
            table_file.write(f"Correct Tag: {correct_tag}\n")
            table_file.write("    - Incorrect Tag: \n")
            for wrong_tag, frequency in wrong_tags_dict.items():
                table_file.write(f"        - {wrong_tag}: {frequency}\n")
            table_file.write("\n")  # Adding a newline for better readability between entries

if __name__ == "__main__":
    # Get the current working directory
    parent = Path.cwd()
    tagger, train, test, output = None, None, None, None
    
    if len(sys.argv) == 9:
        assert sys.argv[1] == '--tagger' and sys.argv[3] == '--train' and sys.argv[5] == '--test' and sys.argv[7] == '--output', f"inccorect arguments"
        tagger, train, test, output = sys.argv[2], sys.argv[4], sys.argv[6], sys.argv[8]

    else:
        sys.exit(1)
    
    training_data = read_data(train)
    test_data = read_data(test)
    
    if tagger == 'hmm':
        test_hmm(output, training_data, test_data)
    elif tagger == 'brill':
        test_brill(output, training_data, test_data)
    
    if test.__contains__('ood'):
        string_test = 'test_ood'
        
    else:
        string_test = 'test'
    
    # Uncomment to generate the error output tables

    #generate_diff_table(test, output, f'{parent}/output/error_tables/{string_test}_{tagger}_table_output.txt')
        
        