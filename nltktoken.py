import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import string

# model for tokenization
nltk.download('punkt')
nltk.download('stopwords')


text = "Hello there! My name is Alice. I'm learning NLP with NLTK, and it's really exciting."

sentences = nltk.sent_tokenize(text)
print("Sentences:")
for s in sentences:
    print("-", s)

# Word Tokenization
words = word_tokenize(text)
print("\nAll Tokens:")
print(words)

# Remove Stopwords and Punctuation
stop_words = set(stopwords.words('english'))
filtered_words = [
    word for word in words 
    if word.lower() not in stop_words and word not in string.punctuation
]
print("\n Filtered Tokens (no stopwords, no punctuation):")
print(filtered_words)

#  Apply Stemming (Optional)
ps = PorterStemmer()
stemmed_words = [ps.stem(word) for word in filtered_words]
print("\n Stemmed Tokens:")
print(stemmed_words)
