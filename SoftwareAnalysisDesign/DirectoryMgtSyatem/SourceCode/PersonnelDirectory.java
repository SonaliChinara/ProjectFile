import java.util.Scanner;

public class PersonnelDirectory {
	
	
	
	public static Personnel per = ObjectInfo.getPersonnel();

	public static void main(String[] args) throws Exception {
		
		Scanner scan = new Scanner(System.in);
		int choice = -1;
		
		do {

			selectMenu();
			choice = scan.nextInt();
			scan.nextLine();

			switch (choice) {
			case 1:
				per.createPerson();
				break;

			case 2:
				per.getPerson();
				break;
			case 3:
				per.printAllPersonNames();
				break;

			case 4:
				System.out.println("Total Entries : " + per.totalNoOfPersons());
				break;	
			case 5:
				System.exit(0);
			default:
				System.out.println("Please choose valid option!");
				break;

			}
		

		} while (true);
		
		

	}
	
	
	/**
	 * This function will give the option to user to select menu
	 */
	public static void selectMenu() {
		System.out.println("Welcome to the Personnel Directory Management System");
        System.out.println("====================================================");

        System.out.println("\n\n\t 1. Add Personel");
        System.out.println("\n\t 2. Find Personel");
        System.out.println("\n\t 3. Print Names");
        System.out.println("\n\t 4. Number of Entries in the Directory");
        System.out.println("\n\t 5. Exit");

        System.out.println("\n\t Select one of the options above (1, 2, 3, 4, 5)");
	}

}