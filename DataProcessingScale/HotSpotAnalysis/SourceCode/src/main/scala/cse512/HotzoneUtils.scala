package cse512

object HotzoneUtils {

  def ST_Contains(queryRectangle: String, pointString: String ): Boolean = {
    // YOU NEED TO CHANGE THIS PART
	
	if (Option(queryRectangle).getOrElse("").isEmpty || Option(pointString).getOrElse("").isEmpty)
      return false
	  
    var rect = queryRectangle.split(",")
    var x1_co = rect(0).trim.toDouble
    var y1_co = rect(1).trim.toDouble
    var x2_co = rect(2).trim.toDouble
    var y2_co = rect(3).trim.toDouble

    var point = pointString.split(",")
    var x = point(0).trim.toDouble
    var y = point(1).trim.toDouble

   if (x >= x1_co && x <= x2_co && y >= y1_co && y <= y2_co)
        return true
	else if (x >= x2_co && x <= x1_co && y >= y2_co && y <= y1_co)
		return true
	else
		return false
    
  }
}
