# Intro to NLP - Assignment 4

## Team

| Student name | CCID    |
| ------------ | ------- |
| student 1    | amman1  |
| student 2    | hitarth |

Please note that CCID is **different** from your student number.

## TODOs

In this file you **must**:

- [*] Fill out the team table above.
- [*] Make sure you submitted the URL on eClass.
- [*] Acknowledge all resources consulted (discussions, texts, urls, etc.) while working on an assignment.
- [*] Provide clear installation and execution instructions that TAs must follow to execute your code.
- [*] List where and why you used 3rd-party libraries.
- [*] Delete the line that doesn't apply to you in the Acknowledgement section.

## Acknowledgement

In accordance with the UofA Code of Student Behaviour, we acknowledge that  
(**delete the line that doesn't apply to you**)

- We did not consult any external resource for this assignment.
- We have listed all external resources we consulted for this assignment.

Non-detailed oral discussion with others is permitted as long as any such discussion is summarized and acknowledged by all parties.

## 3-rd Party Libraries

You do not need to list `nltk` and `pandas` here.

- `main.py L:[105]` used `pandas` for creating the output dataframe.
- `main.py L:[109]` used `pandas` for the confusion matrix.
- `main.py L:[149]` used `numpy` for calculating precision.
- `main.py L:[150]` used `numpy` for calculating recall.

## Execution

1. Make sure all required libraries are installed. Install them using the provided `requirements.txt` file:

   ```bash
   pip install -r requirements.txt
   ```

   or

   ```bash
   pip3 install -r requirements.txt
   ```

2. Example usage: use the following command in the current directory. Etimated runtime **< 10 seconds**

   ```bash
   python3 src/main.py --train data/train.csv --test data/test.csv --output output/test.csv
   ```

## Output

The output is of below, containing the cross validated training accuracy, test accuracy, and the matrices for the respective tables including with precision and recall

```bash
Cross-validated Training Accuracy: 0.89
Test Accuracy: 0.89
Predicted   characters  director  performer  publisher
Actual
characters          83         9          3          8
director             4        85          2          3
performer            7         3         91          2
publisher            2         0          1         97
publisher:
97 13
3 287
publisher recall: 0.97
publisher precision: 0.8818181818181818

director:
85 12
9 294
director recall: 0.9042553191489362
director precision: 0.8762886597938144

performer:
91 6
12 291
performer recall: 0.883495145631068
performer precision: 0.9381443298969072

characters:
83 13
20 284
characters recall: 0.8058252427184466
characters precision: 0.8645833333333334


micro_avg_presision 0.89
micro_avg_recall 0.89

macro_avg_presision 0.8902086262105592
macro_avg_recall 0.8908939268746128
```

**Links Referenced**

A variety of links and resources were used to help put together the coding tasks

1. Links that helped in programming the tasks and their use

   - https://www.guru99.com/pos-tagging-chunking-nltk.html

     - Naive Bayes Scratch Implementation using Python

   - https://github.com/gbroques/naive-bayes/blob/master/naive_bayes/naive_bayes.py

     - Applying smoothing to a naive bayes

2. ChatGPT helped in the following tasks

   - Extracting only the columns from the datasets
     - Prompt - "How to use the csv library to extract the columns in a dataset?"
   - To get an idea of how to tokenize a sentence with regex
     - Prompt - "Give an example of how to tokenize a sentence with regex"
   - Fixing an error in applying smoothing
     - Prompt - "Why does my NaiveBayesClassifier give an error in applying smoothing?"
