from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

#this function gets our google drive info/credentials so we can use it
#allows us to return the "drive" so we can upload/download stuff as needed
def client_auth():
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile("user.txt") #try to load credentials for gdrive

    if gauth.credentials is None:
        #we need to get them if they arent able to be loaded
        gauth.LocalWebserverAuth() # Creates local webserver and auto handles authentication.
    elif gauth.access_token_expired:
        gauth.Refresh()
        #refresh the creds if necessary
    else:
        gauth.Authorize()
        #using saved credentials and moving on
    gauth.SaveCredentialsFile("user.txt")
    #this saves our credentials so we dont pop the webpage every opening

    drive = GoogleDrive(gauth)

    return drive #return usable list file

#function to create our folder, to have stability within a users gdrives
def create_folder():
    drive = client_auth()
    folder_metadata = {'title' : 'CalData', 'mimeType' : 'application/vnd.google-apps.folder'}
    folder = drive.CreateFile(folder_metadata)
    folder.Upload()

#creates our .json file for our task data
def create_db():
    drive = client_auth()
    data = drive.CreateFile({'title': 'task_db.json'})
    data.Upload()
    return data['id'] # this is how you access file id
    
def find_db(file_id): # this function finds if the file exists by search via ID
    drive = client_auth()
    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()

    status = False

    for file1 in file_list:
        print('title: %s, id: %s' % (file1['title'], file1['id']))
        if file1['id'] ==file_id:
            status = True
    
    return status
    
    #need to find our db file by its gdrive ID

#function creates a file within the folder specified by that hardcoded id
#change this to be dynamic later
def db_to_folder():
    drive = client_auth()
    file1 = drive.CreateFile({'title':'dummy.json', 'mimeType':'text/csv',
        "parents": [{"kind": "drive#fileLink","id": "1tbNBs1ZdWNOUB1lqWaryQABNyBDFNc-F"}]})
    file1.Upload()

def test_file_update():
    drive = client_auth()
    file1 = drive.CreateFile({'mimeType':'text/csv',
        "parents": [{"kind": "drive#fileLink","id": "1w_ttNr9D8mGw2JWJAxRR_OdMo2DmlIER"}]})    
    file1['title'] = 'newtitlebro.json'
    file1.Upload()

def ListFolder(parent):
    drive = client_auth()
    filelist=[]
    file_list = drive.ListFile({'q': "'%s' in parents and trashed=false" % parent}).GetList()
    for f in file_list:
        if f['mimeType']=='application/vnd.google-apps.folder': # if folder
            filelist.append({"id":f['id'],"title":f['title'],"list":ListFolder(f['id'])})
        else:
            filelist.append({"id":f['id'],"title":f['title'],"title1":f['alternateLink']})
    return filelist


def main():
    #db_file = create_db()
    #create_folder()
    #status = find_db("1PHn3tgxZT4NsR72PeptJiQ8ybiyQJRLb") #pass in the id string of the file to search for it
    #print(db_file)
    #print(status)
    #db_to_folder()
    #test_file_update()

    #getting all the file id's within the the directory we specifify to search
    test_list =ListFolder("1tbNBs1ZdWNOUB1lqWaryQABNyBDFNc-F")
    for lists in test_list:
        print(lists["id"])

if __name__ == '__main__':
    main()