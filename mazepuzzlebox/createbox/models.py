from django.db import models
import json
import simplejson as json
from django.conf import settings

#TODO

startX = 2
startY = 4
endX = 15
endY = 5
noGoStartX = 4
noGoStartY = 2
noGoEndX = 9
noGoEndY = 6

class Callable:
    def __init__(self, anycallable):
        self.__call__ = anycallable

# Create your models here.
class Box(models.Model):
    pub_date = models.DateTimeField('date published')
    maze = models.CharField(max_length=400)
    version = models.IntegerField('version')


    def getDimensions(self):
        if self.version == 1:
            return(13,6)
        if self.version == 2:
            return(16,6)


    #we want the maze in columns of rows not rows of columns
    def htmlMaze(self):
        (xCells,yCells) = self.getDimensions()        
        maze = json.loads( self.maze )
        #initalize new array
        outmaze = [[ 0 for x in range(xCells)]for y in range(yCells)]
        for x in range(xCells):
            for y in range(yCells):
                if x > noGoStartX and x < noGoEndX and y > noGoStartY and y < noGoEndY:
                    outmaze[y][x] = 'no-go'
                if maze[x][y]:
                    outmaze[y][x] = 'gone'
                if x == startX and y == startY:
                    outmaze[y][x] = 'start'
                if x == endX and y == endY:
                    outmaze[y][x] = 'end'
                
        return outmaze

    def checkJSON(jstr):
        version=settings.DXFVERSION
        #TODO repeated code
        if version == 1:
            (xCells,yCells)=(13,6)
        if version == 2:
            (xCells,yCells)=(16,6)
        try:
            maze = json.loads( jstr )
        except:
            raise Exception( "bad json string" )
        try:
            if len( maze ) != xCells:
                raise Exception( "wrong number of columns in json array" )
            for i in range( xCells ):
                if len( maze[i] ) != yCells:
                    raise Exception( "wrong number of rows in json array" )
        except:
            raise Exception( "json doesn't represent an array" )


    checkJSON = Callable(checkJSON)

