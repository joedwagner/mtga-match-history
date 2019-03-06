# At heimdall.py's call, gather what needs to be known and send it to be forged by brokkr.py
import json
import pytz
from datetime import datetime
from tzlocal import get_localzone

def retrieve(path,filename):
# read in the strings
    file = open(path + '\\' + filename,'r')
            
    lines = file.readlines()
    lines = [x for x in lines if x!='\n']
    lines = [x for x in lines if x!=' \n']
    
    # find '    "messageName": "DuelScene.GameStop",\n'
    mStr = list([s for s in lines
                 if '"matchId"'.lower() in s.lower()])
    # check if list is empty
    if mStr:
        mIdx = [i for i,
                s in enumerate(lines) 
                if '"matchid"'.lower() in s.lower()]
        matchcreated = [i for i,
                        s in enumerate(lines) 
                        if 'matchcreated'.lower() in s.lower()]
    
        mList = list() 
        for i in range(0,len(mIdx)):
            bgn = [i for i, 
                   s in enumerate(reversed(lines[0:mIdx[i]])) 
                   if s == "{\n"]
            bgnIdx = mIdx[i]-bgn[0]-1
            # Check if the MatchFound outlier is here
            for m in range(0,len(matchcreated)):
                if bgnIdx<matchcreated[m]<mIdx[i]:
                    # If this entry was the match created message, find actual 
                    # beginning of the string as well as the index of the 
                    # opening bracket for later use
                    bgnIdx = matchcreated[m]
                    bracketFnd = lines[bgnIdx].find('{')
                    
                    # Find the deck info since it will appear just above this 
                    # point
                    deckbgn = [i for i, 
                               s in enumerate(reversed(lines[0:mIdx[i]]))
                               if 'decksubmit' in s.lower()]
                    deckbgnIdx = mIdx[i]-deckbgn[0]
                    deckend = [i for i,
                               s in enumerate(lines[deckbgnIdx:-1])
                               if s == "}\n"]
                    deckendIdx = deckbgnIdx + deckend[0] + 1
                    deckStr = ''.join(lines[deckbgnIdx:deckendIdx])
                    break
                else:
                    bracketFnd = 0
                                        
            end = [i for i, s in enumerate(lines[mIdx[i]:-1]) if s == "}\n"]
            endIdx = mIdx[i]+end[0]+1
            
            # Build the dict and append thelist
            matchStr = ''.join(lines[bgnIdx:endIdx])
            matchStr = matchStr[bracketFnd:-1]
            mList.append(json.loads(matchStr))
            
            # Find the time for the entry and enter it at the top level
            tStart=[]
            tEnd=[]
            idx = 0
            while not tStart or not tEnd:
                tStart = [it for it, char in enumerate(lines[bgnIdx-idx]) if char == ']']
                tEnd = [it for it, char in enumerate(lines[bgnIdx-idx]) if char == ':']
                idx += 1
            tString = lines[bgnIdx-idx+1][tStart[0]+1:tEnd[1]+6]
            timeobj = datetime.strptime(tString,'%m/%d/%Y %I:%M:%S %p')
            timeobj.astimezone(get_localzone())
            timeobjUTC = timeobj.astimezone(pytz.utc)
            mList[i]['timestamp'] = int(timeobjUTC.timestamp())
            
            # add matchid to first level if there isn't one
            if not mStr[i].strip()[1:8] in mList[i]:
                ends = [it for it, char in enumerate(mStr[i]) if char == '"']
                mList[i]['matchid'] = mStr[i][ends[-2]+1:ends[-1]]
            else:
                mList[i]['matchid'] =  mList[i].pop(mStr[i].strip()[1:8])
            
            # add deck dictionary if found
            if deckStr:
                mList[i]['deck'] = json.loads(deckStr)
                deckStr = None
                
        data = mList
                    
#        with open('rawdata.json','w') as outfile: 
#            json.dump(data,outfile)
        
        return data
    else:
        print("No match data found in file")