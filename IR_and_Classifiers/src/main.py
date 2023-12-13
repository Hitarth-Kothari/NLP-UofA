import pandas as pd
import numpy as np
import sys
from pathlib import Path
import re
import csv
from collections import defaultdict
import math
import random

class NaiveBayesClassifier:
    def __init__(self):
        self.log_class_priors = {}
        self.word_counts = {}
        self.vocab = set()

    def train(self, data):
        class_counts = defaultdict(int)
        word_counts = defaultdict(lambda: defaultdict(int))
        total_count = 0

        # Count words in each class
        for tokens, label, row_id in data:
            class_counts[label] += 1
            total_count += 1
            for word in tokens:
                word_counts[label][word] += 1
                self.vocab.add(word)

        # Calculate log class priors
        for label in class_counts:
            self.log_class_priors[label] = math.log(class_counts[label] / total_count)

        # Store word counts
        self.word_counts = word_counts

    def predict(self, text):
        # Tokenize and filter non-vocabulary words
        words = set(text)
        words = [word for word in words if word in self.vocab]

        # Calculate class log likelihood
        class_scores = {label: self.log_class_priors[label] for label in self.word_counts.keys()}
        for label, log_prior in class_scores.items():
            log_sum = 0
            for word in words:
                # Laplace smoothing
                log_word_likelihood = math.log((self.word_counts[label].get(word, 0.0) + 1) / (sum(self.word_counts[label].values()) + len(self.vocab)))
                log_sum += log_word_likelihood
            class_scores[label] += log_sum

        return max(class_scores, key=class_scores.get)


def parse_data(file_path):
    data = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)

        for row in reader:
            # The sentence is in the second column (index 1)
            row_id, tokens, relation = row[0], row[1], row[2]

            tokens = tokens.strip('"')
            tokens = tokenize(tokens)
            data.append((tokens, relation, row_id))

    return data

def cross_validate(data, folds=3):
    random.shuffle(data)
    fold_size = len(data) // folds
    accuracies = []

    for i in range(folds):
        start, end = i * fold_size, (i + 1) * fold_size
        test_data = data[start:end]
        train_data = data[:start] + data[end:]

        model = NaiveBayesClassifier()
        model.train(train_data)
        
        correct = 0
        for tokens, label, row_id in test_data:
            prediction = model.predict(tokens)
            if prediction == label:
                correct += 1

        accuracies.append(correct / len(test_data))

    return sum(accuracies) / len(accuracies)

def tokenize(text):
    # Regular expression for word tokenization
    token_pattern = r"(?u)\b\w\w+\b|'\w+|\w+|\S"
    tokens = re.findall(token_pattern, text)
    return tokens
        
def write_predictions_to_file(predictions, file_path):
    output_dataframe = pd.DataFrame(columns=['original_label', 'output_label', 'row_id'])
    for i in range(0, len(predictions)):
        output_dataframe.loc[i] = predictions[i][0],predictions[i][1],predictions[i][2]
    output_dataframe.to_csv(file_path,index=False)
    confusion_matrix = pd.crosstab(output_dataframe['original_label'], output_dataframe['output_label'], rownames=['Actual'], colnames=['Predicted'])
    print(confusion_matrix)
    get_table(output_dataframe)

def get_table(dataframe):
    #Got help from chatgpt
    labels = ('publisher', 'director', 'performer', 'characters')
    precisions = []
    recall = []
    microaverage = [0, 0, 0, 0]
    for label in labels:
        tp =0
        fp=0
        fn=0
        tn=0
        for _ , row in dataframe.iterrows():
            
            if row['output_label'] == label:
                if row['original_label'] == row['output_label']:
                    tp+=1
                else:
                    fp+=1
            else:
                if row['original_label'] == label:
                    fn+=1
                else:
                    tn+=1
        print(label+':')
        print(tp,fp)
        print(fn,tn)
        microaverage[0]+=tp
        microaverage[1]+=tn
        microaverage[2]+=fp
        microaverage[3]+=fn
        print(label, 'recall:',(tp/(tp+fn)))
        print(label, 'precision:',(tp/(tp+fp)),'\n')
        precisions.append((tp/(tp+fp)))
        recall.append((tp/(tp+fn)))
    print('\npooled_micro_avg_presision',(microaverage[0]/(microaverage[2]+microaverage[0])))
    print('pooled_micro_avg_recall',(microaverage[0]/(microaverage[3]+microaverage[0])))
    print('\npooled_macro_avg_presision', np.average(precisions))
    print('pooled_macro_avg_recall',np.average(recall))

if __name__ == "__main__":
    # Get the current working directory
    parent = Path.cwd()
    train, test, output = None, None, None
    
    if len(sys.argv) >= 7:
        assert sys.argv[1] == '--train' and sys.argv[3] == '--test' and sys.argv[5] == '--output', f"inccorect arguments"
        train, test, output = sys.argv[2], sys.argv[4], sys.argv[6]

    else:
        sys.exit(1)
        
    # Parse and process training data
    training_data = parse_data(train)
    accuracy = cross_validate(training_data)
    print(f"Cross-validated Training Accuracy: {accuracy:.2f}")
    
    
    test_data = parse_data(test)
    
    # Train model on the full training data
    model = NaiveBayesClassifier()
    model.train([(tokens, relation, row_id) for tokens, relation, row_id in training_data])

    # Make predictions on test data and calculate accuracy
    predictions = []
    correct_predictions = 0
    for tokens, original_label, row_id in test_data:
        output_label = model.predict(tokens)
        predictions.append([original_label, output_label, row_id])

        if output_label == original_label:
            correct_predictions += 1

    test_accuracy = correct_predictions / len(test_data)
    print(f"Test Accuracy: {test_accuracy:.2f}")

    # Write predictions to output file
    write_predictions_to_file(predictions, output)
    
    