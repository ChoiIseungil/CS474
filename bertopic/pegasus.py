import torch
from transformers import PegasusForConditionalGeneration, PegasusTokenizer
import numpy as np
from bertopic import BERTopic
model_name = 'tuner007/pegasus_summarizer'
torch_device = 'cuda' if torch.cuda.is_available() else 'cpu'
tokenizer = PegasusTokenizer.from_pretrained(model_name)
model = PegasusForConditionalGeneration.from_pretrained(model_name).to(torch_device)


def get_response(input_text):
  batch = tokenizer([input_text],truncation=True,padding='longest',max_length=1024, return_tensors="pt").to(torch_device)
  gen_out = model.generate(**batch,max_length=128,num_beams=5, num_return_sequences=1, temperature=1.5)
  output_text = tokenizer.batch_decode(gen_out, skip_special_tokens=True)
  return output_text

topic_model = BERTopic(min_topic_size=20, top_n_words = 8)
file_path = "/home/cs474/CS474/data/data.csv"

of = open(file_path, 'r')
rf = of.read()
of.close()
splitted = rf.split('\n')[1:-1]
splitted = list(zip(*[[a.split(',')[0], ','.join(a.split(',')[1:-2]), a.split(',')[-2], a.split(',')[-1]] for a in splitted]))
titles = splitted[0]
docs = splitted[1]
dates = splitted[2]
sections = splitted[3]
topics, probs = topic_model.fit_transform(docs)
print(len(topic_model.get_topic_info()))
print(topic_model.get_topic_info()[:30])



# get documents per class
topic_docs = {topic: [] for topic in set(topics)}
for topic, doc in zip(topics, docs):
    topic_docs[topic].append(doc)

resulting_text = get_response(topic_model.get_representative_docs()[0][0])

