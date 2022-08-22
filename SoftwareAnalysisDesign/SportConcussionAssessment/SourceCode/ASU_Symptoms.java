/*
 * File: ASU_Symptoms.java
 * Author: Sonali Chinara
 * Purpose: This java file get and set the id,symptom name and value
 *           
 * 
 */
public class ASU_Symptoms {
	
	private int questionID;
	private String questionName;
	private int questionValue;
	
	public ASU_Symptoms() {}

	public ASU_Symptoms(int qId, String qName, int qValue) {
		this.questionID = qId;
		this.questionName = qName;
		this.questionValue = qValue;
	}
	
	public int get_questionID() {
		return questionID;
	}
	
	public void set_questionID(int questionID) {
		this.questionID = questionID;
	}
	
	public String get_questionName() {
		return questionName;
	}
	
	public void set_qname(String questionName) {
		this.questionName = questionName;
	}
	
	public int get_questionValue() {
		return questionValue;
	}
	
	public void set_questionValue(int questionValue) {
		this.questionValue = questionValue;
	}
	

}
