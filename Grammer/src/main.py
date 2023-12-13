# Import necessary libraries
import pandas as pd
from pathlib import Path
from nltk import CFG, ChartParser
import os
import sys

# Define a function to access the Context-Free Grammar (CFG) from a file
def accessCFG(grammar_path):
    with open(grammar_path, 'r') as f:
        content = f.read()

    grammar = CFG.fromstring(content)
    return grammar

# Define a function to access and process the data from a TSV file
def accessData(data_path):
    df = pd.read_csv(data_path, sep='\t', engine='python')
    POSTAG_sequences = df[['id', 'label', 'pos']]
    return POSTAG_sequences

# Define a function to parse the data using a CFG and return predictions
def parseData(grammar, data):
    parser = ChartParser(grammar)
    predictions = []

    for _, row in data.iterrows():
        pos_sequence = row['pos'].split()  # Assuming POS tags are space-separated
        try:
            if list(parser.parse(pos_sequence)):
                predictions.append(0)  # No grammar errors
            else:
                predictions.append(1)  # Has grammar errors
        except:
            predictions.append(1)  # Has grammar errors in case of any exception

    return predictions

# Define a function to calculate precision and recall based on predictions and ground truth
def calculate_metrics(predictions, ground_truth):
    TP, FP, FN, TN = 0, 0, 0, 0
    
    for i in range(len(predictions)):
        if predictions[i] == 1 and ground_truth[i] == 1:
            TP += 1
        elif predictions[i] == 1 and ground_truth[i] == 0:
            FP += 1
        elif predictions[i] == 0 and ground_truth[i] == 1:
            FN += 1
        elif predictions[i] == 0 and ground_truth[i] == 0:
            TN += 1
    
    # Calculate precision and recall, with F1
    precision = TP / (TP + FP) if TP + FP != 0 else 0
    recall = TP / (TP + FN) if TP + FN != 0 else 0
    F1 = 2 * ((precision*recall)/(precision+recall)) if precision+recall != 0 else 0

    return precision, recall, TP, FP, FN, TN, F1

def getIncorrectSequences(df):
    filtered_df = df[((df['label'] == 0) & (df['prediction'] == 1)) | ((df['label'] == 1) & (df['prediction'] == 0))]
    return filtered_df

def write_output_results(grammar, data, output_path):
    # Parse the data using the grammar and add predictions to the DataFrame
    data['prediction'] = parseData(grammar, data)

    # Define output file paths
    output_path = Path(f'{parent}/{output_path}').resolve()
    bad_results_path = parent / 'output' / 'incorrect_output.tsv'

    # Check if results.tsv exists and remove it
    remove_existing_file(output_path)

    # Save data with id, label, and predictions to results.tsv
    data[['id', 'label', 'prediction']].to_csv(output_path, sep='\t', index=False)
    getIncorrectSequences(data).to_csv(bad_results_path, sep='\t', index=False)
    
def remove_existing_file(filepath: Path) -> None:
    if filepath.exists():
        os.remove(filepath)

    

def write_metrics_to_file(path, precision, recall, TP, FP, FN, TN, F1):
    with open(path, 'w') as f:
        f.write(f"Precision: {precision}\n")
        f.write(f"Recall: {recall}\n")
        f.write(f"TP: {TP}\n")
        f.write(f"FP: {FP}\n")
        f.write(f"FN: {FN}\n")
        f.write(f"TN: {TN}\n")
        f.write(f"F1: {F1}\n")

if __name__ == "__main__":
    # Get the current working directory
    parent = Path.cwd()

    data_path = sys.argv[1]
    grammar_path = sys.argv[2]
    output_path = sys.argv[3]
    
    # Access the CFG grammar and the data from respective files
    grammar = accessCFG(Path(f'{parent}/{grammar_path}').resolve())
    data = accessData(Path(f'{parent}/{data_path}').resolve())

    # Write the results for with the labels including the predictions
    write_output_results(grammar, data, output_path)

    # Now calculate the necessary metrics for recall and precision
    predictions = parseData(grammar, data)
    precision, recall, TP, FP, FN, TN, F1 = calculate_metrics(predictions, data['label'].tolist())

    # Write precision and recall to the file
    write_metrics_to_file(Path(f'{parent}/output/metrics.txt').resolve(), precision, recall, TP, FP, FN, TN, F1)
