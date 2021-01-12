from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

# Making Chatbot object
chatbot = ChatBot(
    'Cheeky',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
)


def InitializeBot():
    print('a')
    chatbot.initialize()
    # Make the trainer
    trainer = ChatterBotCorpusTrainer(chatbot)
    # train it
    trainer.train('chatterbot.corpus.english')


def GetReply(request):
    r = str(chatbot.get_response(request))
    return r


# InitializeBot()
# while True:
#     a = input("ENTER SOMETHING, FAST   ")
#     print(GetReply(a))
