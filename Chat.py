from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

# Making CHatbot object
chatbot = ChatBot(
    'Cheeky',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
)

chatbot.initialize()

# Make the trainer
trainer = ChatterBotCorpusTrainer(chatbot)
# train it
trainer.train('chatterbot.corpus.english')

a = ''
while a != exit:
    a = str(input('Enter something'))

    # Get a response to an input statement
    r = str(chatbot.get_response(a))
    print(r)
