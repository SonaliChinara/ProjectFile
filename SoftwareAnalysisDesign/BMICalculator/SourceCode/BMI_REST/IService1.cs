using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.Serialization;
using System.ServiceModel;
using System.ServiceModel.Web;
using System.Text;

namespace BMI_REST
{
    // NOTE: You can use the "Rename" command on the "Refactor" menu to change the interface name "IService1" in both code and config file together.
    [ServiceContract]
    public interface IService1
    {

        [OperationContract]
        [WebInvoke(Method = "GET", UriTemplate = "/myBMI?height={height}&weight={weight}",
                     RequestFormat = WebMessageFormat.Json,
                     ResponseFormat = WebMessageFormat.Json,
                     BodyStyle = WebMessageBodyStyle.Wrapped)]
        double myBMI(int height, int weight);

        [OperationContract]
        [WebInvoke(Method = "GET", UriTemplate = "/myHealth?height={height}&weight={weight}",
                     RequestFormat = WebMessageFormat.Json,
                     ResponseFormat = WebMessageFormat.Json,
                     BodyStyle = WebMessageBodyStyle.Wrapped)]
        Bmi myHealth(int height, int weight);
    }


    // Use a data contract as illustrated in the sample below to add composite types to service operations.
    [DataContract]

    public class Bmi
    {
        
        double bmiValue;
        string risk;
        string more;
       

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
