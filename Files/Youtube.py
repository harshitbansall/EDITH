import requests,webbrowser,re,sqlite3,datetime,sys
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
from prettytable import PrettyTable
####################################################################################################################################
def newAccessToken(clientID,clientSecret,refreshToken):
    accessTokenData = mainDB.execute("select currentAccessToken,tokenExpiry from GoogleAPI where address = '{}'".format(mainAddress)).fetchone()
    if accessTokenData not in [("",""),(None,None)]:
        if datetime.datetime.now()<datetime.datetime.strptime(accessTokenData[1], '%Y-%m-%d %H:%M:%S'):
            return accessTokenData[0]
        else:
            mainDB.execute("update GoogleAPI set currentAccessToken = '', tokenExpiry = '' where address = '{}'".format(mainAddress))
            return newAccessToken(clientID,clientSecret,refreshToken)
    else:
        try:
            response = eval(requests.post('https://oauth2.googleapis.com/token', data={'client_id': clientID,'client_secret': clientSecret,'refresh_token': refreshToken,'grant_type': 'refresh_token'}).text)
            mainDB.execute("update GoogleAPI set currentAccessToken = '{0}', tokenExpiry = '{1}' where address = '{2}'".format(response['access_token'],(datetime.datetime.now()+datetime.timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S'),mainAddress)),mainDB.commit()
            return(response['access_token'])
        except:
            print("Requirement Of New Access Token for '{}'. Kindly Paste the Redirected Link Below.".format(mainAddress)),webbrowser.open('''https://accounts.google.com/o/oauth2/v2/auth?scope=https://www.googleapis.com/auth/youtube%20https://www.googleapis.com/auth/drive&prompt=consent&access_type=offline&include_granted_scopes=true&response_type=code&state=state_parameter_passthrough_value&redirect_uri=http://localhost&client_id={}'''.format(clientID))
            response = eval(requests.post('https://accounts.google.com/o/oauth2/token', data={'code': re.split('[=&]',input("Redirected Link: "))[3].replace("%2F","/"),'client_id': clientID,'client_secret': clientSecret,'redirect_uri': 'http://localhost','grant_type': 'authorization_code'}).text)
            mainDB.execute("update GoogleAPI set refreshToken = '{}' where address = '{}'".format(response['refresh_token'],mainAddress))
            mainDB.execute("update GoogleAPI set currentAccessToken = '{}', tokenExpiry = '{}' where address = '{}'".format(response['access_token'],(datetime.datetime.now()+datetime.timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S'),mainAddress)),mainDB.commit()
            return(response['access_token'])
####################################################################################################################################
def getUserChannelID():
    channelID = mainDB.execute("select channelID from youtubeAccounts where status = 'In Use'").fetchone()[0]
    if channelID is None or channelID == "":
        for k in getResponse('https://www.googleapis.com/youtube/v3/channels?part=snippet&mine=true')['items']:
            mainDB.execute("update youtubeAccounts set channelID = '{}' where status = 'In Use'".format(k['id'])),mainDB.commit()
            return k['id']
    else:
        return channelID
####################################################################################################################################
def getResponse(link, pageToken = ""):
    if pageToken != "":
        link = link + "&pageToken={}".format(pageToken)
    return (eval(requests.get(link, headers = {"Authorization": "Bearer " + accessToken}).text.replace("true","True").replace("false","False")))
def getVideoTitle(videoLink):
    videoID = videoLink.split("=")[1]
    for k in getResponse('https://www.googleapis.com/youtube/v3/videos?part=snippet&id={0}'.format(videoID))['items']:
        return k['snippet']['title']
####################################################################################################################################
def listPlaylistItems(playlistID, boolNextPage = False, boolPrevPage = False):
    global pageCursor,pageIndex
    link = 'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId={}&maxResults=10'.format(playlistID)
    ############################################################################
    if boolNextPage is True:
        try:
            response = getResponse(link, pageToken = pageCursor['nextPageToken'])
        except:
            raise Exception("NO NEXT PAGE EXISTS.")
    elif boolPrevPage is True:
        try:
            response = getResponse(link, pageToken = pageCursor['prevPageToken'])
        except:
            raise Exception("NO PREVIOUS PAGE EXISTS.")
    else:
        response = getResponse(link)
    ############################################################################
    totalResults = response['pageInfo']['totalResults']
    if boolNextPage is True:
        if pageIndex[1]+10 < totalResults:
            pageIndex = [pageIndex[0]+10,pageIndex[1]+10]
        else:
            pageIndex = [pageIndex[0]+10,totalResults]
    elif boolPrevPage is True:
        if pageIndex[1]-10 < totalResults:
            pageIndex = [pageIndex[0]-10,10]
        else:
            pageIndex = [pageIndex[0]-10,pageIndex[1]-10]
    else:
        pageIndex = [1,len(response['items'])]
    ############################################################################
    if "nextPageToken" in response.keys() and "prevPageToken" in response.keys():
        pageCursor = {"cursorFunc":listPlaylistItems,"funcArg":playlistID,"nextPageToken":response['nextPageToken'],"prevPageToken":response['prevPageToken']}
    elif "nextPageToken" in response.keys():
        pageCursor = {"cursorFunc":listPlaylistItems,"funcArg":playlistID,"nextPageToken":response['nextPageToken']}
    elif "prevPageToken" in response.keys():
        pageCursor = {"cursorFunc":listPlaylistItems,"funcArg":playlistID,"prevPageToken":response['prevPageToken']}
    print("Showing '{0} - {1}' of '{2}' Videos.".format(pageIndex[0],pageIndex[1],totalResults))
    x = PrettyTable()
    x.field_names = ['No.','Name', 'Type']
    for num,(videoName,videoID) in list(map(lambda x, y: (x,y), [x for x in range(pageIndex[0],pageIndex[1]+1)], [(x['snippet']['title'],x['snippet']['resourceId']['videoId']) for x in response['items']])):
        x.add_row([num,videoName,'Video'])
        exec("global item{0}\nitem{0}=('Video','{1}','{2}')".format(num,videoName.replace("'","\\'"),videoID))
    print(x)
####################################################################################################################################
def listPlaylistsofChannel(channelID, boolNextPage = False, boolPrevPage = False):
    global pageCursor,pageIndex
    if channelID == myChannelID:
        link = "https://www.googleapis.com/youtube/v3/playlists?part=snippet&maxResults=10&mine=true"
    else:
        link = "https://www.googleapis.com/youtube/v3/playlists?part=snippet&channelId={}&maxResults=10".format(channelID)
    ############################################################################
    if boolNextPage is True:
        try:
            response = getResponse(link, pageToken = pageCursor['nextPageToken'])
        except:
            raise Exception("NO NEXT PAGE EXISTS.")
    elif boolPrevPage is True:
        try:
            response = getResponse(link, pageToken = pageCursor['prevPageToken'])
        except:
            raise Exception("NO PREVIOUS PAGE EXISTS.")
    else:
        response = getResponse(link)
    ############################################################################
    totalResults = response['pageInfo']['totalResults']
    if boolNextPage is True:
        if pageIndex[1]+10 < totalResults:
            pageIndex = [pageIndex[0]+10,pageIndex[1]+10]
        else:
            pageIndex = [pageIndex[0]+10,totalResults]
    elif boolPrevPage is True:
        if pageIndex[1]-10 < totalResults:
            pageIndex = [pageIndex[0]-10,10]
        else:
            pageIndex = [pageIndex[0]-10,pageIndex[1]-10]
    else:
        pageIndex = [1,len(response['items'])]
    ############################################################################
    if "nextPageToken" in response.keys() and "prevPageToken" in response.keys():
        pageCursor = {"cursorFunc":listPlaylistsofChannel,"funcArg":channelID,"nextPageToken":response['nextPageToken'],"prevPageToken":response['prevPageToken']}
    elif "nextPageToken" in response.keys():
        pageCursor = {"cursorFunc":listPlaylistsofChannel,"funcArg":channelID,"nextPageToken":response['nextPageToken']}
    elif "prevPageToken" in response.keys():
        pageCursor = {"cursorFunc":listPlaylistsofChannel,"funcArg":channelID,"prevPageToken":response['prevPageToken']}
    print("Showing '{0} - {1}' of '{2}' Playlists.".format(pageIndex[0],pageIndex[1],totalResults))
    x = PrettyTable()
    x.field_names = ['No.','Name', 'Type']
    for num,(playlistName,playlistID) in list(map(lambda x, y: (x,y), [x for x in range(pageIndex[0],pageIndex[1]+1)], [(x['snippet']['title'],x['id']) for x in response['items']])):
        x.add_row([num,playlistName,'Playlist'])
        exec("global item{0}\nitem{0}=('Playlist','{1}','{2}')".format(num,playlistName.replace("'","\\'"),playlistID))
    print(x)
####################################################################################################################################
def listUserSubscriptions(boolNextPage = False, boolPrevPage = False):
    global pageCursor,pageIndex
    link = "https://www.googleapis.com/youtube/v3/subscriptions?part=snippet&part=contentDetails&maxResults=10&mine=true&order=alphabetical"
    if boolNextPage is True:
        try:
            response = getResponse(link, pageToken = pageCursor['nextPageToken'])
        except:
            raise Exception("NO NEXT PAGE EXISTS.")
    elif boolPrevPage is True:
        try:
            response = getResponse(link, pageToken = pageCursor['prevPageToken'])
        except:
            raise Exception("NO PREVIOUS PAGE EXISTS.")
    else:
        response = getResponse(link)
    ############################################################################
    totalResults = response['pageInfo']['totalResults']
    if boolNextPage is True:
        if pageIndex[1]+10 < totalResults:
            pageIndex = [pageIndex[0]+10,pageIndex[1]+10]
        else:
            pageIndex = [pageIndex[0]+10,totalResults]
    elif boolPrevPage is True:
        if pageIndex[1]-10 < totalResults:
            pageIndex = [pageIndex[0]-10,10]
        else:
            pageIndex = [pageIndex[0]-10,pageIndex[1]-10]
    else:
        pageIndex = [1,len(response['items'])]
    ############################################################################
    if "nextPageToken" in response.keys() and "prevPageToken" in response.keys():
        pageCursor = {"cursorFunc":listUserSubscriptions,"funcArg":"","nextPageToken":response['nextPageToken'],"prevPageToken":response['prevPageToken']}
    elif "nextPageToken" in response.keys():
        pageCursor = {"cursorFunc":listUserSubscriptions,"funcArg":"","nextPageToken":response['nextPageToken']}
    elif "prevPageToken" in response.keys():
        pageCursor = {"cursorFunc":listUserSubscriptions,"funcArg":"","prevPageToken":response['prevPageToken']}
    print("Showing '{0} - {1}' of '{2}' Channels.".format(pageIndex[0],pageIndex[1],totalResults))
    x = PrettyTable()
    x.field_names = ['No.','Name', 'Type']
    x.title = "{}'s Subscriptions"
    for num,(channelName,channelID) in list(map(lambda x, y: (x,y), [x for x in range(pageIndex[0],pageIndex[1]+1)], [(x['snippet']['title'],x['snippet']['resourceId']['channelId']) for x in response['items']])):
        x.add_row([num,channelName,'Channel'])
        exec("global item{0}\nitem{0}=('Channel','{1}','{2}')".format(num,channelName,channelID))
    print(x)
def youtubeSearch(query, searchType = "All"):
    x = PrettyTable()
    x.field_names = ['No.','Name', 'Type']
    if searchType=="All":
        response = getResponse("https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=10&q={}".format(query.replace(" ","%20")))
        for num,k in enumerate(response['items']):
            if k['id']['kind']=="youtube#channel":
                x.add_row([num+1,k['snippet']['title'].translate(non_bmp_map),'Channel'])
                exec("global item{0}\nitem{0}=('Channel','{1}','{2}')".format(num+1,k['snippet']['title'],k['id']['channelId']))
            elif k['id']['kind']=="youtube#video":
                x.add_row([num+1,k['snippet']['title'].translate(non_bmp_map),'Video'])
                exec("global item{0}\nitem{0}=('Video','{1}','{2}')".format(num+1,k['snippet']['title'],k['id']['videoId']))
        print(x)
    
####################################################################################################################################
previousProgress = 0
Mode = "NGUI"
def mainYoutube(query):
    global currentSelectedPlaylist,currentSelectedChannel,accessToken,mainAddress,mainAccount,myChannelID
    if query in ["my subscriptions",'my subs']:
        listUserSubscriptions()
    elif query in ["my playlists","mp"]:
        listPlaylistsofChannel(myChannelID)
    elif "playlists" in query:
        currentSelectedChannel = eval("item{}".format(query.split("playlists ")[1]))
        listPlaylistsofChannel(currentSelectedChannel[2])
    elif "list " in query:
        currentSelectedPlaylist = eval("item{}".format(query.split("list ")[1]))
        listPlaylistItems(currentSelectedPlaylist[2])
    elif "info " in query:
        try:
            infoItem = eval("item{}".format(query.split("info ")[1]))
            if infoItem[0] == "Video":
                for k in getResponse('https://www.googleapis.com/youtube/v3/videos?part=snippet&part=statistics&id={0}'.format(eval("item{}".format(query.split("info ")[1]))[2]))['items']:
                    print("Title: {0}\nVideo ID: {1}\nThumbnail URL: {2}\nViews: {3}\nLikes: {4}\nDislikes: {5}\nComments: {6}".format(k['snippet']['title'],k['id'],k['snippet']['thumbnails']['high']['url'],k['statistics']['viewCount'],k['statistics']['likeCount'],k['statistics']['dislikeCount'],k['statistics']['commentCount']))
            elif infoItem[0] == "Playlist":
                return 0
            elif infoItem[0] == "Channel":
                for k in getResponse('https://www.googleapis.com/youtube/v3/channels?part=snippet&part=statistics&id={}'.format(eval("item{}".format(query.split("info ")[1]))[2]))['items']:
                    print("Title: {0}\nChannel ID: {1}\nDescription: {2}\nThumbnail URL: {3}\nVideos: {4}\nSubscribers: {5}\nViews: {6}".format(k['snippet']['title'],k['id'],k['snippet']['description'],k['snippet']['thumbnails']['high']['url'],k['statistics']['videoCount'],k['statistics']['subscriberCount'],k['statistics']['viewCount']))
        except:
            raise Exception ("No Video/Playlist/Channel Named '{}'".format(query.split("info ")[1].title()))
##print("Title: {0}\nChannel ID: {1}\nDescription: {2}\nThumbnail URL: {3}\nVideos: {4}\nSubscribers: {5}\nViews: {6}".format(k['snippet']['title'],k['id'],k['snippet']['description'],k['snippet']['thumbnails']['high']['url'],k['statistics']['videoCount'],k['statistics']['subscriberCount'],k['statistics']['viewCount']))
    elif "play " in query:
        playItem = eval("item{}".format(query.split("play ")[1]))
        if playItem[0]=='Video':
            return("Playing '{}'.".format(playItem[1])),webbrowser.open("https://www.youtube.com/watch?v={}".format(playItem[2]))
        else:
            return("'{}' is not a Valid Video.".format(playItem[1]))
    elif "download " in query:
        if "www" in query.split("download ")[1]:
            link = query.split("download ")[1]
            videoName = getVideoTitle(link)
        elif query.split("download ")[1].isdigit():
            videoTuple = eval("item{}".format(query.split("download ")[1]))
            link = "https://www.youtube.com/watch?v={}".format(videoTuple[2])
            videoName = videoTuple[1]
        else:
            link = "https://www.youtube.com/watch?v={}".format(query.split("download ")[1])
            videoName = getVideoTitle(link)
        from pytube import YouTube


        def on_progress(stream, chunk, bytes_remaining):
            global previousProgress
            totalSize = stream.filesize
            liveProgress = int((stream.filesize - bytes_remaining) / totalSize * 100)
            if liveProgress > previousProgress:
                previousProgress = liveProgress
                if Mode == "NGUI":
                    print(str(liveProgress) + "%", end = " ")
                else:
                    print(liveProgress,end = " ")



        def downloadVideo(videoLink):
            videoStream = YouTube(videoLink)
            videoStream.register_on_progress_callback(on_progress)
            videoTitle = videoStream.title
            print("Now downloading,  " + str(videoTitle))
            mainVideo = videoStream.streams.filter(progressive=True).last()
            print('File Size : ' + str(round(mainVideo.filesize/(1024*1024))) + 'MB')
            print("Downloaded: ", end = "")
            mainVideo.download()
            print("\nDownload Complete, " + str(videoTitle))

        downloadVideo(link)



    
    elif "streams " in query:

        videoTuple = eval("item{}".format(query.split("streams ")[1]))
        link = "https://www.youtube.com/watch?v={}".format(videoTuple[2])
        videoName = videoTuple[1]
        import pytube
        yt = pytube.YouTube(link).streams
        for videoStream in yt:
##            if videoStream.includes_audio_track:
            print(videoStream)
##                videoStream.download(output_path="C:/Users/Tania/Desktop")
##                break
    elif query in ["next page","np"]:
        if pageCursor['funcArg']!="":
            pageCursor['cursorFunc'](pageCursor['funcArg'],boolNextPage = True)
        else:
            pageCursor['cursorFunc'](boolNextPage = True)
    elif query in ["prev page","pp","previous page"]:
        if pageCursor['funcArg']!="":
            pageCursor['cursorFunc'](pageCursor['funcArg'],boolPrevPage = True)
        else:
            pageCursor['cursorFunc'](boolPrevPage = True)
    elif query=="info account":
        return 0
    elif query in ["youtube login",'yl']:
        global AnonymousDriveLogin
        AnonymousDriveLogin = True
        accessToken = input("Temporary Access Token: ")
    elif "search" in query:
        youtubeSearch(query.split("search ")[1])
    elif query=="change youtube account":
        for k in mainDB.execute("select sNum,address from youtubeAccounts order by sNum").fetchall():print("{}: {}".format(k[0],k[1]))
        mainAddress = mainDB.execute("select sNum,address from youtubeAccounts order by sNum").fetchall()[int(input("Which Address Should I Use?: "))-1][1]
        mainAccount = mainDB.execute("select * from GoogleAPI where address = '{}'".format(mainAddress)).fetchone()
        mainDB.execute("UPDATE youtubeAccounts SET status = '' where status = 'In Use'"),mainDB.execute("UPDATE youtubeAccounts SET status = 'In Use' where address = '{}'".format(mainAddress)),mainDB.commit()
        accessToken = newAccessToken(mainAccount[2],mainAccount[3],mainAccount[4])
        myChannelID = getUserChannelID()
        return("Account Changed.")

####################################################################################################################################        
if __name__=="__main__":
    mainDB = sqlite3.connect("C:/Users/Tania/Desktop/Harshit/EDITH/Data/mainDB.db")
    mainAddress = mainDB.execute("select address from youtubeAccounts where status = 'In Use'").fetchone()[0]
    mainAccount = mainDB.execute("select * from GoogleAPI where address = '{}'".format(mainAddress)).fetchone()
    accessToken = newAccessToken(mainAccount[2],mainAccount[3],mainAccount[4])
    myChannelID = getUserChannelID()
    while True:
        try:
            finalQuery = mainYoutube(input("Say Something: "))
            if finalQuery is not None:print(finalQuery)
        except Exception as e:print(str(e).title())
else:
    mainDB = sqlite3.connect("C:/Users/Tania/Desktop/Harshit/EDITH/Data/mainDB.db")
    mainAddress = mainDB.execute("select address from youtubeAccounts where status = 'In Use'").fetchone()[0]
    mainAccount = mainDB.execute("select * from GoogleAPI where address = '{}'".format(mainAddress)).fetchone()
    accessToken = newAccessToken(mainAccount[2],mainAccount[3],mainAccount[4])
    myChannelID = getUserChannelID()
##    mainYoutubeExplorer(input("Say Something: "))
