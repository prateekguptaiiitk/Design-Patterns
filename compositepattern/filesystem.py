from abc import ABC, abstractmethod
class FileSystem(ABC):
    @abstractmethod
    def ls(self):
        pass

class File(FileSystem):
    def __init__(self, name):
        self.fileName = name

    def ls(self):
        print("file name ", self.fileName)

class Directory(FileSystem):
    def __init__(self, name):
        self.directoryName = name
        self.fileSystemList = []

    def add(self, fileSystemObj):
        self.fileSystemList.append(fileSystemObj)

    def ls(self):
        print("Directory name ", self.directoryName)

        for fileSystemObj in self.fileSystemList:
            fileSystemObj.ls()

if __name__ == '__main__':
    movieDirectory = Directory("Movie")
    border = File("Border")
    movieDirectory.add(border)

    comedyMovieDirectory = Directory("ComedyMovie")
    hulchul = File("Hulchul")
    comedyMovieDirectory.add(hulchul)
    movieDirectory.add(comedyMovieDirectory)

    movieDirectory.ls()

