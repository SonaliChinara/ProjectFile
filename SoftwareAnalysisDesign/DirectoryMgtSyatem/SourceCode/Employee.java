public class Employee extends Person {
	private int empID;
	private double baseSalary;

	public Employee() {
		super();

	}

	public Employee(String last, String first, String middle, int id, double sal) {
		super(last, first, middle);
		empID = id;
		baseSalary = sal;

	}

	public int getEmpId() {
		return empID;
	}

	public void setEmpId(int empID) {
		this.empID = empID;
	}

	public double getBaseSalary() {
		return baseSalary;
	}

	public void setBaseSalary(double baseSalary) {
		this.baseSalary = baseSalary;
	}

	public int getID() {
		return empID;

	}

}
