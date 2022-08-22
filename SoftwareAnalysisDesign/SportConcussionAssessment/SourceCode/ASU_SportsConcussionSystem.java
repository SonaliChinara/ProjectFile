/*
 * File: ASU_SportConcussionSystem
 * Author: Sonali Chinara
 * Purpose: The scs_objective of this java file to provide various option to the user
 *           
 * 
 */

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.HashMap;

public class ASU_SportsConcussionSystem {
	
	
	private BufferedReader br;
	private HashMap<String, ASU_Athlete> mapAthleteId;
	
	public ASU_SportsConcussionSystem() {
		this.br = new BufferedReader(new InputStreamReader(System.in));
		this.mapAthleteId = new HashMap<>();
	}
	
	public void roleOption() {
		System.out.println("\n Select your role: \n"
				+ "  1. Athlete \n"
				+ "  2. Sport Medical practitioners \n"
				+ "  3. Exit");
	}
	
	public void selectMenu(String strUserID) {
		System.out.println("\n              Athlete ID:  " + strUserID);
		System.out.println(" Select an options from the list: \n"
												+ "  1. Enter Symptoms \n"
												+ "  2. Display Symptom Summary \n"
												+ "  3. Am I at Risk? \n"
												+ "  4. Exit");
	}
	
	public String readInput() {
		String sLine = "";
		try {
			sLine = this.br.readLine();
		} catch (IOException e) {
			e.printStackTrace();
		}
		return sLine;
	}

	/**
	 * @param args
	 * @throws IOException
	 * This method give option to the user to select 
	 * Based on the selection, next option will come 
	 */
	/**
	 * @param args
	 * @throws IOException
	 */
	public static void main(String[] args) throws IOException {
		ASU_SportsConcussionSystem scs_obj = new ASU_SportsConcussionSystem();
		
		boolean bFlag = true;
		String str_optionNo;
		
		System.out.println("		!! Welcome to Sport Concussion Assessment System !!		");
		scs_obj.roleOption();
		
		while(bFlag) {
			str_optionNo = scs_obj.readInput();
			
			switch(str_optionNo) {
				//Case for Athlete
				case "1":					
					System.out.println("\n Enter Your Athlete ID: ");
					String athlete_Id = scs_obj.readInput();
					Boolean bLoop = true;
					ASU_Athlete athleteObj;
					
					if(! scs_obj.mapAthleteId.containsKey(athlete_Id)) {
						scs_obj.mapAthleteId.put(athlete_Id, new ASU_Athlete(athlete_Id));
					}
					athleteObj = scs_obj.mapAthleteId.get(athlete_Id);
					
					scs_obj.selectMenu(athleteObj.getAthleteId());
					while(bLoop && bFlag) {
						switch(scs_obj.readInput()) {
							//Athlete ID
							case "1":
								ASU_GenerateQuestion qFormGenerator = new ASU_GenerateQuestion();
								athleteObj.addGame(qFormGenerator.getGameQuestionValue());
								scs_obj.selectMenu(athleteObj.getAthleteId());
								break;
							
							//Symptom Evaluation Form and it's summary
							case "2":
								System.out.println("\n Symptoms Summary:");
								if(athleteObj.hasExistingRecord()) {
									athleteObj.displaySymptomQuestion();
								} else {
									System.out.println("\n No record(s) found !. "
														+ "Fill the Symptom Evaluation Form");
								}
								scs_obj.selectMenu(athleteObj.getAthleteId());
								break;
								
							//Risk Calculation
							case "3":
								System.out.println(" Am I at Risk?");
								if(athleteObj.getSummaryReport()) {
									String riskMessage = athleteObj.sOverAllRating();
									System.out.println(riskMessage);
									scs_obj.selectMenu(athleteObj.getAthleteId());
								}
								scs_obj.selectMenu(athleteObj.getAthleteId());
								break;
								
							case "4":
								bFlag = false;
								break;
							default:
								System.out.println("Please enter a valid option [1-4]\n");
						}
					}
					if(! bFlag) {
						System.out.println("!! Thank you for using Sport Concussion Assessment System !!");
						System.exit(0);
					}
					break;
					
				//For Sport Medical Partitioner
				case "2":
					System.out.println("\n 'Sport Medical practitioners' functionality is not a part of Sport Concussion Assessment System project \n 	Please select other options");
					scs_obj.roleOption();
					break;
					
				case "3":
					System.out.println("!! Thank you for using Sport Concussion Assessment System !!");
					bFlag = false;
					System.exit(0);
					break;
				default:
					System.out.println("\n Please enter a valid option");
					
			}
		}
		
	}
}
