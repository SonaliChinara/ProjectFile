
/**
 * This java file take care of creating all type of person objects 
 *
 */
public class PersonnelFactory implements IntefacePersonnelFactory{	

	@Override
	public Person createPersonnel (int personType, String first, String last, String middle, int id, double salary) {		
		if(personType == 1){
		    return new Employee(last, first, middle, id, salary);     
		} 
		else if(personType == 2){
		    return new Executives(last, first, middle,id, salary);
		} 
		else if(personType == 3){
			return new Volunteers(last, first, middle, id, salary);
		}
		else if(personType == 4){
			return new Security(last, first, middle, id, salary);
		}
		else {
			return null;
		}
					
	}
	
}
