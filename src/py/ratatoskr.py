# At heimdall.py's call, gather what needs to be known and send it to be forged by brokkr.py
import json
import pytz
from datetime import datetime
from tzlocal import get_localzone

def retrieve(path,filename):
    # read in the strings
    file = open(path + '\\' + filename,'r', encoding='utf-8')
                
    lines = file.readlines()
    lines = [x for x in lines if x!='\n']
    lines = [x for x in lines if x!=' \n']
    
    matchesIdx = [mii for mii,
        mis in enumerate(lines) 
        if '"matchid"'.lower() in mis.lower()]
    if matchesIdx:
        matchesList = list()
        
        for ci in range(0,len(matchesIdx)):
            for matchBeginBraceIdx, currentLine in enumerate(reversed(lines[0:matchesIdx[ci]])):
                if currentLine == "{\n":
                    openBraceIdx = matchesIdx[ci] - matchBeginBraceIdx - 1
                    bracePosition = 0
                    break
                elif "MatchCreated".lower() in currentLine.lower():
                    openBraceIdx = matchesIdx[ci] - matchBeginBraceIdx - 1
                    bracePosition = currentLine.find("{")
                    
                    for deckAppearIdx, currentDeckLine in enumerate(reversed(lines[0:openBraceIdx])):
                        if "deck".lower() in currentDeckLine.lower():
                            for searchDeckOpenBraceIdx, deckBlockLine in enumerate(reversed(lines[0:openBraceIdx-deckAppearIdx])):
                                if deckBlockLine == "{\n":
                                    deckOpenBraceIdx = openBraceIdx - deckAppearIdx - searchDeckOpenBraceIdx - 1
                                    break
                                    
                            for searchDeckCloseBraceIdx, deckBlockLine in enumerate(lines[deckOpenBraceIdx:matchesIdx[ci]]):
                                if deckBlockLine == "}\n":
                                    deckCloseBraceIdx = deckOpenBraceIdx + searchDeckCloseBraceIdx + 1
                                    break
                            
                            deckStr = ''.join(lines[deckOpenBraceIdx:deckCloseBraceIdx])
                            deckDict = json.loads(deckStr)
                            try:
                                deckDict['CourseDeck'] = json.loads(deckDict['params']['deck'])
                            except KeyError:
                                pass
                            break
                    
                    break
            
            for matchEndBraceIdx, currentLine in enumerate(lines[matchesIdx[ci]:-1]):
                if currentLine == "}\n":
                    closeBraceIdx = matchesIdx[ci] + matchEndBraceIdx + 1
                    break
            
            matchStr = ''.join(lines[openBraceIdx:closeBraceIdx])
            matchesList.append(json.loads(matchStr[bracePosition:-1]))
            
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
            matchesList[ci]['timestamp'] = int(timeobjUTC.timestamp())
        
            # add matchid to first level if there isn't one
            if not lines[matchesIdx[ci]].strip()[1:8] in matchesList[ci]:
                ends = [it for it, char in enumerate(lines[matchesIdx[ci]]) if char == '"']
                matchesList[ci]['matchid'] = lines[matchesIdx[ci]][ends[-2]+1:ends[-1]]
            else:
                matchesList[ci]['matchid'] =  matchesList[ci].pop(lines[matchesIdx[ci]].strip()[1:8])
        
            if deckDict:
                matchesList[ci]['deck'] = deckDict
                deckDict = None
                    
        data = matchesList
        return data
    else:
        print("No match data found in file")