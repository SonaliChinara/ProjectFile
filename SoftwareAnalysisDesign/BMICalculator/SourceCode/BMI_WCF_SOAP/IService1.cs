using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.Serialization;
using System.ServiceModel;
using System.ServiceModel.Web;
using System.Text;

namespace BMI_WCF_SOAP
{
    // NOTE: You can use the "Rename" command on the "Refactor" menu to change the interface name "IService1" in both code and config file together.
    [ServiceContract]
    public interface IService1
    {

        [OperationContract]
        double myBMI(int height, int weight);

        [OperationContract]
        //CompositeType GetDataUsingDataContract(CompositeType composite);
        Bmi myHealth(int height, int weight);

        // TODO: Add your service operations here
    }


    // Use a data contract as illustrated in the sample below to add composite types to service operations.
    

    [DataContract]
    public class Bmi
    {
        //bool boolValue = true;
        //string stringValue = "Hello ";

        double bmiValue;
        string risk;

        string more;
       


        /*public static readonly string[] more = new string[3] { "https://www.cdc.gov/healthyweight/assessing/bmi/index.html",
                                        "https://www.nhlbi.nih.gov/health/educational/lose_wt/index.htm",
                                        "https://www.ucsfhealth.org/education/body_mass_index_tool/"};*/



        [DataMember]
        public double BmiValue
        {
            get { return bmiValue; }
            set { bmiValue = value; }
        }

        [DataMember]
        public string Risk
        {
            get { return risk; }
            set { risk = value; }
        }

        [DataMember]
        public string More
        {
            get { return more; }
            set { more = value; }
        }

        
    }
}
