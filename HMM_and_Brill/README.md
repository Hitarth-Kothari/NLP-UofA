# Intro to NLP - Assignment 4

## Team

| Student name | CCID    |
| ------------ | ------- |
| student 1    | hitarth |
| student 2    | amman1  |

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

- We have listed all external resources we consulted for this assignment.
- We counsulted ChatGPT to give us a starting point for our codes, and help find errors when stuck.
- We have also lifted some code from the documentation of nltk modules.

## 3-rd Party Libraries

You do not need to list `nltk` and `pandas` here.

`main.py L:[107]` and `main.py L:[156]` used `re` for manually creating rules for tagging as a final backoff.
`sklearn` was used to implement KFold cross validation in `main.py L:[81]` and `main.py L:[84]`.

## Execution

1. Make sure all required libraries are installed. Install them using the provided `requirements.txt` file:

   ```bash
   pip install -r requirements.txt
   ```

   or

   ```bash
   pip3 install -r requirements.txt
   ```

2. Example usage: use the following command in the current directory. Etimated runtime **~ 10 second** for Brill and **~ 30 seconds** for HMM

   ```bash
   python3 src/main.py --tagger hmm --train data/train.txt --test data/test.txt --output output/test_hmm.txt`
   ```

## Output

The output is either of the format of below for Brill.

```bash
Cross-validated Brill Tagger Accuracy: 0.991120472474776
Test accuracy: 0.8747457134553909
```

or below for HMM

```bash
Test accuracy for HMM: 0.8622493461203139, with best number of hidden states 2 and best estimator witten bell estimator
```

## Structure

The file structure is in accordance with the requirements, but there are additional files and folder that were used:-

- the error_tables folder cosists of 4 output tables: `test_brill_table_output.txt`, `test_ood_brill_table_output.txt`, `test_hmm_table_output.txt` and `test_ood_hmm_table_output.txt`. These files helped put into perspective the most correct-incorrect tag pairs across the different output test files
- `error.py` is used to helped create the `most_incorrect_tags.txt` file, which consists of the high frequency (>10) correct-incorrect tag pairs

These `error_table` files helped put together the report.pdf

## Data

The assignment's training data can be found in [data/train.txt](data/train.txt), the in-domain test data can be found in [data/test.txt](data/test.txt), and the out-of-domain test data can be found in [data/test_ood.txt](data/test_ood.txt).

**Links Referenced**

A variety of links and resources were used to help put together the coding tasks

1. Links that helped in programming the tasks and their use

   - https://www.guru99.com/pos-tagging-chunking-nltk.html

     - POS Tagging example

   - https://gist.github.com/blumonkey/007955ec2f67119e0909

     - Example of using HMM trainer

   - https://www.nltk.org/api/nltk.tag.hmm.html#nltk.tag.hmm.HiddenMarkovModelTagger

     - Documentation of HMM Tagger

   - https://www.geeksforgeeks.org/nlp-brill-tagger/

     - Using the Brill tagger

   - https://www.geeksforgeeks.org/hidden-markov-model-in-machine-learning/

     - Using HMM tagger

2. ChatGPT helped in the following tasks. However, it was not perfect since its knowledge was quite outdated

   - How to start using the brill library from nltk to tag a dataset
     - Prompt - "Give an example of how to start using the brill library from nltk to tag a datasets"
   - Improving the brill tagger, and helped give the idea for a RegexpTagger
     - Prompt - "How to the accuracy of a brill tagger?"
   - Gave a good list of estimators to use for HMM model
     - Prompt - "Give me some good estimators to use for HMM trainer model"
   - Showed implementation of using n-grams for Brill
     - Prompt - "How to use nltk's n-gram Tagger with Brill, specifically for doing backoff?"
