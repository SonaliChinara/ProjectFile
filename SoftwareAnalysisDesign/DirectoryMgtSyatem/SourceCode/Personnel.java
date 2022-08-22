import java.util.*;

public class Personnel {

	private ArrayList<Person> personList;
	private totalObjects totalObjs;
	public Scanner scan = new Scanner(System.in);
	
	PersonnelFactory Perfac = new PersonnelFactory();

	public Personnel() {
	   personList = new ArrayList<Person>();
	   totalObjs =  ObjectInfo.getTotalObject();
	}

	public void addPersonnel(Person p)
	{
		personList.add(p);
	}
	
	public void addPersonnel(String first, String last, String middle) {
		personList.add(ObjectInfo.getPerson(first, last, middle));
		totalObjs.objectAdded();
	}
	
	
	public void createPerson() throws Exception {
		try {
			
			
			System.out.println("Enter first name: ");
			String firstN = scan.nextLine();
			
			System.out.println("Enter last name: ");
			String lastN = scan.nextLine();
			
			System.out.println("Enter middle name: ");
			String middleN = scan.nextLine();
			
			System.out.print("\nChoose your role category (1-Employee, 2-Executive, 3-Volentree, 4-Security) : ");
			int role = scan.nextInt();
			
			System.out.println("Enter empploy id : ");
			int empID = scan.nextInt();
			System.out.println("Enter base salaey");
			double salary = scan.nextDouble();
			scan.nextLine();

			personList.add(Perfac.createPersonnel(role, firstN, lastN, middleN, empID, salary));
			totalObjs.objectAdded();
		} catch (Exception e) {
			System.out.println("Incorrect input format. Start again!!");
		}
		
	}
	
	
	public void getPerson() {
		
		System.out.println("Enter firts name : ");
		String firstN = scan.nextLine();

		System.out.println("Enter last name : ");
		String lastN = scan.nextLine();
		
		boolean bExist = false;
		ArrayList<Person> arrTempPerList = getPersonList();
		for(int i=0; i<arrTempPerList.size(); i++) {
			if(arrTempPerList.get(i).getFirst().equals(firstN) && arrTempPerList.get(i).getLast().equals(lastN)) {
				if(!bExist) { 
					System.out.println("=========================================");
					System.out.println("      MATCH FOUND FOR THE PERSON        ");
					System.out.println("=========================================");
					bExist = true;
				}
				personList.get(i).printName(0);
			}
		}
		
		if(!bExist) {
			System.out.println("=========================================");
			System.out.println(            "NO RECORD FOUND"              );
			System.out.println("=========================================");
			addPersonnel(firstN, lastN, " ");
		}
	}
	
	
	public void printAllPersonNames() {
		System.out.println("Enter the order 0: first, middle,  last, 1: first, last, middle, 2: last, first , middle ");
		int order = scan.nextInt();
		
		for(int i=0; i<personList.size(); i++) {
			personList.get(i).printName(order);
		}
	}
	
	public ArrayList<Person> getPersonList() {
		return personList;
	}
	
	public int totalNoOfPersons() {
		return totalObjs.getTotalObjects();
	}

}