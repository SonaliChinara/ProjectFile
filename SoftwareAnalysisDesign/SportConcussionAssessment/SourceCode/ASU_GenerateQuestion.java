/*
 * File: ASU_GenerateQuestion.java
 * Author: Sonali Chinara
 * Purpose: This java file read the symptoms from a text file and show to the user
 *           
 * 
 */

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.LinkedList;

public class ASU_GenerateQuestion {
	

	private LinkedList<ASU_Symptoms> symptomObjList;
	private BufferedReader br;
	
	public ASU_GenerateQuestion() throws FileNotFoundException {
		this.br = new BufferedReader(new FileReader(new File("SymptomList")));
		this.symptomObjList = new LinkedList<>();
	}
	
	
	/**
	 * @return
	 * @throws IOException
	 * This function will display the symptom list which the Athlete has to fill 
	 */
	public boolean getQuestionList() throws IOException{
		String sLine;
		boolean bSuccess = false;
		BufferedReader brInput = new BufferedReader(new InputStreamReader(System.in));
		
		System.out.println("Please enter pain level for the below symptoms:");
		while((sLine = this.br.readLine()) != null) {
			String [] arrQuestion = sLine.split(",");
			
			int i = 0;
			Integer iVal = -2;
			while(i < arrQuestion.length) {
				//Read input from the text file and display
				String sMsg = String.format(" %d. Please enter your %-26s score [none (0), mild (1-2), moderate (3-4) & severe (5-6)]:  ", i+1, arrQuestion[i]);
				System.out.print(sMsg);
				try {
					 iVal = Integer.parseInt(brInput.readLine());
				} catch(NumberFormatException ne) {
					System.out.println("Please Enter Numeric Value ");
					continue;
				}
				if(iVal > -1 && iVal < 7) {
					ASU_Symptoms symptomObj = new ASU_Symptoms(i, arrQuestion[i], iVal);
					this.symptomObjList.add(symptomObj);
					i++;
				} else {
					System.out.println(" Not a valid option. Please enter value from [0-6]");
				}
			}
			System.out.println(" !!You have successfully fill the Symptom Evaluation Form!!");
			bSuccess = true;
		}
		return bSuccess;
	}
	
	public LinkedList<ASU_Symptoms> getGameQuestionValue() throws IOException{
		this.getQuestionList();
		return this.symptomObjList;
	}

}
