using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.Serialization;
using System.ServiceModel;
using System.ServiceModel.Web;
using System.Text;

namespace BMI_REST
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

        public Bmi myHealth(int height, int weight)
        {
            Bmi b = new Bmi();
            b.BmiValue = myBMI(height, weight);
            b.More = "https://www.cdc.gov/healthyweight/assessing/bmi/index.html, https://www.nhlbi.nih.gov/health/educational/lose_wt/index.htm, https://www.ucsfhealth.org/education/body_mass_index_tool/";

            if (b.BmiValue < 18)
            {
                b.Risk = "You are underweight";
            }
            else if (b.BmiValue >= 18 && b.BmiValue < 25)
            {
                b.Risk = "You are normal";
            }
            else if (b.BmiValue >= 25 && b.BmiValue <= 30)
            {
                b.Risk = "You are pre-obese";
            }

            else if (b.BmiValue > 30)
            {
                b.Risk = "You are obese";
            }
            else
            {
                b.Risk = "ERROR";
            }
            return b;
        }
    }
}
