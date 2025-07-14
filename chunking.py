import nltk

text= 'Random sentence which has been prepared for an output'

sentence = nltk.sent_tokenize(text)
print('Before the for loop how the sentence look to be',sentence)

for sent in sentence:
 print(f"\nSentence: {sent}")
 words =nltk.word_tokenize(sent)
 print("Tokens:" , words)
 pos_tags = nltk.pos_tag(words)
 print("Parts of Speech Tags:",pos_tags)

 
 
