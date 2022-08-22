This SymptomList file contains all the 21 symptoms of the Athlete. This file is use in ASU_GenerateQuestion.java, line no 24

I kept SymptomList file in the same directory where the all othe java files are present, so "file not found" could not be an issue while executing the program.

Unfortunately, if  "File not found exception" came for the "SymptomList" file, then provide the actual path of the SymptomList file in ASU_GenerateQuestion.java, line no 24.

Below is the code when the file is used.
		br = new BufferedReader(new FileReader(new File("SymptomList")));
		
ASU_SportsConcussionSystem.java is the starting point of the project, which contains the main method





