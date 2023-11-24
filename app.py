from openAiFunctions import OpenAiFunctions
#Aqui realizo pruebas manuales 
openAi = OpenAiFunctions()
fileId = "file-FmkfSSf5MdhhnD8VSlzsj6Ve"
assistantId = "asst_dbNhwDpTkxLjinonDWjFIREm"
tools = [
    {
      "type": "retrieval"
    },
    {
      "type": "code_interpreter"
    }
]
thread = "thread_O65cHPNt4spP3C7y0tq6jtBx"


""" openAi.uploadRemoteFile("https://files.slack.com/files-pri/TJPALFNDB-F06748R3TB5/python_cheat_sheet_-_the_basics_coursera.pdf")
print(openAi.listFiles()) """
""" openAi.createMessage(thread,content="Que eres ?")
openAi.runAssistant(thread,assistantId) """
print(openAi.listMessages(thread))