import os
from urllib.request import urlopen
import requests
from io import BytesIO
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())
client = OpenAI()
client = OpenAI(
   api_key=os.getenv('OPENAI_API_KEY'),
)
class OpenAiFunctions():
    def createAssistant(self,instructions,model="gpt-3.5-turbo-1106",name="test1",tools=[],fileIds=[]):
        my_assistant = client.beta.assistants.create(
            instructions=instructions,
            name=name,
            tools=tools,
            model=model,
            file_ids=fileIds
        )
        return my_assistant
    def getAssistant(self, id):
        my_assistant = client.beta.assistants.retrieve(id)
        return my_assistant
    def deleteAssistant(self, id):
        response = client.beta.assistants.delete(id)
        print(response)
    def createThread(self):
        thread = client.beta.threads.create()
        return thread
    def deleteThread(self, threadId):
        response = client.beta.threads.delete(threadId)
        return response
    def createMessage(self,threadId,content = "How does AI work? Explain it in simple terms.",role = "user"):
        thread_message = client.beta.threads.messages.create(
        threadId,
        role=role,
        content=content,
        )
        return thread_message
    def listMessages(self, threadId):
        thread_messages = client.beta.threads.messages.list(threadId)
        return thread_messages
    def getMessage(self, messagId,threadId ):
        message = client.beta.threads.messages.retrieve(
            message_id=messagId,
            thread_id= threadId,
        )
        return message
    def compleation(self, prompt):

        response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
              
            ]
        )
        return response
    def runAssistant(self, threadId,assistantId):
        run = client.beta.threads.runs.create(
            thread_id=threadId,
            assistant_id=assistantId
        )
        return run
    def uploadFile(self, myFile, purpose="assistants"):
        file = client.files.create(
            file=open(myFile, "rb"),
            purpose=purpose
        )
        return file 
    def uploadRemoteFile(self,file,purpose="assistants"):
        response = requests.get(file)
        if response.status_code == 200:
            file_content = BytesIO(response.content)
        else:
            raise Exception("No se pudo descargar el archivo desde la URL")
        file = client.files.create(
            file=file_content,
             purpose=purpose
        )
    def deleteFile(self, myFileId):
        file = client.files.delete(myFileId)
        return file 
    def getAssistant(self, assistanId):
        my_assistant = client.beta.assistants.retrieve(assistanId)
        return my_assistant
    def modifyAssistant(self, assistantID, instrunctions = None, name = None, tools = None, model=None,fileIds=None):
        assistant = self.getAssistant(assistantID)
        assistant.instructions = instrunctions if instrunctions != None else assistant.instructions
        assistant.name = name if name != None else assistant.name
        assistant.tools = tools if tools != None else assistant.tools
        assistant.model = model if model != None else assistant.model
        assistant.file_ids = fileIds if fileIds != None else assistant.file_ids
        assistant = client.beta.assistants.update(
            assistantID,
            instructions=assistant.instructions,
            name=assistant.name,
            tools=assistant.tools,
            model=assistant.model,
            file_ids=assistant.file_ids,
        ) 
        return assistant
    def listAssistants(self):
        my_assistants = client.beta.assistants.list(
            order="desc",
            limit="20",
        )
        return my_assistants
    def listFiles(self):
        return client.files.list()
    def extractContent(self, message):
    
        message_content = message.content[0].text
        annotations = message_content.annotations
        citations = []

        for index, annotation in enumerate(annotations):

            message_content.value = message_content.value.replace(annotation.text, f' [{index}]')

 
            if (file_citation := getattr(annotation, 'file_citation', None)):
                cited_file = client.files.retrieve(file_citation.file_id)
                citations.append(f'[{index}] {file_citation.quote} from {cited_file.filename}')
            elif (file_path := getattr(annotation, 'file_path', None)):
                cited_file = client.files.retrieve(file_path.file_id)
                citations.append(f'[{index}] Click <here> to download {cited_file.filename}')
           
        message_content.value += '\n' + '\n'.join(citations)
        return message_content