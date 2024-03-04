import re
import json
from collections import Counter
import os

STOP_WORDS = {
    "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours",
    "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers",
    "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves",
    "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are",
    "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does",
    "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until",
    "while", "of", "at", "by", "for", "with", "about", "against", "between", "into",
    "through", "during", "before", "after", "above", "below", "to", "from", "up", "down",
    "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here",
    "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more",
    "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so",
    "than", "too", "very",
}

def extract_two_word_phrases(text):
    words = re.findall(r'\b\w+\b', text.lower())
    filtered_words = [word for word in words if word not in STOP_WORDS and '\\' not in word and '_' not in word]
    two_word_phrases = [' '.join(pair) for pair in zip(filtered_words[:-1], filtered_words[1:])]
    return two_word_phrases

def most_common_phrases(two_word_phrases, n=10):
    phrase_counts = Counter(two_word_phrases)
    return phrase_counts.most_common(n)

def process_file(input_file_name, output_file_name, n=1000):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file_path = os.path.join(script_dir, input_file_name)
    output_file_path = os.path.join(script_dir, output_file_name)

    if not os.path.exists(input_file_path):
        print(f"Input file '{input_file_path}' not found.")
        return

    try:
        with open(input_file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except Exception as e:
        print(f"Failed to read input file: {e}")
        return

    two_word_phrases = extract_two_word_phrases(text)
    if not two_word_phrases:
        print("No valid two-word phrases found.")
        return

    common_phrases = most_common_phrases(two_word_phrases, n)
    data = {'two_word_phrases': {phrase: count for phrase, count in common_phrases}}

    try:
        with open(output_file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        print(f"Output written to '{output_file_path}'")
    except Exception as e:
        print(f"Failed to write output file: {e}")

input_file = 'tsd.txt' 
output_file = 'tsd.json'
process_file(input_file, output_file)
