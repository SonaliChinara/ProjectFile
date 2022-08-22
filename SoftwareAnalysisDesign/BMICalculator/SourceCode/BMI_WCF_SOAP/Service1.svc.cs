using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.Serialization;
using System.ServiceModel;
using System.ServiceModel.Web;
using System.Text;

namespace BMI_WCF_SOAP
{
    // NOTE: You can use the "Rename" command on the "Refactor" menu to change the class name "Service1" in code, svc and config file together.
    // NOTE: In order to launch WCF Test Client for testing this service, please select Service1.svc or Service1.svc.cs at the Solution Explorer and start debugging.
    public class Service1 : IService1
    {
        public double myBMI(int height, int weight)
        {
            double bmi = 1.0f * weight / height / height * 703;
            return bmi;
        }

        public Bmi myHealth (int height, int weight)
        {
            Bmi objBmi = new Bmi();
            objBmi.BmiValue = myBMI(height, weight);
            objBmi.More = "https://www.cdc.gov/healthyweight/assessing/bmi/index.html, https://www.nhlbi.nih.gov/health/educational/lose_wt/index.htm, https://www.ucsfhealth.org/education/body_mass_index_tool/";
            

            if (objBmi.BmiValue < 18)
            {
                objBmi.Risk = "You are underweight";
            }

            else if (objBmi.BmiValue >= 18 && objBmi.BmiValue < 25)
            {
                objBmi.Risk = "You are normal";
            }
            else if (objBmi.BmiValue >= 25 && objBmi.BmiValue <= 30)
            {
                objBmi.Risk = "You are pre-obese";
            }

            else if (objBmi.BmiValue > 30)
            {
                objBmi.Risk = "You are obese";
            }
            else
            {
                objBmi.Risk = "ERROR";
            }           
            return objBmi;

        }

    }
}
