# Forge the knowledge from ratatoskr.py into great works to be recorded by mimir.py
def forge(dictList):
    dicts = dictList
    matchesInfo = dict()
    seatIds = dict()
    gameIdx = 0
    for i in range(0,len(dicts)):
        matchId = dicts[i]['matchid']
        
        # make an entry for the match if it does not exist
        if matchId not in matchesInfo:
            matchesInfo[matchId] = dict()
        
        # Now make a bunch of try/except statements for the desired information
        # Deck name and ID as well as match time start, opponent name, opponent 
        # rank division, and opponent rank tier 
        try:
            matchesInfo[matchId]['deckName'] = dicts[i]['deck']['CourseDeck']['name']
            matchesInfo[matchId]['deckId'] = dicts[i]['deck']['CourseDeck']['id']
            matchesInfo[matchId]['matchId'] = matchId
            matchesInfo[matchId]['opponent'] = dict([('displayName',dicts[i]['opponentScreenName']),
                       ('rank',dict([('tier',dicts[i]['opponentRankingClass']),('division',dicts[i]['opponentRankingTier'])]))])
            matchesInfo[matchId]['timestampStart'] = dicts[i]['timestamp']
        except KeyError:
            pass
        
        try:
            matchesInfo[matchId]['opponent']['playerId'] = dicts[i]['matchGameRoomStateChangedEvent']['gameRoomInfo']['gameRoomConfig']['reservedPlayers'][0]['userId']
        except KeyError:
            pass
        
        # Get the player's seat id to check who won the match
        try: 
            players = dicts[i]['matchGameRoomStateChangedEvent']['gameRoomInfo']['gameRoomConfig']['reservedPlayers']
            for p in range(0,len(players)):
                if players[p]['playerName'] != matchesInfo[matchId]['opponent']['displayName']:
                    seatIds[matchId] = dict([('seatId',players[p]['systemSeatId'])])
        except KeyError:
            pass
        
        
        # Match Result and end time
        try:
            gameRoomInfo = dicts[i]['matchGameRoomStateChangedEvent']['gameRoomInfo']
            matchesInfo[matchId]['gameType'] = gameRoomInfo['gameRoomConfig']['eventId']
            winner = gameRoomInfo['finalMatchResult']['resultList'][-1]['winningTeamId']
            reasonStr = gameRoomInfo['finalMatchResult']['matchCompletedReason']
            reasonChar = [it for it, char in enumerate(reasonStr) if char == '_']
            # reasonStr[reasonChar[0]+1:-1] clipped the last character for some reason
            matchesInfo[matchId]['matchCompletedReason'] = reasonStr[reasonChar[0]+1:len(reasonStr)]
            matchesInfo[matchId]['timestampEnd'] = dicts[i]['timestamp']
            if winner == seatIds[matchId]['seatId']:
                matchesInfo[matchId]['result'] = 'Win'
            else:
                matchesInfo[matchId]['result'] = 'Loss'
        except KeyError:
            pass
       
        # Individual game end, their results, and end-time
        try:
            obj = dicts[i]['params']['payloadObject']
            gamestate = dicts[i]['params']['messageName']
            if gamestate == 'DuelScene.GameStart':
                gameInfo = dict([('gameNumber',obj['gameNumber']),('timestampStart',dicts[i]['timestamp'])])
                try:
                    matchesInfo[matchId]['games'].append(gameInfo)
                    gameIdx += 1
                except KeyError:
                    matchesInfo[matchId]['games'] = list()
                    matchesInfo[matchId]['games'].append(gameInfo)
                    gameIdx = 0
            elif gamestate == 'DuelScene.GameStop':
                gameInfo = dict()
                reasonStr = obj['winningReason']
                reasonChar = [it for it, char in enumerate(reasonStr) if char == '_']
                # reasonStr[reasonChar[0]+1:-1] clipped the last character for some reason
                matchesInfo[matchId]['games'][gameIdx]['reason'] = reasonStr[reasonChar[0]+1:len(reasonStr)]
                if obj['seatId'] == obj['winningTeamId']:
                    matchesInfo[matchId]['games'][gameIdx]['result'] = 'Win'
                else:
                    matchesInfo[matchId]['games'][gameIdx]['result'] = 'Loss'
                matchesInfo[matchId]['games'][gameIdx]['timestampEnd'] = dicts[i]['timestamp']
        except KeyError:
            pass
    
    return matchesInfo