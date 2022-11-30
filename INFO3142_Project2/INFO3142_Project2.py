#
#	 * Purpose:		To extract some free-form information from a series of (pre-filtered) email messages
#	 * Coder(s):	Cassia Weydtt and Jessica Trigo		
#	 * Date:	    Nov. 30, 2022		
#


import spacy
nlp = spacy.load('en_core_web_sm')

with open("emailLog.txt", "r", encoding='utf-8') as testFile:
    #read in file
    text = testFile.read()
    doc = nlp(text)
   
    # step 1
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
    
    #close file after write
    parsed.close()
    
    # step 2
    email = ''
    org = ''
    amount = 0
    accumulatedAmount = 0
    total = 0
    emails = {}
    for sentence in doc.sents:
        listA = [] 
        if sentence.text.__contains__('@') or sentence.text.__contains__('$'): 
            for word in sentence:
                if word.like_email:
                    email = word
                    emails[word] = {}
                    org = ''
                    amount = 0
                    accumulatedAmount = 0
                if word.pos_ == "SYM":
                    if(word.head.text == 'thousand'):
                        number = [w for w in word.head.lefts if w.pos_ == "NUM"]
                        numberThousand = float(number[0].text) * 1000
                        amount = numberThousand
                        accumulatedAmount += amount
                        total += numberThousand
                    else:
                        amount = float(word.head.text.replace(",",""))
                        accumulatedAmount += amount
                        total += float(word.head.text.replace(',',''))
                if word.ent_type_ == 'ORG' and not word.text == 'Inc.':
                    org = word
                    emails[email][org] = amount

    #output
    phrase = ''
    currentEmail = ''
    currentAmount = ''
    accumulatedAmount = 0
    organizations = ''
    for e_email, e_info in emails.items():
        phrase = ''   
        organizations = ''
        accumulatedAmount = 0

        if currentEmail != e_email.text:
            currentEmail = e_email.text
            phrase += currentEmail + ":"
            orgs = []
            accumulatedOrgs = []
            
            for org in e_info:
                currentAmount = e_info[org]
                orgs.append(" ${:,.2f}".format(currentAmount) + " to " + str(org))   
                
                accumulatedAmount += currentAmount
                accumulatedOrgs.append(str(org))

            for acc_index in range (len(accumulatedOrgs)):
                
                organizations += accumulatedOrgs[acc_index]
                
                if len(accumulatedOrgs) > 1:
                    if acc_index == len(accumulatedOrgs) - 2:
                        organizations += " and "
                    elif acc_index < len(accumulatedOrgs) - 2:
                        organizations += ", "
                    else:
                        organizations += "."

            if len(orgs) > 1:
                phrase += " ${:,.2f}".format(accumulatedAmount) + " to " + organizations 
            
            for org_index in range(len(orgs)):
                
                phrase += orgs[org_index]

                if len(orgs) > 1:
                    if org_index == len(orgs) - 2:
                        phrase += " and"
                    elif org_index < len(orgs) - 2:
                        phrase += ","
                    else:
                        phrase += "."
            print(phrase)
    
    print("\nTotal Requests:","${:,.2f}".format(total))





