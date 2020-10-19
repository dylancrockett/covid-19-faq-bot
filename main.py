from faq_bot import FAQBot

# initialize the FAQ bot
bot = FAQBot(False)


if __name__ == "__main__":
    print("#############################")
    print("   Welcome to the COVID-19")
    print("           Help Bot")
    print("#############################")
    print("")
    print("Enter a question you have about COVID19, 'Q' to quit, or 'about' for")
    print("more information about this bot and where the responses come from.")
    print("")
    print("############################")
    print("")

    # start the main program loop
    while True:
        query = input("> ")

        if query == "Q" or query == "q":
            break
        elif query == "ABOUT" or query == "about":
            print("\n[COVID-19 FAQ Bot]")
            print("I am a chat bot designed to answer question about the current COVID-19 pandemic using information")
            print("found from the CDC's FAQ page. I may not always give the most relevant responses but all of the")
            print("information I do give can be trusted as it comes directly from the CDC's FAQ page.\n")
            continue
        if query == "":
            continue
        else:
            print("\n[COVID-19 FAQ Bot] \n" + bot.get_faq_response(query) + "\n")
