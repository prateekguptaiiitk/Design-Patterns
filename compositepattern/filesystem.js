class FileSystem {
    ls() {
        throw new Error('Abstract method "ls()" must be implemented');
    }
}

class File extends FileSystem {
    constructor(fileName) {
        super()
        this.fileName = fileName
    }

    ls() {
        console.log('file name:', this.fileName)
    }
}

class Directory extends FileSystem {
    constructor(directoryName) {
        super()
        this.directoryName = directoryName
        this.fileSystemList = []
    }

    add(fileSystemObj) {
        this.fileSystemList.push(fileSystemObj)
    }

    ls() {
        console.log('Directory name:', this.directoryName)

        for (let fileSystemObj of this.fileSystemList) {
            fileSystemObj.ls()
        }
    }
}


const movieDirectory = new Directory("Movie")
const border = new File("Border")
movieDirectory.add(border)

const comedyMovieDirectory = new Directory("ComedyMovie")
const hulchul = new File("Hulchul")
comedyMovieDirectory.add(hulchul)
movieDirectory.add(comedyMovieDirectory)

movieDirectory.ls()

