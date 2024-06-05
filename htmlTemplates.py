css = '''
<style>
body {
    background-color: #556B2F;
}

.container {
    background-color: #263318;
    padding: 20px;
    border-radius: 10px;
}

.chat-message {
    padding: 1rem; 
   

.chat-message.user .message {
    
    border-radius: 10px;
    padding: 10px;
    color: black;
}

.chat-message.bot .message {
    
    border-radius: 10px;
    padding: 10px;
    color: black;
}

.chat-message .message {
    flex: 1;
    margin-left: 10px;
}

.text-input {
    position: fixed;
    bottom: 20px;
    width: 80%;
    margin-left: 10%;
}


</style>
'''

# # Define your HTML templates
# bot_template = '''
# <div class="chat-message bot">
#     <div class="message">BOT: {{MSG}}</div>
# </div>
# '''

# user_template = '''
# <div class="chat-message user">
#     <div class="message">USER: {{MSG}}</div>
# </div>
# '''

bot_template = '''
    BOT: {{MSG}}
'''

user_template ='''
    USER: {{MSG}}
'''