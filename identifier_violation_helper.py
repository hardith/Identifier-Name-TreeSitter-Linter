from word2number import w2n
from itertools import groupby
import enchant


dictionary_detector = enchant.Dict("en_US")
short_identifier_exception_list = ["c","d","e","g","i","in","inOut","j","k","m","n","o","out","t","x","y","z"]

def get_number_of_words(identifier_name):
    index_list = [x for x,y in enumerate(list(identifier_name)) if(y.isupper())] 
    # print(index_list)
    if len(index_list) == 0:
        return 0
    else:
        if index_list[0] != 0:
            return (len(index_list) + 1)
        else:
            return len(index_list)

def check_mixed_case_words(identifier_name):
    #check for starting and ending with _ Ex: _name_
    if (identifier_name.startswith('_')) and (identifier_name.endswith('_')):
        identifier_name = identifier_name[1:-1]
    if identifier_name.startswith('_'):
        identifier_name = identifier_name[1]
    if identifier_name.endswith('_'):
        identifier_name = identifier_name[:-1]

    words = []
    if "_" in identifier_name or "-" in identifier_name:
        new_identifier_name = identifier_name.replace("_", " ")
        new_identifier_name = new_identifier_name.replace("-", " ")
        new_identifier_name = new_identifier_name.lstrip()
        new_identifier_name = new_identifier_name.rstrip()
        words = new_identifier_name.split(" ")
    else:
        for _key, group in groupby(identifier_name, key=lambda x: x.islower()):
            word = "".join(list(tuple(group)))
            if len(word) >0 and len(word) > 1:
                words.append(word)

    lower_word_list = [word for word in words if word.islower()]

    upper_word_list = [word for word in words if word.isupper()]

    if len(lower_word_list) >= 1 and len(upper_word_list) >= 1:
        return True
    else:
        return False

def check_long_identifier_name(identifier_name):
    index_list = [x for x,y in enumerate(list(identifier_name)) if(y.isupper())] 

    if len(index_list) > 0 and index_list[0] != 0:
        index_list = [0] + index_list

    camel_=[]

    for i in range(len(index_list)):
        try:
            camel_.append(identifier_name[index_list[i]:index_list[i+1]])
        except:
            camel_.append(identifier_name[index_list[i]:])

    return any(len(i)>=10 for i in camel_)

def check_identifier_encoding(identifier_name):
    index_list = [x for x,y in enumerate(list(identifier_name)) if(y.isupper())] 

    if len(index_list) > 0 and index_list[0] != 0:
        index_list = [0] + index_list

    camel_=[]

    for i in range(len(index_list)):
        try:
            camel_.append(identifier_name[:index_list[i+1]])
        except:
            camel_.append(identifier_name[index_list[i]:])
            
    if len(camel_) > 0:
        if len(camel_[0]) == 1:
            return True
        else:
            return False
    else:
        return False

def check_capitalisim_anomoly(identifier_name):
    if len(identifier_name) >=2:
        if identifier_name[0].isupper():
            return True
        else:
            return False
    else:
        return False

def check_not_in_dictionary_words(identifier_name):
    index_list = [x for x,y in enumerate(list(identifier_name)) if(y.isupper())] 

    if len(index_list) > 0 and index_list[0] != 0:
        index_list = [0] + index_list

    camel_=[]

    for i in range(len(index_list)):
        try:
            camel_.append(identifier_name[index_list[i]:index_list[i+1]])
        except:
            camel_.append(identifier_name[index_list[i]:])
    
    for i in camel_:
        if not dictionary_detector.check(i):
            return True
    return False

def check_violation(identifier_name):
    violation_list = []
    #-------Capitalisation Anomaly-----------------------------
    if check_capitalisim_anomoly(identifier_name) == True:
        violation_list.append("Capitalisation Anomaly")
        return violation_list

    #-------Consecutive Underscores------------------------------
    if "__" in identifier_name:
        violation_list.append("Consecutive Underscores")

    #-------Dictionary Words-------------------------------------
    if check_not_in_dictionary_words(identifier_name) == True:
        violation_list.append("Dictionary Words")

    #-------Excessive Words-------------------------------------
    number_of_excessive_words = get_number_of_words(identifier_name)
    if number_of_excessive_words > 4:
        violation_list.append("Excessive Words")

    #------Enumeration Identifier Declaration Order--------------

    #------External Underscores------------------
    if (identifier_name.startswith('_')) and (identifier_name.endswith('_')):
        violation_list.append("External Underscores")

    #------Identifier Encoding-------------------
    if check_identifier_encoding(identifier_name) == True:
        violation_list.append("Identifier Encoding")

    #------Long Identifier Name------------------
    if check_long_identifier_name(identifier_name) == True:
        violation_list.append("Long Identifier Name")

    #------Naming Convention Anomoly-------------
    if check_mixed_case_words(identifier_name) == True:
        violation_list.append("Naming Convention Anomoly")

    #------Number of Words----------------------
    number_of_words = get_number_of_words(identifier_name)
    if (number_of_words >= 2 and number_of_words <= 4):
        #valid dont do anything
        pass
    else:
        violation_list.append("Number of Words")

    #------Numeric Identifier Name--------------
    word2num_identifier_name = ""
    #check if string contains _ if so replace with empty spaces
    #Ex: Forty_two to Forty two
    if "_" in identifier_name or "-" in identifier_name:
        word2num_identifier_name = identifier_name.replace("_", " ")
        word2num_identifier_name = word2num_identifier_name.replace("-", " ")
        word2num_identifier_name = word2num_identifier_name.lstrip()
        word2num_identifier_name = word2num_identifier_name.rstrip()
    else:
        word2num_identifier_name = identifier_name
    
    try:
        w2n.word_to_num(word2num_identifier_name)
        violation_list.append("Numeric Identifier Name")
    except:
        pass

    #-------Short Identifier Name-----------------
    if (len(identifier_name) <= 8) and (not(identifier_name in short_identifier_exception_list)):
        violation_list.append("Short Identifier Name")

    return violation_list




