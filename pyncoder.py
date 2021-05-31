#!/usr/bin/python3.9

##################################################################################################################
# Name          : pynCoder.py                                                                                    #
#                                                                                                                #
# Version       : 1.0.0                                                                                          #
#                                                                                                                #
# Description   : This script is a CLI encoding/decoding tool that can come in handy if you are a CTF player or  #
#                 if you just need to add some layer of obfuscation on some text/file/scripts.                   #
#                                                                                                                #
#                 It's not recommended to rely on this tool to encode any passwords or confidential document in  #
#                 **Plain Text** since it won't hash or encrypt them in anyway.                                  #
#                                                                                                                #
#                 However you could encode an already encrypted password or text, which might be more secure     #
##################################################################################################################

import base64
import binascii
import sys
import os
import time

# GLOBALS
ACTION = ''
CIPHER = ''
INPUT_PATH = ''
MODE = ''
OPTIONS = []
TUMBLING_CYCLE = 0
STOP_AUTO = False


morseDictionary = {
    "a" : ".-", "b" : "-...", "c" : "-.-.", "d" : "-..",  "e" : ".", "f" : "..-.", "g" : "--.", "h" : "....","i" : "..",
    "j" : ".---", "k" : "-.-", "l" : ".-..", "m" : "--", "n" : "-.", "o" : "---", "p" : ".--.", "q" : "--.-", "r" : ".-.", 
    "s" : "...", "t" : "-", "u" : "..-", "v" : "...-", "w" : ".--", "x" : "-..-", "y" : "-.--", "z" : "--..","1" : ".----",
    "2" : "..---", "3" : "...--","4" : "....-","5" : ".....","6" : "-....","7" : "--...","8" : "---..","9" : "----.",
    "0" : "-----", " " : "/", "!" : "-.-.--", "@" : ".--.-.", "$" : ".....", "&" : ".-...", "(" : "-.--.", ")" : "-.--.-", 
    "-" : "-....-", "_" : "..--.-", "=" : "-...-","+" : ".-.-.","/" : "-..-.",":" : "---...",";" : "-.-.-.",
    "'" : ".----.","\"": ".-..-.", "," : "--..--", "." : ".-.-.-", "?" : "..--.."
}

cipherMap = {
    "-hex": "Hex",
    "-b32": "Base-32",
    "-b64": "Base-64",
    "-r13": "Rot-13",
    "-r18": "Rot-18",
    "-r47": "Rot-47",
    "-m"  : "Morse",
    "-ch" : "Chained",
    "-done": "Done"
}

chainEncoding = [
    "-m",
    "-b64",
    "-r47"
]

fileExtensions = [
    ".txt", 
    ".c", 
    ".py", 
    ".log", 
    ".html", 
    ".css", 
    ".php", 
    ".js", 
    ".h", 
    ".cpp", 
    ".md", 
    ".hosts", 
    '.config',
    '.sh',
    '.bash',
    '.ps',
    '.bat',
    '.vbs'
]

def showHelp():
    print("""
    \n
     ACTIONs: |             Description
    ---------------------------------------------------------------------------------------
     -e       |      Encode a single string from the specified encoding
              |
     -e<N>    |      Encode a single string from the specified encoding <N> times
              |
     -E       |      Encode each line of a file from the specified encoding
              |
     -E<N>    |      Encode each line of a file from the specified encoding <N> times each
              |
     -d       |      Decode a single string from the specified encoding
              |
     -d<N>    |      Decode a single string from the specified encoding <N> times
              |
     -D       |      Decode each line of a file from the specified encoding
              |
     -D<N>    |      Decode each line of a file from the specified encoding <N> times each
    ---------------------------------------------------------------------------------------
    \n\n
     Encoding:|             Description
    ---------------------------------------------------------------------------------------
     -hex     |      Hexadecimal encoding (Hexadecimal string)
              |
     -b32     |      Base-32 encoding
              |
     -b64     |      Base-64 encoding
              |
     -r13     |      ROT-13 encoding
              |
     -r18     |      ROT-18 encoding
              |
     -r47     |      ROT-47 encoding
              |
     -m       |      Morse code encoding
              |
     -ch      |      Chained encoding/decoding: 
              |                  INPUT -> Morse -> Base32 -> Rot47 
    ---------------------------------------------------------------------------------------
    \n
    """)
    return

def showUsage():
    print("""
    \n
    For more info about the program and commands, run:\n\n       ./pynCoder.py -h\n\n
    Usage: ./pynCoder.py -[ACTIONS] (TEXT/PATH/CIPHER) -[ENCODING] -[OPTION]
           ./pynCoder.py -E /home/user/file.txt -r13
           ./pynCoder.py -e 'Hello World!' -B64
    \n
    """)
    return

def isMorse(line):
    for char in line:
        if char != " " and char != "." and char != "-" and char != "/":
            return False
    return True

def isRot13(line):

    return

def isRot18(line):

    return

def isRot47(line):
    normality_constance = 0
    max_norm_occurence = 0
    for char in line:
        if normality_constance > max_norm_occurence:
            max_norm_occurence = normality_constance
        if ord(char) >=97 and ord(char)<=122:
            normality_constance += 1
        elif ord(char) >=65 and ord(char)<=90:
            normality_constance += 1
        elif char == " ":
            normality_constance += 1
        else:
            normality_constance = 0
    if max_norm_occurence > 4:
        return False
    else:
        return True
# permitted : 97 - 102 a-f
#             65 - 70  A-f
#             48 - 57  0-9
def isHex(line):
    for char in line:
        if not (ord(char.upper()) >= 65 and ord(char.upper()) <= 70):
            if not (ord(char.upper()) >= 48 and ord(char.upper()) <= 57):
                return False
    return True

def isBase32(line):
    for char in line:
        if char == " ":
            return False
        if ord(char) <= 47:
            return False
        if ord(char) > 96:
            return False
        if ord(char) < 65 and ord(char) != 61:
            if ord(char)>= 48 and ord(char) <=57:
                continue
            else:
                return False
        if ord(char) >=91 and ord(char) < 97:
            return False
    return True

def isBase64(line):
    for char in line:
        if char == " ":
            return False
        if ord(char) <= 47:
            return False
        if ord(char) >=91 and ord(char) < 97:
            return False
    return True

def encode_decodeMorse(line):
    global ACTION

    output=''
    #Encoding part
    if ACTION == '-e' or ACTION == '-E':
        try:
            if line[list(line).index('.'): len(line)] in fileExtensions:
                print("The encoding of {0} might not be accurate.\nIf you are trying to encode a file, use the -E switch instead of -e\n"
                .format(line))
        except:
            pass
        finally:
            for char in line:
                try:
                    output += morseDictionary[char.lower()] + ' '
                except:
                    print("Can't parse : '{0}' to Morse ".format(char))
                    exit()
    #Decoding part
    else:
        splittedMorse = line.split(' ')
        for char in splittedMorse:
            dictCounter = 0
            for val in morseDictionary.values():
                if val == char:
                    break
                dictCounter += 1
            try:
                output += list(morseDictionary.keys())[dictCounter]
            except:
                print("'{0}': is not recognized as valid Morse string ".format(char))
                try:
                    if char[list(char).index('.'):len(char)] in fileExtensions:
                        print("If you are trying to decode a file, use the -D switch instead of -d\n")
                finally:
                    exit()
    return output.strip(" ")

def encode_decodeRot13(line):
    global ACTION

    output=''
    for char in line:
        uChar = char.upper()
        threshold = ord(uChar) + 13 if ACTION == "-e" or ACTION == "-E" else ord(uChar) -13
        if ord(uChar) >=65 and ord(uChar) <= 90:
            if threshold > 90 and (ACTION == "-e" or ACTION == "-E"):
                output += chr( 64 + (threshold - 90)  )
            elif threshold < 65 and (ACTION == "-d" or ACTION == "-D"):
                output += chr(91 - (65 - threshold)  )
            else:
                output += chr(threshold) 
                
        else:
            output += char
    return output

def encode_decodeRot18(line):
    global ACTION

    output=''
    for char in line:
        uChar = char.upper()
        threshold = ord(uChar) + 13 if ACTION == "-e" or ACTION == "-E" else ord(uChar) -13
        if ord(uChar) >=65 and ord(uChar) <= 90:
            if threshold > 90 and (ACTION == "-e" or ACTION == "-E"):
                output += chr( 64 + (threshold - 90)  )
            elif threshold < 65 and (ACTION == "-d" or ACTION == "-D"):
                output += chr(91 - (65 - threshold)  )
            else:
                output += chr(threshold)
        elif char.isnumeric():
            if (int(char) + 5) > 9:
                output += str(((int(char) + 5) -9) -1)
            else:
                output += str((int(char) + 5))
        else:
            output += char
    return output

def encode_decodeRot47(line):
    global ACTION

    output=''
    for char in line:
        threshold = ord(char) + 47 if ACTION == "-e" or ACTION == "-E" else ord(char) -47
        if ord(char) >=33 and ord(char) <= 126:
            if threshold > 126 and (ACTION == "-e" or ACTION == "-E"):
                output += chr( 32 + (threshold - 126)  )
            elif threshold < 33 and (ACTION == "-d" or ACTION == "-D"):
                output += chr(126 - (33- threshold) +1 )
            else:
                output += chr(threshold) 
        else:
            output += char
    return output

def encode_decodeBaseHex(line):
    global ACTION
    try:
        lineBytes = line.encode('ascii')
        if ACTION == '-e' or ACTION == '-E':
            newLineBytes = binascii.hexlify(lineBytes).upper()
        else:
            newLineBytes = binascii.unhexlify(lineBytes)
        newLine = newLineBytes.decode('ascii')
    except:
        print('Couldn\'t encode over the {0} iteration'.format(str(TUMBLING_CYCLE)), file=sys.stderr)
        return line
    return newLine

def encode_decodeBase32(line):
    global ACTION
    global TUMBLING_CYCLE

    try:
        lineBytes = line.encode('ascii')
        if ACTION == '-e' or ACTION == '-E':
            newLineBytes = base64.b32encode(lineBytes)
        else:
            newLineBytes = base64.b32decode(lineBytes)
        newLine = newLineBytes.decode('ascii')
    except:
        print('Couldn\'t encode over the {0} iteration'.format(str(TUMBLING_CYCLE)), file=sys.stderr)
        return line
    return newLine

def encode_decodeBase64(line):
    global ACTION
    global TUMBLING_CYCLE

    try:
        lineBytes = line.encode('ascii')
        if ACTION == '-e' or ACTION == '-E':
            newLineBytes = base64.b64encode(lineBytes)
        else:
            newLineBytes = base64.b64decode(lineBytes)
        newLine = newLineBytes.decode('ascii')
    except:
        print('Couldn\'t encode over the {0} iteration'.format(str(TUMBLING_CYCLE)))
        return line
    return newLine

def encode_decodeFile(filePath):
    inputFileContent = loadFile(filePath)
    outputFileContent = []
    for line in inputFileContent:
        outputFileContent.append(cycleIterator(line))

    return outputFileContent

def algorithmSelector(line):
    global ACTION
    global MODE

    if MODE == "-hex" or MODE == "-HEX":
        line = encode_decodeBaseHex(line)
    elif MODE == "-b32" or MODE == "-B32":
        line = encode_decodeBase32(line.upper())
    elif MODE == "-b64" or MODE == "-B64":
        line = encode_decodeBase64(line)
    elif MODE == "-r13" or MODE == "-R13":
        line = encode_decodeRot13(line)
    elif MODE == "-r18" or MODE == "-R18":
        line = encode_decodeRot18(line)
    elif MODE == "-r47" or MODE == "-R47":
        line = encode_decodeRot47(line)
    elif MODE == "-m" or MODE == "-M":
        line = encode_decodeMorse(line)
    elif MODE == "-ch" or MODE == "-CH":
        if ACTION == '-e' or ACTION == '-E':
            line = encode_decodeRot47(encode_decodeBase32(encode_decodeMorse(line)))
        else:
            line = encode_decodeMorse(encode_decodeBase32(encode_decodeRot47(line)))
    return line

def cycleIterator(line):
    global STOP_AUTO
    global TUMBLING_CYCLE

    origin_line = line
    for i in range (0, TUMBLING_CYCLE):
        line = algorithmSelector(line)

        newMode = cipherMap[detectEncoding(line)]
        if origin_line == line or (len(line) == len(origin_line) and newMode == "Done"):
            STOP_AUTO = True
            print('\t{0}{1} ] →  Output\t: {2}\n'.format( "\033[90m ∟"," [DONE {0}".format("\u2713"),line))
        else:
            print('{0} {1} [CYCLE {4}] →  {2}\t: {3}'.format(("\t")*1, "∟", newMode ,line, i + 1))
        time.sleep(0.5)
    return line

def detectEncoding(line):
    #TODO: Should try to Map all functions and iterate over them in a for loop instead
    if not isMorse(line):
        if not isHex(line):
            if not isBase32(line):
                if not isBase64(line):
                    if not isRot47(line):
                        return '-done'
                    #    if not isRot18(line):
                    #        if not isRot13(line):
                    #            #print ("\n pynCoder wasn't able to Auto-detect the cipher encoding\n")
                    #            return '-done'
                    #        else:
                    #            return '-r13'
                    #    else:
                    #        return '-r18'
                    else:
                        return '-r47'
                else:
                    return '-b64'
            else:
                return '-b32'
        else:
            return '-hex'
    else:
        return '-m'

def loadFile(filePath):
    with open (filePath, 'r') as inputReader:
        inputFileContent = inputReader.readlines()
        for x in range (0, len(inputFileContent) -1) :
            inputFileContent[x] = inputFileContent[x].replace("\n", "")
    return inputFileContent

def writeOutputToFile():
    return

def initArgs():
    global STOP_AUTO
    global ACTION
    global CIPHER
    global INPUT_PATH
    global MODE
    global TUMBLING_CYCLE
    global OPTIONS
    
    input_type, task, cipher_type = ("",)*3

    for x in range(1, len(sys.argv)):
        if x == 1:
            try:                
                if int((sys.argv[x])[2: len(sys.argv[x])]) > 4:
                    TUMBLING_CYCLE = 4
                    print("\n {1}Tumbling cycle as been set to {0} to increase stability".format(TUMBLING_CYCLE, "\033[133m"))
                else:
                    TUMBLING_CYCLE = int((sys.argv[x])[2: len(sys.argv[x])])
            except:
                TUMBLING_CYCLE = 1
            finally:
                ACTION = sys.argv[x][0:2]
                if ACTION == "-h" or ACTION == "-H" or ACTION =="-help":
                    showUsage()
                    showHelp()
                    exit()
                if ACTION == "-e" or ACTION == "-E":
                    task = "Encoding"
                else:
                    task = "Decoding"
        elif x == 2:
            if ACTION[1:len(ACTION)].isupper():
                INPUT_PATH = sys.argv[x]
                input_type = "File"
            else:
                CIPHER = sys.argv[x]
                input_type = "String"
        elif x == 3:
            MODE = sys.argv[x]
            try:
                cipher_type = cipherMap[MODE]
            except:
                MODE = '-A'
                cipher_type = "Auto-Detect"
        else:
            OPTIONS.append(sys.argv[x])
    if len(sys.argv) >= 3:
        print("\n** Running in {0} {1} mode with cipher type: {2} **\nTumbling cycle is set to {3} turns\n".format(input_type, task, cipher_type, TUMBLING_CYCLE))
    return

def main():
    global MODE
    global ACTION
    global CIPHER
    global TUMBLING_CYCLE

    initArgs()

    if TUMBLING_CYCLE > 0: 
        if (MODE == '-a' or MODE == '-A') and (ACTION == '-d' or ACTION == '-D'):
            print("   Trying to Auto-Detect cipher encoding...\n")
            MODE = detectEncoding(CIPHER)
            output = CIPHER
            print('{0} {1} [ORIGIN ] →  {2}\t: {3}'.format(("\t")*1, "∟", cipherMap[MODE] ,CIPHER))
            while STOP_AUTO == False:
                output = cycleIterator(output)
                MODE = detectEncoding(output)
        elif ACTION == '-E'  or ACTION == '-D' :
            print('{0} {1} [ORIGIN ] →  {2}\t: {3}'.format(("\t")*1, "∟", "File input" ,INPUT_PATH))
            output = encode_decodeFile(INPUT_PATH, TUMBLING_CYCLE, ACTION, MODE)
        elif ACTION == '-e' or ACTION == '-d':
            print('{0} {1} [ORIGIN ] →  {2}\t: {3}'.format(("\t")*1, "∟", "String input" ,CIPHER))  
            output = cycleIterator(CIPHER)
        else:
            print("\n   Error:   {0} is not a valid action.\n".format(ACTION))
            return
    else:
        showUsage()
    return

if __name__ == '__main__': 
	main()
