# Bert Chatbot

This is the first python package I made, so I use this project to attend 

## Description

Use Google Bert to implement a chatbot with Q&A pairs and 
Reading comprehension!

### Install 
* Use pip to install Bert-ChatBot
```
pip install bert-bot
```
* Download base model
* Use Google Drive to download my model [QA Model]() and [Reading Comprehension Model]()


### How to use

one command to start on your server

```
bert-chatbot --run_server/
 --qa-model_dir=$YOUR_QA_MODEL_PATH/
 --rc-model_dir=$YOUR_Reading_Comprehension_MODEL_PATH
 --cpu=false
 --gpu=true
 --num_works=1
 --ip=0.0.0.0
 --port=2333 
 ```
 
 Then you can test the server in your browser
 

### TODO
- [ ] Complete the whole project
- [ ] Docker support
- [ ] Implement training function
