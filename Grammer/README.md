# Intro to NLP - Assignment 2 with Dataset Version 2

## Team

| Student name    | CCID    |
| --------------- | ------- |
| Amman Das       | amman1  |
| Hitarth Kothari | hitarth |

## TODOs

In this file you **must**:

- [*] Fill out the team table above. Please note that CCID is **different** from your student number.
- [*] Acknowledge all resources consulted (discussions, texts, urls, etc.) while working on an assignment. Non-detailed oral discussion with others is permitted as long as any such discussion is summarized and acknowledged by all parties.
- [*] Provide clear installation and execution instructions that TAs must follow to execute your code.

## Execution

Example usage: use the following command in the current directory.

`python3 src/main.py data/train.tsv grammars/toy.cfg output/train.tsv`

## Data

The assignment's train data can be found in [data/train.tsv](data/train.tsv).

## Acknowledgement

**How to Execute**

1. Make sure all required libraries are installed. Install them using the provided `requirements.txt` file:

   ```bash
   pip install -r requirements.txt
   ```

   or

   ```bash
   pip3 install -r requirements.txt
   ```

2. Execute the main Python script:

   ```bash
   python src/main.py data/train.tsv grammars/toy.cfg output/train.tsv
   ```

   or

   ```bash
   python3 src/main.py data/train.tsv grammars/toy.cfg output/train.tsv
   ```

**Output**

The output folder contains 3 files:-

1. `output/train.tsv` contains the output with the following columns

   | Column name  | Description                                                                                                                                       |
   | ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------- |
   | id           | The id of the input sentence.                                                                                                                     |
   | ground_truth | The ground truth label of the input sentence, copied from the original data/train.tsv.                                                            |
   | prediction   | 1 if the sentence has grammar errors, 0 if not. In other words, whether the POS sequence can be parsed successfully with your grammar and parser. |

2. `output/metrics.txt` contains 7 important metrics

   - Precision: Important when the cost of false positives is high

   - Recall: Important when the cost of false negatives is high

   - F1 score: considers both the precision and recall

   - FN: False Negatives (ground truth is 1 but prediction is 0)

   - FP: False Positives (ground truth is 0 but prediction is 1)

   - TP: True Positives (ground truth is 1 but prediction is 1)

   - TN: True Negatives (ground truth is 0 but prediction is 0)

3. `output/incorrect_output.tsv` is an additional file that contains the incorrect outputs (pos sequences were parsed incorrectly)

**Links Referenced**

A variety of links and resources were used to help put together the coding tasks

1. Links that helped in programming the tasks and their use

   - https://www.analyticsvidhya.com/blog/2020/09/precision-recall-machine-learning/

     - Performing the precision and recall against a dataset

   - https://www.nltk.org/howto/parse.html

     - Using the CFG library to parse the string file "toy.cfg" containing the grammar

2. ChatGPT helped in the following tasks

   - Fixing of bugs in using the sys library
     - Prompt - "How is the sys library used, and how to get the arguments into a Path format?"
   - Precision and Recall
     - Prompt - "How to store precision and recall stores from a file?"
