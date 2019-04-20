# At heimdall.py's call, gather what needs to be known and send it to be forged by brokkr.py
import json
import pytz
from datetime import datetime
from tzlocal import get_localzone
import time

def retrieve(path,filename):
    # read in the strings
    file = open(path + '\\' + filename,'r', encoding='utf-8')
            
    lines = file.readlines()
    lines = [x for x in lines if x!='\n']
    lines = [x for x in lines if x!=' \n']
    
    matchesStr = list([string for string in lines
                 if '"matchId"'.lower() in string.lower()])
    
    matchesIdx = [mii for mii,
        mis in enumerate(lines) 
        if '"matchid"'.lower() in mis.lower()]
    
    # Parse lines if matches are found
    if matchesIdx:
        matchcreatedIdx = [mci for mci,
                        mcs in enumerate(lines) 
                        if 'matchcreated'.lower() in mcs.lower()]
    
        matchesList = list() 
        for i in range(0,len(matchesIdx)):
           
            for matchBeginBraceIdx, currentLine in enumerate(reversed(lines[0:matchesIdx[i]])):
                if currentLine == "{\n":
                    openBraceIdx = matchesIdx[i] - matchBeginBraceIdx - 1
                    break
            
            # Check if the MatchFound outlier is here
            for m in range(0,len(matchcreatedIdx)):
                if openBraceIdx<matchcreatedIdx[m]<matchesIdx[i]:
                    # If this entry was the match created message, find actual 
                    # beginning of the string as well as the index of the 
                    # opening bracket for later use
                    openBraceIdx = matchcreatedIdx[m]
                    matchFound = lines[openBraceIdx].find('{')
                    
                    for deckBeginBraceIdx, currentLine in enumerate(reversed(lines[0:matchesIdx[i]])):
                        if currentLine == "{\n":
                            deckBeginIdx = matchesIdx[i] - deckBeginBraceIdx - 1
                            break
                   
                    for deckEndBraceIdx, currentLine in enumerate(lines[deckBeginIdx:-1]):
                        if currentLine == "}\n":
                            deckEndIdx = deckBeginIdx + deckEndBraceIdx + 1
                            break
                    
                    deckStr = ''.join(lines[deckBeginIdx:deckEndIdx])
                    break
                else:
                    matchFound = 0
            
            for matchEndBraceIdx, currentLine in enumerate(lines[matchesIdx[i]:-1]):
                if currentLine == "}\n":
                    closeBraceIdx = matchesIdx[i]+matchEndBraceIdx+1
                    break
            
            # Build the dict and append the list
            matchStr = ''.join(lines[openBraceIdx:closeBraceIdx])
            matchStr = matchStr[matchFound:-1]
            matchesList.append(json.loads(matchStr))
            
            # Find the time for the entry and enter it at the top level
            tStart=[]
            tEnd=[]
            idx = 0
            while not tStart or not tEnd:
                tStart = [it for it, char in enumerate(lines[openBraceIdx-idx]) if char == ']']
                tEnd = [it for it, char in enumerate(lines[openBraceIdx-idx]) if char == ':']
                idx += 1
            tString = lines[openBraceIdx-idx+1][tStart[0]+1:tEnd[1]+6]
            timeobj = datetime.strptime(tString,'%m/%d/%Y %I:%M:%S %p')
            timeobj.astimezone(get_localzone())
            timeobjUTC = timeobj.astimezone(pytz.utc)
            matchesList[i]['timestamp'] = int(timeobjUTC.timestamp())
            
            # add matchid to first level if there isn't one
            if not matchesStr[i].strip()[1:8] in matchesList[i]:
                ends = [it for it, char in enumerate(matchesStr[i]) if char == '"']
                matchesList[i]['matchid'] = matchesStr[i][ends[-2]+1:ends[-1]]
            else:
                matchesList[i]['matchid'] =  matchesList[i].pop(matchesStr[i].strip()[1:8])
            
            # add deck dictionary if found
            if deckStr:
                matchesList[i]['deck'] = json.loads(deckStr)
                deckStr = None
                
        data = matchesList
        return data
    else:
        print("No match data found in file")