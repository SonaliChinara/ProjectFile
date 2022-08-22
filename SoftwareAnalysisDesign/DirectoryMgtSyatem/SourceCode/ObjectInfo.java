
public class ObjectInfo {

	public static Person getPerson(String first, String last, String middle) {
		Person per = new Person();
		per.setFirst(first);
		per.setLast(last);
		per.setMiddle(middle);
		return per;
	}
	
	public static Personnel getPersonnel() {
		return new Personnel();
	}

	public static totalObjects getTotalObject() {
		return new totalObjects();
	}
}
