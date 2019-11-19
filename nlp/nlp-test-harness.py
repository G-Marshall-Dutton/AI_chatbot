import nlp

# get an nlp object
re = nlp.ReasoningEngine()



# get user input, classify
while(True):
    # get user input
    userInput = input("> ")

    # classify
    nlp_response = re.get_journey_info(userInput)

    # print results of classifying
    print(nlp_response)

