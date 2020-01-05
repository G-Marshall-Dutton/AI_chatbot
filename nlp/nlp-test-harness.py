import nlp

# get an nlp object
re = nlp.ReasoningEngine()

# test dictionary for passing into nlp
#{from: to: date: time:}
dict = {
    "from": None,
    "to": None,
    "date": None,
    "time": None
}

# test dictionary for passing into nlp for delay
#{from: to: at: delay_mins:}
delay_dict = {
    "from": None,
    "to": None,
    "at": None,
    "delay_mins": None
}


# get user input, classify
while(True):
    # get user input
    userInput = input("Input for NLP > ")

    # # TEST CODE FOR RESPONSES
    # # get journey info test
    # nlp_response = re.get_journey_info(userInput, dict)

    # # print results of classifying
    # print('get_journey_info returns:')
    # print(dict)


    # # TEST CODE FOR CLASSIFYING

    # # classify input
    # # nlp_classified = re.classify_user_sentence(userInput)

    # # print classification returned
    # # print(nlp_classified)


    # # # TEST CODE FOR AFFIRMATOR
    # # nlp_affirm = re.affirmation(userInput)

    # # print(nlp_affirm)


    # TEST CODE FOR DELAY 
    # get delay info test
    nlp_response = re.get_delay_info(userInput, delay_dict)

    # print results of classifying
    print('get_delay_info returns:')
    print(delay_dict)
