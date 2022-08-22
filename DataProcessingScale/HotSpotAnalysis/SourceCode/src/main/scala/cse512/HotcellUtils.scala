package cse512

import java.sql.Timestamp
import java.text.SimpleDateFormat
import java.util.Calendar
import scala.collection.mutable.ListBuffer

object HotcellUtils {
  val coordinateStep = 0.01

  def CalculateCoordinate(inputString: String, coordinateOffset: Int): Int =
  {
    // Configuration variable:
    // Coordinate step is the size of each cell on x and y
    var result = 0
    coordinateOffset match
    {
      case 0 => result = Math.floor((inputString.split(",")(0).replace("(","").toDouble/coordinateStep)).toInt
      case 1 => result = Math.floor(inputString.split(",")(1).replace(")","").toDouble/coordinateStep).toInt
      // We only consider the data from 2009 to 2012 inclusively, 4 years in total. Week 0 Day 0 is 2009-01-01
      case 2 => {
        val timestamp = HotcellUtils.timestampParser(inputString)
        result = HotcellUtils.dayOfMonth(timestamp) // Assume every month has 31 days
      }
    }
    return result
  }

  def timestampParser (timestampString: String): Timestamp =
  {
    val dateFormat = new SimpleDateFormat("yyyy-MM-dd hh:mm:ss")
    val parsedDate = dateFormat.parse(timestampString)
    val timeStamp = new Timestamp(parsedDate.getTime)
    return timeStamp
  }

  def dayOfYear (timestamp: Timestamp): Int =
  {
    val calendar = Calendar.getInstance
    calendar.setTimeInMillis(timestamp.getTime)
    return calendar.get(Calendar.DAY_OF_YEAR)
  }

  def dayOfMonth (timestamp: Timestamp): Int =
  {
    val calendar = Calendar.getInstance
    calendar.setTimeInMillis(timestamp.getTime)
    return calendar.get(Calendar.DAY_OF_MONTH)
  }

  // YOU NEED TO CHANGE THIS PART
  
   def calculateGScoreValue(cell: String, noOfCell: Int, hotCell: Map[String, Long], min_x: Int, max_x: Int , min_y: Int, max_y: Int, min_z: Int, max_z: Int, mean : Double, stdDev : Double): Double =
  {
    var adjCell = new ListBuffer[Long]()
    val cx :: cy :: cz :: _ = cell.split(",").toList
	
	
    for(t <- cz.toInt.-(1) to cz.toInt.+(1)) {
      for(lat <- cx.toInt.-(1) to cx.toInt.+(1)) {
        for(lon <- cy.toInt.-(1) to cy.toInt.+(1)) {
          if(lat >= min_x && lat <= max_x && lon >= min_y && lon <= max_y && t >= min_z && t <= max_z) {
            if (hotCell.contains(lat.toString +','+ lon.toString +','+ t.toString))
              adjCell += hotCell(lat.toString +','+ lon.toString +','+ t.toString)
            else
              adjCell += 0
          }
        }
      }
    }
	
    val gScoreValue = adjCell.sum.-(mean.*(adjCell.size))./(stdDev.*(scala.math.sqrt((adjCell.size).*(noOfCell).-((adjCell.size).*(adjCell.size))./(noOfCell.-(1)))))
    return gScoreValue
  }
}
