import os

from boxsdk import Client
from boxsdk import OAuth2

class FileReader:
    """
    FilesReader :- A helpful client to capture file related information
    and to access the file's content.
    This module refers to the box skill kit nodejs and the Box Python SDK.
    https://github.com/box/box-skills-kit-nodejs
    https://github.com/box/box-python-sdk/blob/master/docs/usage/files.md#get-a-files-information
    
    API:-FileReader.file : boxsdk.File
    FilesReader.download_to(writeable_stream, file_version, byte_range) : 
    FilesReader.get_download_url () : str
    FilesReader.get_embed_url () : str
    FilesReader.get_representation_info (rep_hints) : list of dict
    """
    BOX_API_ENDPOINT = 'https://api.box.com/2.0'

    BOXSDK_CLIENT_ID = 'BoxSkillsClientId'
    BOXSDK_CLIENT_SECRET = 'BoxSkillsClientSecret'

    def __init__(self, json_event_body):
        self.request_id = json_event_body['id']
        self.skill_id = json_event_body['skill']['id']
        self.file_id = json_event_body['source']['id']
        self.file_name = json_event_body['source']['name']
        self.file_size = json_event_body['source']['size']
        self.file_format = self.__get_file_format(self.file_name)
        self.file_type = self.__get_file_type(self.file_format)
        self.file_read_token = json_event_body['token']['read']['access_token']
        self.file_write_token = json_event_body['token']['write']['access_token']
        self.file_read_client = Client(OAuth2(
            self.BOXSDK_CLIENT_ID,
            self.BOXSDK_CLIENT_SECRET,
            access_token=self.file_read_token))
        self.file = self.file_read_client.file(self.file_id)

    FileType = {
        'AUDIO': { 'name': 'AUDIO', 'representationType': '[mp3]' },
        'VIDEO': { 'name': 'VIDEO', 'representationType': '[mp4]' },
        'IMAGE': { 'name': 'IMAGE', 'representationType': '[jpg?dimensions=1024x1024]' },
        'DOCUMENT': { 'name': 'DOCUMENT', 'representationType': '[extracted_text]' }
    }

    boxVideoFormats = (
        '3g2', '3gp', 'avi', 'flv', 'm2v', 'm2ts', 'm4v', 'mkv',
        'mov', 'mp4', 'mpeg', 'mpg', 'ogg', 'mts', 'qt', 'ts', 'wmv'
    )

    boxAudioFormats = (
        'aac', 'aif', 'aifc', 'aiff', 'amr', 'au', 'flac', 'm4a', 'mp3',
        'ra', 'wav', 'wma'
    )

    boxImageFormats = (
        'ai', 'bmp', 'gif', 'eps', 'heic', 'jpeg', 'jpg', 'png', 'ps',
        'psd', 'svg', 'tif', 'tiff', 'dcm', 'dicm', 'dicom', 'svs', 'tga'
    )

    def __get_file_format(self, file_name):
        file_extension = os.path.splitext(file_name.lower())[1].replace('.', '')
        return file_extension
 
    def __get_file_type(self, file_format):
        if file_format in self.boxAudioFormats:
            return self.FileType['AUDIO']['name']
        elif file_format in self.boxImageFormats:
            return self.FileType['IMAGE']['name']
        elif file_format in self.boxVideoFormats:
            return self.FileType['VIDEO']['name']
        return self.FileType['DOCUMENT']['name']

    def content(self, file_version=None, byte_range=None):
        """Download the file; write it to the given stream.
        
        Keyword Arguments:
            file_version {FileVersion} -- optionally download a specific version of the file (default: {None})
            byte_range {(`int`, `int`)} -- A tuple of inclusive byte offsets to download, e.g. (100, 199) to download the second 100 bytes of a file (default: {None})
        
        Returns:
            bytes -- File content as bytes.
        """
        return self.file.content(file_version, byte_range)

    def download_to(self, writeable_stream, file_version=None, byte_range=None):
        """Download the file; write it to the given stream.
        
        Arguments:
            writeable_stream {file} -- A file-like object where bytes can be written into.
        
        Keyword Arguments:
            file_version {FileVersion} -- The specific version of the file to retrieve the contents of. (default: {None})
            byte_range {(`int`, `int`)} -- A tuple of inclusive byte offsets to download, e.g. (100, 199) to download the second 100 bytes of a file (default: {None})        
        """
        return self.file.download_to(
            writeable_stream, file_version, byte_range)

    def get_download_url(self):
        """Get Download URL
        
        Returns:
            str -- Download url of file.
        """
        return self.file.get_download_url()

    def get_embed_url(self):
        """Get an Embed Link
        
        Returns:
            str -- Embed link of file.
        """
        return self.file.get_embed_url()

    def get_representation_info(self, rep_hints=None):
        """ Get information about the representations available for a file.
        
        Keyword Arguments:
            rep_hints {`unicode` or None} -- A formatted string describing which representations are desired. (default: {None})
        
        Returns:
            `list` of `dict` -- The representation information
        """
        return self.file.get_representation_info(rep_hints)
   
