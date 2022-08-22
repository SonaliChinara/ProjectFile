
public class Executives extends Person{
	private int executiveId;
	private double baseSalary;
	
	public Executives(String last, String first, String middle, int id, double salary) {
		super(last, first, middle);
		executiveId = id;
		baseSalary = salary;
	}	
	
	public int getID()
	{
		return executiveId;

	}

}
