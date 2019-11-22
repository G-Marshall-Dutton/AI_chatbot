import nlp

# get an nlp object
re = nlp.ReasoningEngine()



# get user input, classify
while(True):
    # get user input
    userInput = input("> ")

    #{from: to: date: time:}
    dict = {
        "from": None,
        "to": None,
        "date": None,
        "time": None
    }

    # get journey info test
    nlp_response = re.get_journey_info(userInput, dict)

    # print results of classifying
    print(nlp_response)
    print('Dict is now:')
    print(dict)

