import os
import sys
import platform
import json
import hashlib
from urllib.parse import quote
import random
import requests
import fire
import pyperclip

# config
userDir = os.environ['HOME']
configDir = userDir + '/.config/app-conf'
appConfigDir = configDir +'/baidu-trans'
configFile = appConfigDir +'/main.json'

red='\033[0;31m'
green='\033[0;32m'
yellow='\033[0;33m'
blue='\033[0;34m'
purple='\033[0;35m'
cyan='\033[0;36m'
white='\033[0;37m'
end='\033[0m'

def configureIncorrect(configFile):
    print("You can register an account on this : "+green+"http://api.fanyi.baidu.com/api/trans/product/index")
    sysstr = platform.system()
    if(sysstr =="Windows"):
        configFile = configFile.replace('/','\\')
    elif(sysstr == "Linux"):
        pass
    else:
        logError('Not support this system')

    logError("Please fill up the configuration infomation : appid & secretKey on \033[0;32m"+configFile)

def isEmpty(target):
    if target is None or target == '' or target == ' ':
        return True
    else:
        return False

def confirmDir(dirs):
    if not os.path.exists(dirs):
        os.mkdir(dirs)

# load json file add init script dir
def loadConfig():
    confirmDir(configDir)
    confirmDir(appConfigDir)

    if not os.path.exists(configFile):
        with open(configFile, 'w') as file:
            file.write('{\n    "appid"     : "",\n    "secretKey" : ""\n}')
        configureIncorrect(configFile)

    data = json.load(open(configFile))
    if isEmpty(data['appid'] ) or isEmpty(data['secretKey']):
        configureIncorrect(configFile)

    return data

def sendRequest(query=None, fromLang='zh', toLang='en', copy=False):
    # print('query:', query)
    if query is None or len(query) == 0:
        logError("Please select at least one parameter.")
        return 0
    data = loadConfig()
    appid = data['appid']
    secretKey = data['secretKey']
    myurl = '/api/trans/vip/translate'
    salt = random.randint(32768, 65536)
    sign = appid+query+str(salt)+secretKey

    temp = hashlib.md5()
    temp.update(sign.encode("utf-8"))
    sign = temp.hexdigest()

    myurl = myurl+'?appid='+appid+'&q='+quote(query)+'&from='+fromLang+'&to='+toLang+'&salt='+str(salt)+'&sign='+sign
    # print('https://fanyi-api.baidu.com'+myurl)

    result = requests.get('https://fanyi-api.baidu.com'+myurl, timeout=4)
    resultJson = json.loads(result.text)
    try:
        resultText = resultJson["trans_result"][0]["dst"]
        logInfo(resultText)
        if copy:
            # on linux, finally invoke xclip 
            pyperclip.copy(resultText)
    except :
        logError("Error: Please check main.json or baidu api")
        print(result.text)

def logError(msg):
    print("%s%s%s"%(red, msg, end))
    sys.exit(1)

def logInfo(msg):
    print("%s%s%s"%(green, msg, end))

def printParam(verb, args, comment):
    print("  %s%-5s %s%-6s %s%s"%(green, verb, yellow, args, end, comment))

def help():
    print('run: %s  %s <verb> %s <args>%s'%('python baidu.py', green, yellow, end))
    printParam("-h", "", "help")
    printParam("ze","word", "Translating Chinese into English")
    printParam("ez", "word", "Translating English into Chinese")
    logInfo("\nStatements containing special characters need to be wrapped with double quotes.")

# normalize chinese char
def normalizationData(word):
    if word is None:
        logError('Please input what you want to translation')
    word = word.replace(',', '')
    word = word.replace('(', '')
    word = word.replace(')', ',')

    return word

def translation(verb, word, copy):
    # print('word:', word)
    paramList = ['ez', 'ze']
    if verb in paramList:
        if len(word) <= 1:
            logError("Please input the sentence that needs to be translated.")
        word = normalizationData(word)
        if verb == "ez":
            # print('en:', word)
            sendRequest(word, 'en', 'zh', copy)
        if verb == "ze":
            # print('zn:', word)
            sendRequest(word, 'zh', 'en', copy)
    else:
        word = normalizationData(word)
        # print('default ze:', word)
        sendRequest(word, copy=copy)

def handleSimpleOption(verb):
    if verb is None:
        logError("Please select at least one parameter.")

    if verb == '-h':
        help()
        sys.exit(0)

    if verb == '-v':
        print('version: 0.2.2')
        sys.exit(0)

def handleParam(verb=None, *args):
    # print('input param: ', verb, args)
    handleSimpleOption(verb)
    
    copy = False
    if verb == '-c':
        if len(args) == 0:
            logError("Please select at least one parameter.")
            sys.exit(1)
        verb = args[0]
        args = args[1:]
        copy = True

    if len(args) == 0:
        word = verb
    else:
        word = str(list(args))[1:-1].replace('\'', '')
    
    translation(verb, word, copy)

def main():
    try:
        fire.Fire(handleParam)
    except requests.exceptions.ConnectionError:
        logError("Please check the network connection.")

if __name__ == '__main__':
    main()
