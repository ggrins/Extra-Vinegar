#!/usr/bin/python

import string, math, re, argparse

def textSplit(cipherText, size):
    split = [cipherText[i:i + size] for i in range(0, len(cipherText), size)]
    return split

def compare(first, second):
    global ff
    count = 0
    for x in first:
        for y in second:
            ff += 1
            if x == y:
                count += 1	
    return count

def setRows(clist):
    rows, temp = [],[]
    for x in range(len(clist[0])+1):
        rows.append(temp)
        temp = []
        for z in clist:
            try:
                temp.append(z[x])
            except IndexError:
                pass
    rows.pop(0)

    for i in range(len(rows)):
        rows[i] = ''.join(rows[i])
    return rows

def caesarCrack(c):
    outputs = []
    t = ''
    for i in range(27):
        outputs.append(t)
        t = ''
        for l in c.lower():
            if (ord(l)-i) < 97:
                t += chr((ord(l)-i) + 26)
            else:
                t += chr(ord(l)-i)
    outputs.pop(0)
    return outputs

def mostCommon(l):
    return max(set(l), key=l.count)

def correlation(list1, list2): 
    cor = []
    for x in range(len(list1)):
       cor.append(list1[x] * list2[x])
    return sum(cor)

def decodeCipher(cipher, cipherCopy, key):
    key = key * ((len(cipher) / len(key)) + 5)
    decoded = []
    for x in range(len(cipher)):
        numDiff = ord(key[x]) - 65
        t = ord(cipher[x])
        t = t - numDiff
        if t < 65:
            t += 26
        t = chr(t)
        decoded.append(t)
    for x in range(len(cipherCopy)):
        if re.match('[^A-Za-z0-9]+', cipherCopy[x]) is not None:
            decoded.insert(x, cipherCopy[x])
    for x in range(len(cipherCopy)):
        if cipherCopy[x].islower():
            decoded[x] = decoded[x].lower()
    return ''.join(decoded)

def calculateKeySize(cipherText):
    global ff
    deltaList, keySizeList = [],[]
    print "+---------------+---------------+--------------------+"    
    print "|      Size     |     Count     |   Delta-bar I.C.   |"
    print "+---------------+---------------+--------------------+"
    for z in range(1, inputTestSize+1):
        fivelist = textSplit(cipherText, z)
        rows = setRows(fivelist)
        count = 0
        for x in range(len(rows)):
            for y in range(len(rows[x])):
                count += compare(rows[x][y], rows[x][y+1:len(rows[x])])
        final = count / (ff/float(26))
        deltaList.append(float(round(final, 3)))
        keySizeList.append(str(z)) 
        print "|\t" + str(z)  + "\t|\t"  + str(count) + "\t|\t" + str(round(final, 3)) + "\t     |"
        ff = 0
    print "+---------------+---------------+--------------------+"
    englishIC = 1.73
    keyLengthValue = min(deltaList, key=lambda x:abs(x-englishIC))
    print "Closest Delta Value to %s -> %s" % (str(englishIC), str(keyLengthValue))
    index = deltaList.index(keyLengthValue)
    keySize = keySizeList[index]
    print "Most Likely Key Size -> %s" % str(keySize)
    if inputKeySize:
        print 'Overriden Key Size -> %s' % inputKeySize
        return inputKeySize
    else:
        return int(keySize)

def calculateKey(cipherText, englishFrequency, keySize):
    csize = textSplit(cipherText, keySize)
    rows = setRows(csize)
    freqCounter = 0
    temp, temp2, frequency = [],[],[]

    for z in rows:
        caesarList = caesarCrack(z)
        for y in range(len(caesarList)):
            for x in range(len(string.ascii_lowercase)):
                for w in range(len(caesarList[y])):
                    if (string.ascii_lowercase[x] == caesarList[y][w].lower()):
                        freqCounter += 1
                temp.append(((freqCounter/float(len(caesarList[y]))) * 100)) 
                freqCounter = 0
            temp2.append(temp)
            temp = []
        frequency.append(temp2)
        temp2 = []

    temp, c = [],[]
    for z in range(len(frequency)):
        for y in range(len(frequency[z])):
            e = correlation(frequency[z][y], englishFrequency)
            temp.append(e)
        maxnum = max(temp)
        char = chr(temp.index(maxnum) + 65)
        c.append(char)
        temp = []
    key = ''.join(c)
    return key

def readFile(cipherFile):
    f = open(cipherFile,'r')
    cipherText = f.read()
    cipherText = cipherText.strip('\n')
    f.close()
    return cipherText

def writeFile(outputFile, plaintext):
    f = open(outputFile, 'w')
    f.write(plaintext)
    f.write('\n')
    f.close()

def readArgs(args):
    global inputKeySize
    global inputTestSize
    global outputFile
    if args.keysize:
        inputKeySize = args.keysize[0]
    else:
        inputKeySize = ''
    if args.size:
        inputTestSize = args.size[0]
    else:
        inputTestSize = 10
    if args.output:
        outputFile = args.output[0]
    else:
        outputFile = ''

def main():
    description = 'Extra Vinegar decrypts Vigenere ciphers with statistical analysis.'
    p = argparse.ArgumentParser(description=description)
    p.add_argument('input', metavar='InputFile', type=str, nargs=1, help='Input file location containing ciphertext')
    p.add_argument('-o', '--output', type=str, nargs=1, help='Output file location for plaintext')
    p.add_argument('-s', '--size', type=int, nargs=1, help='Allows the maximum tested key size to be overridden (default 10)')
    p.add_argument('-k', '--keysize', type=int, nargs=1, help='Allows the calculated key size to be overridden')
    args = p.parse_args()
    readArgs(args)

    cipherText = readFile(args.input[0])
    print "Ciphertext -> %s\n" % cipherText
    
    copyCipherText = cipherText
    cipherText = re.sub('[^A-Za-z0-9]+', '', cipherText)
    cipherText = cipherText.upper()
    englishFrequency = [8.167,1.492,2.782,4.253,12.702,2.228,2.015,6.094,6.966,0.153,0.772,4.025,2.406,6.749,7.507,1.929,0.095,5.987,6.327,9.056,2.758,0.978,2.360,0.150,1.974,0.074]

    global ff
    ff = 0

    keySize = calculateKeySize(cipherText)
    print '\nKey -> %s' % calculateKey(cipherText, englishFrequency, keySize)
    print '\nPlaintext -> %s' % decodeCipher(cipherText, copyCipherText, calculateKey(cipherText, englishFrequency, keySize))
    if outputFile:
        writeFile(outputFile, decodeCipher(cipherText, copyCipherText, calculateKey(cipherText, englishFrequency, keySize)))
    
if __name__ == "__main__":
    main()
