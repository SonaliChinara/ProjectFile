public class Person {
	private String last;
	private String first;
	private String middle;

	public Person() {

	}

	public Person(String last, String first, String middle) {
		this.last = last;
		this.first = first;
		this.middle = middle;

	}

	public String getLast() {
		return last;
	}

	public void setLast(String last) {
		this.last = last;
	}

	public String getFirst() {
		return first;
	}

	public void setFirst(String first) {
		this.first = first;
	}

	public String getMiddle() {
		return middle;
	}

	public void setMiddle(String middle) {
		this.middle = middle;
	}

	public void printName(int order) {

		if (order == 0) {
			System.out.println(first + "  " + middle + "  " + last);

		} else if (order == 1) {

			//System.out.println(last + " ," + middle + " " + first);
			System.out.println(first + " ," + last + " " + middle);

		} else if (order == 2) {

			System.out.println(last + " ," + first + " " + middle);

		}
	}

}
