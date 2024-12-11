from datetime import datetime
import json
from pathlib import Path
import random
import string
import time

import google.generativeai as genai
from simplegmail import Gmail
from youtube_transcript_api import YouTubeTranscriptApi

base_dir = Path.home()

API_KEY = open("api_key.txt", "r").read()
gmail = Gmail()
messages = gmail.get_unread_inbox()
genai.configure(api_key=API_KEY)

now = datetime.now() # also for message logs, may be unnecessary
randomNum = ''.join(random.choice(string.ascii_letters) for x in range(5)) # for the pin in the message logs

temp1 = open("temp1.txt", "r").read()
temp2 = open("temp2.txt", "r").read()
temp3 = open("temp3.txt", "r").read()

tempList = ["temp1", "temp2", "temp3"]

class chatbotClass():
  def __init__(self, chatPath, tempPath, temp, messageText, author):
    self.temp = temp
    self.chatPath = chatPath
    self.tempPath = tempPath
    self.author = author
    self.messageText = messageText

  def chatbot(self):
    model=genai.GenerativeModel(model_name="gemini-1.5-flash", system_instruction=self.temp)
    userPrompt = {f"User Prompt {randomNum}": f"{self.messageText} {now}"}
    author = self.author

    try:
      with open(self.chatPath, "r+") as outfile:
        file_data = json.load(outfile)
        
        responseText = model.generate_content(f"Answer the following prompt with the knowlege of the past conversations you have had here: '{file_data}' \n Prompt: '{userPrompt}'\n Just respond to the prompt, nothing else.")
        botResponse = {f"Mercury Response {randomNum}": responseText.text}
        print(responseText.text)

        login_dict = file_data["logs"][0]
        login_dict.update(userPrompt)
        login_dict.update(botResponse)
        outfile.seek(0)
        json.dump(file_data, outfile, ensure_ascii=False, indent=4)

    except Exception as e:
      open(self.chatPath, "a")
      dictionary = {"logs":[{}]}
      json_object = json.dumps(dictionary, indent=4)
      
      with open(self.chatPath, "w") as outfile:
        outfile.write(json_object)

      responseText = model.generate_content(f"Answer the following prompt: {userPrompt}")

    gmail.send_message(to=f"{author}", sender="mercury", subject="*Mercury Beta", msg_plain=f"{responseText.text}") 

class mediaClass():
  def __init__(self, path, subject, link, author):
    self.subject = subject
    self.link = link
    self.path = path
    self.author = author

  def videoCheck(self):
    model=genai.GenerativeModel(model_name="gemini-1.5-flash", system_instruction=temp2)

    if self.subject.lower() == "video":
      ytlink = model.generate_content(f"respond with only the ID of the youtube provided link, nothing else. There should be no spaces at the end or start of the ID: '{self.link}'")
      transcript_list = YouTubeTranscriptApi.list_transcripts(ytlink.text)

      transcript = transcript_list.find_transcript(['en'])
      srt = YouTubeTranscriptApi.get_transcript(ytlink.text)
      userPrompt = {f"Video Transcript {randomNum}": f"{srt}"}
      
      try:
        with open(self.path, "r+") as outfile:
          filedata = json.load(outfile)

          login_dict = filedata["logs"][0]
          login_dict.update(userPrompt)
          outfile.seek(0)
          json.dump(filedata, outfile, ensure_ascii=False, indent=4)

          responseText = model.generate_content(f"Answer the following prompt with the knowlege of the past conversations you have had here: '{filedata}' \n Prompt: '{userPrompt}'\n Just respond to the prompt, nothing else.")

      except:
        open(self.path, "a")
        dictionary = {"logs":[{userPrompt}]}
        json_object = json.dumps(dictionary, indent=4)
        
        with open(self.path, "w") as outfile:
          outfile.write(json_object)

        gmail.send_message(to=f"{self.author}", sender="mercury", subject="*Mercury Beta", msg_plain="Profile Created, please try again.")

      gmail.send_message(to=f"{self.author}", sender="mercury", subject="*Mercury Beta", msg_plain=f"{responseText.text}")  

class changeTemp():
  def __init__(self, safeListPath, subject, author):
    self.safeListPath = safeListPath
    self.subject = subject
    self.author = author

  def tempChange(self):
    if self.subject.lower() == "temp2":
      userList = {f"{self.author}": "temp2"}

    elif self.subject.lower() == "temp1":
      userList = {f"{self.author}": "temp1"}

    elif self.subject.lower() == "temp3":
      userList = {f"{self.author}": "temp3"}

    with open(self.safeListPath, "r+") as outfile:
      filedata = json.load(outfile)

      login_dict = filedata["TempList"][0]
      login_dict.update(userList)
      outfile.seek(0)
      json.dump(filedata, outfile, ensure_ascii=False, indent=4)

      gmail.send_message(to=self.author, sender="mercury", subject="*Mercury Beta", msg_plain="Mercury Temp Changed! Type 'help', in the subject line for more info!")

class checkTemp():
  def __init__(self, tempPath, author):
    self.author = author
    self.tempPath = tempPath

  def safelistcheck(self):
    with open(self.tempPath, "r") as outfile:
      filedata = json.load(outfile)

    for login_dict in filedata["TempList"]:
      for profile, level in login_dict.items():
        if self.author == profile:
          
          if level == "temp1":
            temp = temp1
            return temp
          
          elif level == "temp2":
            temp = temp2 
            return temp

          elif level == "temp3":
            temp = temp3
            return temp

def startSearch():
  for message in messages:
    chatPath = base_dir / "emailChatbot" / "chatHistory" / f"{message.sender}.json"
    tempPath = base_dir / "emailChatbot" / "TempList.json"
    
    message.mark_as_read()

    tempCheck = checkTemp(tempPath, message.sender)
    temp = tempCheck.safelistcheck()

    if temp is None:
      temp = temp2

    if message.subject in tempList:
      changetemp = changeTemp(tempPath, message.subject, message.sender)
      changetemp.tempChange()

    elif message.subject in mediaList:
      mediaclass = mediaClass(chatPath, message.subject, message.plain, message.sender)
      mediaclass.videoCheck()

    else:  
      chatclass = chatbotClass(chatPath, tempPath, temp, message.plain, message.sender)
      chatclass.chatbot()

startSearch()