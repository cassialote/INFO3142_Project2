
  #ch. 4 or 5 -> dealing with financial dataclass


import spacy
nlp = spacy.load('en_core_web_sm')

#read in file
fo = open('EmailLog.txt', 'r+');
fileData = fo.read();
print("The following text was read: ", fileData);
fo.close();





