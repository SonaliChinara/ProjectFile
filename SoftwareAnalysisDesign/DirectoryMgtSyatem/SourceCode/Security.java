
public class Security extends Person{
	private int securityId;
	private double baseSalary;
	
	public Security(String last, String first, String middle, int id,double salary) {
		super(last, first, middle);
		securityId = id;
		baseSalary = salary;
	}	

	public int getID()
	{
		return securityId;

	}
	
}
