public class totalObjects
{

   private static int numObjects = 0;

   public totalObjects()
   {
      numObjects=0;
   }

   public void objectAdded()
   {
      numObjects++;
   }

   public int getTotalObjects()
   {
      return numObjects;
   }




}