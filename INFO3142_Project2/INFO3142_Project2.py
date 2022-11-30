import spacy
nlp = spacy.load('en_core_web_sm')

#read in file
fo = open('EmailLog.txt', 'r+')
file = fo.read()
doc = nlp(file)

#create new file if it does not exist
parsed = open("parsedText.txt", "w")   

#parse file and write to txt
for token in doc:
    if token.like_email:
        parsed.write(f'\nEmail: {token}')
        parsed.write(f'\n=================================\n')

    #extract POS
    if token.tag_== 'VBG' or token.tag_== 'VB':
        parsed.write(f'POS: {token}\n')

    #extract entity tags
    if token.ent_type != 0:
        parsed.write(f'Entity: {token.text} - {token.ent_type_}\n')

fo.close();


#output
with open("emailLog.txt", "r", encoding='utf-8') as testFile:
    text = testFile.read()
    doc = nlp(text)

    total = 0
    email = ''
    amount = 0
    org = ''
    emails = {}
    for sentence in doc.sents:
        listA = [] 
        if sentence.text.__contains__('@') or sentence.text.__contains__('$'): 
            for word in sentence:
                #print("word:", word)
                if word.like_email:
                    email = word
                    emails[word] = {}
                    amount = 0
                    org = ''
                if word.pos_ == "SYM":
                    amount = word.text + word.head.text
                    emails[email][org] = amount
                    if(word.head.text == 'thousand'):
                        number = [w for w in word.head.lefts if w.pos_ == "NUM"]
                        numberThousand = float(number[0].text) * 1000
                        total += numberThousand
                    else:
                        total += float(word.head.text.replace(',',''))
                if word.ent_type_ == 'ORG' and not word.text == 'Inc.':
                    org = word
                    emails[email][org] = amount

            print(email,":",amount,"to",org)

    print("Total Requests:","${:,.2f}".format(total))

    from spacy import displacy
    displacy.serve(doc, style="ent")




