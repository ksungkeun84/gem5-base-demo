import os
import sys
import urllib
from uuid import UUID
from pathlib import Path
from typing import Union, List
from gem5art.artifact import Artifact
import gem5art.artifact

class MyArtifact:
    def __init__(self, command:str, name:str, type:str, path: Union[str, Path], cwd:str, documentation:str, inputs:List['Artifact'] = []):
        self.command = command
        self.name = name
        self.type = type
        self.path = path
        self.cwd = cwd
        self.inputs = inputs
        self.documentation = documentation
        self.db = gem5art.artifact.getDBConnection()

    def getArtifact(self):
        artifacts = gem5art.artifact.getByName(self.db, self.name)
        for artifact in artifacts:
            if artifact.name == self.name and \
               artifact.type == self.type and \
               artifact.path == Path(self.path) and \
               artifact.cwd == Path(self.cwd) and \
               artifact.documentation == self.documentation:
                   if artifact.type == 'binary' or artifact.type == 'disk image' or artifact.type == 'gem5 binary' or artifact.type == 'kernel':
                       if not os.path.exists(artifact.path):
                           print("Found artifact")
                           print(artifact)
                           print("Downloaing to %s ..." % (artifact.path))
                           subdirs = os.path.dirname(artifact.path)
                           if not os.path.exists(subdirs):
                               subdirs = os.makedirs(subdirs)
                           self.db.downloadFile(artifact._id, artifact.path)
                           return artifact

        return Artifact.registerArtifact(
                command = self.command,
                typ = self.type,
                name = self.name,
                path = self.path,
                cwd = self.cwd,
                inputs = self.inputs,
                documentation = self.documentation)
