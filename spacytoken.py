import spacy 

nlp = spacy.load('en_core_web_sm')

text = 'Hi My name is Keerthivasan , Working as an ML Trainee in AIT'

docx = nlp(text)
print('Here is the tokenization happens')
for t in docx:
 print('/n',t)