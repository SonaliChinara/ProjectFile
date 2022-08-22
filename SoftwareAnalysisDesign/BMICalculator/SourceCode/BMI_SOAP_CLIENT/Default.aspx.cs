using System;
using System.Net;
using System.IO;


namespace BMI_SOAP_CLIENT
{
    public partial class Default : System.Web.UI.Page
    {
        protected void Page_Load(object sender, EventArgs e)
        {

        }

        protected void Button1_Click(object sender, EventArgs e)
        {
            ServiceReference1.Service1Client myClient = new ServiceReference1.Service1Client();

            int weight = Int32.Parse(TextBox1.Text);
            int height = Int32.Parse(TextBox2.Text);
            double bmiValue = myClient.myBMI(height, weight);
            TextBox3.Text = bmiValue.ToString();

        }

        protected void Button2_Click(object sender, EventArgs e)
        {

            ServiceReference1.Service1Client myClient1 = new ServiceReference1.Service1Client("BasicHttpBinding_IService1");
            int weight = Int32.Parse(TextBox1.Text);
            int height = Int32.Parse(TextBox2.Text);
            double bmiValue = myClient1.myBMI(height, weight);
            TextBox3.Text = myClient1.myHealth(height, weight).BmiValue.ToString();
            TextBox4.Text = myClient1.myHealth(height, weight).Risk.ToString();
            TextBox5.Text = myClient1.myHealth(height, weight).More.ToString();
            if (bmiValue < 18)
            {
                TextBox4.ForeColor = System.Drawing.Color.Blue;
            }
            else if (bmiValue >= 18 && bmiValue < 25)
            {
                TextBox4.ForeColor = System.Drawing.Color.Green;
            }
            else if (bmiValue >= 25 && bmiValue <= 30)
            {
                TextBox4.ForeColor = System.Drawing.Color.Purple;
            }

            else if (bmiValue > 30)
            {
                TextBox4.ForeColor = System.Drawing.Color.Red;
            }


        }


        protected void Button3_Click(object sender, EventArgs e)
        {
            int weight = Int32.Parse(TextBox1.Text);
            int height = Int32.Parse(TextBox2.Text);
            string urlBmi = @"http://localhost:62745/Service1.svc/myBMI?height=" + height + "&weight=" + weight;
            HttpWebRequest request = (HttpWebRequest)WebRequest.Create(urlBmi);

            WebResponse response = request.GetResponse();
            Stream responseStream = response.GetResponseStream();
            StreamReader reader = new StreamReader(responseStream);
            String json = reader.ReadToEnd();
            TextBox6.Text = json.ToString();

        }


        protected void Button4_Click(object sender, EventArgs e)
        {
            int weight = Int32.Parse(TextBox1.Text);
            int height = Int32.Parse(TextBox2.Text);
            string urlMyhealth = @"http://localhost:62745/Service1.svc/myHealth?height=" + height + "&weight=" + weight;
            HttpWebRequest request = (HttpWebRequest)WebRequest.Create(urlMyhealth);

            WebResponse response = request.GetResponse();
            Stream responseStream = response.GetResponseStream();
            StreamReader reader = new StreamReader(responseStream);
            String json = reader.ReadToEnd();
            TextBox6.Text = json.ToString();
            
        }
    }
}