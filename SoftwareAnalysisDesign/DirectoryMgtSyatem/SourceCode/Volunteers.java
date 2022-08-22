
public class Volunteers extends Person{
	private int volunteerId;
	private double baseSalary;
	
	public Volunteers(String last, String first, String middle, int id,double salary) {
		super(last, first, middle);
		volunteerId = id;
		baseSalary = salary;
	}	
	
	public int getID()
	{
		return volunteerId;

	}
	

}
