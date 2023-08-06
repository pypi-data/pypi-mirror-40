#! /usr/bin/env python
# -*- coding: utf-8 -*-

#
#
# Copyright (c) 2018 Pedro Gabaldon
#
#
# Licensed under MIT License. See LICENSE
#
#

"""
main.py - Contain main Google Drive operations

Example:
    
    import main
    
    cred = main.Auth()
    drive = main.Drive(cred)

    drive.CreateFolder()
    drive.UploadSpecificFolder("example.txt")

"""

try:
    from apiclient import discovery
    from apiclient.http import MediaFileUpload
    from apiclient.http import MediaIoBaseDownload
    from apiclient.errors import HttpError

    import io
    import os
    import platform
    import httplib2

    from oauth2client import client
    from oauth2client import tools
    from oauth2client.file import Storage
except ImportError:
    raise ImportError('Please make sure you have installed the requirements.txt')


SCOPES = 'https://www.googleapis.com/auth/drive'
SECRET_FILE = os.path.dirname(__file__)
SECRET_FILE = os.path.join(SECRET_FILE, 'client_secret.json')
APP_NAME = 'Google Drive Utility'
DriveFolderMime = 'application/vnd.google-apps.folder'

if platform.system() == 'Windows':
    slash = '\\'
else:
    slash = '/'

def Auth():
    '''Return drive api object.'''
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.Drive-credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)

    credential_path = os.path.join(credential_dir, 'credential.json')
    store = Storage(credential_path)
    credentials = store.get()

    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(SECRET_FILE, SCOPES)
        flow.user_agent = APP_NAME
        flags = tools.argparser.parse_args(args=[])
        credentials = tools.run_flow(flow, store, flags)
    http = credentials.authorize(httplib2.Http())
    drive = discovery.build('drive', 'v3', http=http)

    return drive


def DeleteCred():
    '''Remove stored Oauth credentials.'''
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.Drive-credentials')
    credential_path = os.path.join(credential_dir, 'credential.json')

    if not os.path.exists(credential_path):
        print 'No OAuth token found, all ok'
        return

    store = Storage(credential_path)
    store.delete()
    print 'Access removed'
    return


class mainDrive(object):
    ''' 
    Main class holding main Google Drive operations.
    Constructor parameters:
        -drive: Drive api object
    '''
    def __init__(self, drive):
        self.drive = drive
        
        if platform.system() == "Windows":
            self.codec = 'windows-1252'    
        else:
            self.codec = 'utf-8'    
    
    def Upload(self, path, FolderId=None):
        """
        Upload method.
        Parameters:
            -path: Path of folder/file to upload
            -FolderId: If it is specified the folder/file will be uploaded to that folder
        Return:
            -True if successful
            -False if it fails
        """
        self.FILE_PATH = path
        
        if self.FILE_PATH[-1:] == slash:
            self.FILE_PATH = self.FILE_PATH.rstrip(self.FILE_PATH[-1:])

        self.FolderId = FolderId
        filename = os.path.basename(self.FILE_PATH)

        if os.path.isfile(self.FILE_PATH):

            if self.FolderId:
                metadata = {'name' : filename, 'parents' : [self.FolderId]}
                query = 'name = ' + '\'' + filename + '\' and trashed=false and mimeType != \'' + DriveFolderMime + '\' and parents in ' + '\'' + self.FolderId + '\''
            else:
                metadata = {'name' : filename}
                query = 'name = ' + '\'' + filename + '\' and trashed=false and mimeType != \'' + DriveFolderMime + '\''

            media = MediaFileUpload(self.FILE_PATH, resumable=True, chunksize=1048576)
            response = self.drive.files().list(q=query, fields='files(id, name)').execute()
            file = response.get('files')

            if file:
                metadata = {'name' : filename}
                file_id = file[0].get('id')
                request = self.drive.files().update(fileId=file_id, body=metadata, media_body=media, fields='id')
                print 'Uploading file...'
                media.stream()
                response = None
                while response is None:
                    try:
                        status, response = request.next_chunk()
                    except HttpError as err:
                        if err.resp.status == 403:
                            print 'You do not have permissions on that file'
                            return False
                        else:
                            raise
                    if status:
                        print 'File uploaded %d%%.' % int(status.progress() * 100)
                print 'File uploaded'
                return True

            else:
                request = self.drive.files().create(body=metadata, media_body=media, fields='id')
                print 'Uploading file...'
                media.stream()
                response = None
                while response is None:
                    try:
                        status, response = request.next_chunk()
                    except HttpError as err:
                        if err.resp.status == 403:
                            print 'You do not have permissions'
                            return False
                        else:
                            raise
                    if status:
                        print 'File uploaded %d%%.' % int(status.progress() * 100)
                print 'File uploaded'
                return True

        elif os.path.isdir(self.FILE_PATH):
            if self.FolderId:
                metadata = {'name' : filename, 'mimeType' : DriveFolderMime, 'parents' : [self.FolderId] }
                query = 'name = ' + '\'' + filename + '\' and trashed=false and mimeType = \'' + DriveFolderMime + '\' and parents in ' + '\'' + self.FolderId + '\''
            else:
                metadata = {'name' : filename, 'mimeType' : DriveFolderMime }
                query = 'name = ' + '\'' + filename + '\' and trashed=false and mimeType = \'' + DriveFolderMime + '\' and parents in \'root\''

            response = self.drive.files().list(q=query, fields='files(id, name)').execute()
            folder = response.get('files')
            dir_files = os.listdir(self.FILE_PATH)
            paths = []

            if self.FILE_PATH[-1:] != slash:
                self.FILE_PATH += slash

            for x in dir_files:
                paths.append(self.FILE_PATH + x)

            if folder:    
                keep_update = raw_input('Same folder found. Do you want to keep files separated or update previous? (K/U): ')
                if keep_update in ['K', 'k']:
                    keep = True
                else:
                    keep = False

            if folder and keep == False:
                folder_id = folder[0].get('id')

                for path in paths:
                    print 'Uploading folder...'
                    self.Upload(path, FolderId=folder_id)
                    
                print 'Folder uploaded'
                return True

            else:
                try:
                    response = self.drive.files().create(body=metadata, fields='id').execute()
                except HttpError as err:
                    if err.resp.status == 403:
                        print 'You do not have permissions on that folder'
                        return False
                    else:
                        raise
                folder_id = response.get('id')

                for path in paths:
                    print 'Uploading folder...'
                    self.Upload(path, FolderId=folder_id)

                print 'Folder uploaded'    
                return True
        else:
            print 'Please make sure you enter a valid path'            
            return False
        
    def UploadSpecificFolder(self, path, Id=None):
        """
        Upload to a particular folder.
        Parameters:
            -path: Path of folder/file to upload
            -Id: If it is specified it will try to upload to that folder/file
        Return:
            -True if successful
            -False if it fails
        """
        self.FILE_PATH = path

        self.Id = Id
        if not self.Id:
            print 'Select where to upload: '
            self.Id = self.List(OnlyFolder=True, SelectId=True)
        
        if self.Id:
            print 'Uploading...'

            if not self.Upload(self.FILE_PATH, FolderId=self.Id):
                print 'Error'
                return False    
            return True
        else:
            return False    
    
    def CreateFolder(self):
        """
        Creates a new folder.
        Return:
            -Id of the newly created folder
        """
        name = raw_input('Enter folder name: ')

        metadata = {'name' : name, 'mimeType' : DriveFolderMime}
        response = self.drive.files().create(body=metadata, fields='id').execute()

        print 'Folder ' + '\'' + name + '\'' + ' created with id ' + '\'' + response.get('id') + '\''

        return response.get('id')
    
    def Download(self, path=None, Id=None):
        """
        Download method.
        Parameters:
            -path: If it is specified it will try to download folder/file to that path
            -Id: If it is specified it will try to download that folder/file
        Return:
            -True if successful
            -False if it fails
        """
        self.Path = path
        if self.Path:
            if self.Path[-1:] != slash:
                self.Path += slash
            os.chdir(self.Path)
                        
        self.Id = Id
        if not Id:
            print 'Select wich folder/file download: '
            self.Id = self.List(SelectId=True)

        if self.Id:
            try:    
                mime = self.drive.files().get(fileId=self.Id, fields='mimeType, name').execute()
            except HttpError as err:
                if err.resp.status == 404:
                    print 'File not found'
                    return False
                else:
                    raise
        else:
            return False

        if mime.get('mimeType') == DriveFolderMime:
            os.makedirs(mime.get('name').encode(self.codec))
            os.chdir(mime.get('name').encode(self.codec))

            query = 'parents in ' + '\'' + self.Id + '\''
            response = self.drive.files().list(q=query, fields='files(id)', orderBy='folder desc').execute()

            files_id = response.get('files')

            for x in range(len(files_id)):
                cwd = os.getcwd()
                self.Download(Id=files_id[x].get('id'))
                os.chdir(cwd.decode(self.codec))
            print 'Folder downloaded'
            return True            

        else:
            request = self.drive.files().get_media(fileId=self.Id)
            file = io.BytesIO()
            downloader = MediaIoBaseDownload(file, request, chunksize=1048576)
            response = False

            while response is False:
                    try:
                        status, response = downloader.next_chunk()
                    except HttpError as err:
                        if err.resp.status == 403:
                            if err._get_reason() == 'Only files with binary content can be downloaded. Use Export with Google Docs files.':
                                print 'That file can not be download. View it in: ' + self.drive.files().get(fileId=self.Id, fields='webViewLink').execute().get('webViewLink')
                                return True
                            else:
                                print 'You do not have permissions'    
                                return False
                        else:
                            raise
                    if status:
                        print 'Downloaded %d%%.' % int(status.progress() * 100)
        
            with open(mime.get('name'), 'wb') as f:
                f.write(file.getvalue())

            print 'File downloaded'
            return True

    def Copy(self, Id=None):
        """
        Copy method.
        Parameters:
            -Id: If it is specified it will try to copy that folder/file
        Return:
            -True if successful
            -False if it fails
        """
        self.Id = Id
        if not Id:
            print 'Select file to copy: '
            self.Id = self.List(SelectId=True)

        if self.Id:
            try:
                response = self.drive.files().copy(fileId=self.Id, body={'name' : 'Copy of - ' + self.drive.files().get(fileId=self.Id, fields='name').execute().get('name')}).execute()
                print 'Copied'
                return True
            except HttpError as err:
                if err.resp.status == 403:
                    print 'You do not have permissions'
                    if err._get_reason() == 'This file cannot be copied by the user.':
                        print 'You cannot copy that file/folder'
                        return False
                    return False
                elif err.resp.status == 400:
                    print 'You cannot copy that file/folder'
                    return False
                else:
                    raise
        else:
            return False

    def SearchByName(self):
        """
        Search a file/folder by name.
        This method return None

        """
        name = raw_input('Enter name to search: ')
        query = 'name contains ' + '\'' + name + '\''
        self.List(query=query)
        return

    def Delete(self, Id=None):
        """
        Method to delete permanently or send to trash folders/files.
        Parameters:
            -Id: If it is specified it will try to remove that particular folder/file
        Return:
            -True if successful
            -False if it fails

        """
        self.Id = Id
        if not Id:
            print 'Select wich folder/file delete: '
            self.Id = self.List(SelectId=True)

        if self.Id:    
            trash = raw_input('Do you want to delete it permanently or send to trash? (P/T): ')

            if trash in ['T', 't']:
                metadata = {'trashed' : 'true'}
                try:
                    request = self.drive.files().update(fileId=self.Id, body=metadata, fields='id').execute()
                    print 'Deleted'
                    return True
                except HttpError as err:
                    if err.resp.status == 403:
                        print 'You are not allowed to delete it'
                        return False
                    else:
                        raise
            elif trash in ['P', 'p']:
                try:
                    request = self.drive.files().delete(fileId=self.Id).execute()
                    print 'Deleted'
                    return True
                except HttpError as err:
                    if err.resp.status == 403:
                        print 'You are not allowed to delete it'
                        return False
                    else:
                        raise
            else:
                print 'That was not an option'            
                return False
        else:
            return False        
        
    def List(self, FolderId=None, OnlyFolder=False, SelectId=False, query=None):
        """
        List folders/files method.
        Parameters:
            -FolderId: If it is specified it will try to search in that particular folder
            -OnlyFolder: It will show only folders, if specified
            -SelectId: The function will return the id of the selected folder/file. This parameters is used by other methods that need an Id and it was not specified
            -query: If it is speficied it perform that particular query
        Return:
            -Folder/file Id if SelectId=True
            -None in other cases
        """
        self.FolderId = FolderId
        if self.FolderId:
            query = 'parents in ' + '\'' + self.FolderId + '\''
        elif OnlyFolder:
            query = '(parents in \'root\' or sharedWithMe) and (mimeType = \'' + DriveFolderMime + '\')'
        elif OnlyFolder and self.FolderId:
            query = 'parents in ' + '\'' + self.FolderId + '\' and mimeType = \'' + DriveFolderMime + '\''
        elif query:
            query = query    
        else:
            query = 'parents in \'root\' or sharedWithMe'

        response = self.drive.files().list(q=query, fields='files(id, name, trashed, mimeType)').execute()
        found = response.get('files')

        if found:
            for x in range(len(found)):
                if found[x].get('trashed'):
                    continue
                try:
                    print str(x) + '. ' + found[x].get('name') + ' (%s)' %('Folder' if (found[x].get('mimeType') == DriveFolderMime) else 'File')
                except UnicodeEncodeError:
                    print str(x) + '. ' + '[Unknown name]. ID: ' + found[x].get('id')
        
            children = raw_input('Do you want to search in? (Y/N): ')

            if children in ['Y', 'y']:
                select = raw_input('Select: ')

                try:
                    select = int(select)
                    if select < len(found) and select >= 0:
                        folder_id = found[select].get('id')

                        if SelectId:
                            return self.List(FolderId=folder_id, SelectId=True)
                        else:
                            return self.List(FolderId=folder_id)
                    else:
                        print 'Enter a valid number'
                        return False

                except ValueError:
                    print 'Error'
                    print 'Enter valid number'


            elif SelectId:
                select = raw_input('Select: ')
                try:
                    select = int(select)
                    if select < len(found) and select >= 0:
                        folder_id = found[select].get('id')

                        return folder_id
                    else:
                        print 'Enter a valid number'
                        return False
                except ValueError:
                    print 'Error'
                    raise ValueError('Enter valid number')

            else:
                return

        else:
            print 'That was not a folder or folders/files were not found'
            return
            