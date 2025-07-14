from transformers import BertTokenizer

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
text = 'Some randomness text gives for the output'
tokens = tokenizer.tokenize(text)
print('The tokens used in:',tokens)
tokenid = tokenizer.convert_tokens_to_ids(tokens)
print('the token ids are:',tokenid)
decodetoken = tokenizer.decode(tokenid)
print('the decoded tokenid is',decodetoken)

