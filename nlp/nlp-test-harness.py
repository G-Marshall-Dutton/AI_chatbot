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

# get user input, classify
while(True):
    # get user input
    userInput = input("Input for NLP > ")

    # get journey info test
    nlp_response = re.get_journey_info(userInput, dict)

    # print results of classifying
    print('get_journey_info returns:')
    print(dict)

