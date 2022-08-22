/*
 * File: ASU_Athlete.java
 * Author: Sonali Chinara
 * Purpose: This java file shows related Athlete information like Total Number of symptoms,severity score and over all rating
 *           
 * 
 */
import java.util.LinkedList;

public class ASU_Athlete {
	
	private String sAthleteID;
	private LinkedList<LinkedList<ASU_Symptoms>> symptomList;
	private String sOverAllRating;
	


	public ASU_Athlete(String sAthleteID) {
		this.sAthleteID = sAthleteID;
		this.symptomList = new LinkedList<>();
		this.sOverAllRating = "N/A";
	}
	
	
	public String getAthleteId() {
		return sAthleteID;
	}
	
	public void setAthleteId(String sAthleteID) {
		this.sAthleteID = sAthleteID;
	}
	
	public LinkedList<LinkedList<ASU_Symptoms>> getSymptomList() {
		return symptomList;
	}
	
	public void setSymptomList(LinkedList<LinkedList<ASU_Symptoms>> symptomList) {
		this.symptomList = symptomList;
	}
	
	public void addGame(LinkedList<ASU_Symptoms> symptomList) {
		this.symptomList.add(symptomList);
	}
	
	public String sOverAllRating() {
		return sOverAllRating;
	}

	public void setOvalAllRatingTag(String sOverAllRating) {
		this.sOverAllRating = sOverAllRating;
	}
	
	
	/**
	 * @param list_Evaluation
	 * This method will evaluate the summary based on symptom pain level
	 */
	public void printEvaluationValue(LinkedList<ASU_Symptoms> list_Evaluation) {		
		int iSymptomCount = 0;
		int iSeverityScore = 0;
		String sOverAllRating = "N/A";
		
		for(int i=0; i<list_Evaluation.size(); i++) {
			ASU_Symptoms symptomObj = list_Evaluation.get(i);
			if(symptomObj.get_questionValue() != 0) {
				iSymptomCount++;
				iSeverityScore += symptomObj.get_questionValue();
			}
		}
		
		
		if(iSymptomCount < 3 && iSeverityScore < 10 ) { 
			sOverAllRating = "No Difference";
		}
		else if (iSymptomCount < 3 && iSeverityScore >= 10)
			sOverAllRating = "Unsure";
		else {
			sOverAllRating = "Very Different";
		}
		
		System.out.println("     Total Number of Symptoms: " + iSymptomCount);
		System.out.println("     Symptom Severity score  : " + iSeverityScore);	
		System.out.println("     Overall Rating          : " + sOverAllRating);
		
	}
	
	public void displaySymptomQuestion() {
		for(int i=0; i<this.symptomList.size(); i++) {
			System.out.println("\n   Game No: " + Integer.valueOf(i+1));
			printEvaluationValue(this.symptomList.get(i));
		}
	}
	
	public boolean getSummaryReport() {
		ASU_SymptomSummary sympSummaryObj = new ASU_SymptomSummary();
		Boolean bFlag = sympSummaryObj.evaludateSymptom(this.symptomList);
		if(bFlag) {
			this.setOvalAllRatingTag(sympSummaryObj.getOverAllRatingTag());
		}
		return bFlag;
	}
	
	public boolean hasExistingRecord() {
		return ! this.symptomList.isEmpty();
	}	

}
