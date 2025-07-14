from transformers import BertTokenizer, BertModel
import torch

# Load pre-trained BERT
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

# Input sentence
text = "LangChain helps build applications using language models."

# Tokenize input
inputs = tokenizer(text, return_tensors='pt')
print("Tokens:", tokenizer.convert_ids_to_tokens(inputs['input_ids'][0]))

# Get token embeddings from BERT
with torch.no_grad():
    outputs = model(**inputs)
    last_hidden_states = outputs.last_hidden_state  # Shape: [1, seq_len, 768]

# Each token has a 768-dimensional embedding
print("Token Embedding shape:", last_hidden_states.shape)

# Example: embedding of the first token ([CLS])
cls_embedding = last_hidden_states[0][0] 
print("CLS Embedding vector:", cls_embedding[:5])
