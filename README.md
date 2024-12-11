# emailChatbot
An email-based ChatBot that will respond to questions sent to the assigned email address. 

# Requirements: 
The project requires the [SimpleGmail](https://github.com/jeremyephron/simplegmail) Library, Google's [Gemini](https://ai.google.dev/gemini-api/docs/quickstart?lang=python), and the [YoutubeTranscriptAPI](https://pypi.org/project/youtube-transcript-api/). 

*(Note: for email sending, make sure to follow entire setup instructions in the SimpleGmail README file)* 

# How it Works:
The chatbot will answer any question by sending an email to the selected address. It has 3 temperature modes that can be edited to better suit your needs and a log that keeps track of all users' individual temperature modes. 

To change temperature modes, simply write the desired temperature mode in the subject line and send it to permanently change your individual temperature until you change it again.

The bot can also pull the transcript of any video on YouTube by writing: "video" in the subject line, and the YouTube link in the message body. The transcript is stored in the users' chatlogs, and you can ask the program any questions about the video (Including time stamps, and summarization).

# For Issues or Help:
Contact me for any help regarding the setup, or post an error in the issues tab if you encounter one. 

Discord: apolloactive

