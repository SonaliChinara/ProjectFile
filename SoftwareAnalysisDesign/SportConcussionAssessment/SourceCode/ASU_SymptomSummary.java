import java.util.HashMap;
import java.util.LinkedList;

public class ASU_SymptomSummary {
	
	private int iTotalNoofSymptoms;
	private int iSeverityScore;
	private String sRating;
	private HashMap<String, Integer> questionValueMap = new HashMap<>();
	
	public ASU_SymptomSummary() {
		this.sRating = "N/A";
		this.iTotalNoofSymptoms = 0;
		this.iSeverityScore = 0;
	}
	
	
	public String getOverAllRatingTag() {
		return sRating;
	}


	public void setOverAllRatingTag(String sRating) {
		this.sRating = sRating;
	}


	/**
	 * @param symptomList
	 * @return
	 * This method will calculate the difference between total symptom difference and severity score. 
	 * Based on the result provide the rating
	 */
	public boolean evaludateSymptom(LinkedList<LinkedList<ASU_Symptoms>> symptomList) {
		
		this.sRating = "N/A";
		this.iTotalNoofSymptoms = 0;
		this.iSeverityScore = 0;
		
		int totalNoOfGames = symptomList.size();
		int count = totalNoOfGames -1;
		
		if(symptomList.size() < 2) {
			System.out.println("   Error: Mininum 2 games is required for 'Symptom Evaluation'. Please use option 1. to fill game evaluation.");
			return false;
			
		}
				
		while(count >= totalNoOfGames -2) {
			if(questionValueMap.isEmpty() || questionValueMap.size() == 0) {
			  symptomList.get(count).forEach( (qObj)-> questionValueMap.put(qObj.get_questionName(), (int)qObj.get_questionValue()));
			} else {
				for(ASU_Symptoms obj: symptomList.get(count)) {
					if(questionValueMap.getOrDefault(obj.get_questionName(), 0) != obj.get_questionValue()) {
						this.iTotalNoofSymptoms++;
						this.iSeverityScore += Math.abs(questionValueMap.getOrDefault(obj.get_questionName(), 0) - obj.get_questionValue());
					}
				}
			}
			count--;			
		}
		
		//Overall Rating comparision
		if(this.iTotalNoofSymptoms < 3) { 
			if (this.iSeverityScore < 10) {
				this.sRating = " #### No Difference [GREEN] #### ";
			} else {
				this.sRating = " #### Unsure [YELLOW] #### ";
			}
		}
		else {
			this.sRating = " #### Very Different [RED] #### ";
		}
		
		return true;
	}

}
