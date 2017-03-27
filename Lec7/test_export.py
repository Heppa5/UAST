from AQLogReader import aqLogReader
from ExportQGC import exportQGC

aqlr = aqLogReader('./021-AQL.LOG')
data = aqlr.getData()

eqgc = exportQGC(data)
eqgc.writeToFile('waypoints.txt')
