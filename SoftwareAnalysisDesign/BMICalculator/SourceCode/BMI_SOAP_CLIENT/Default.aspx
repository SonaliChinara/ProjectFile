<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="Default.aspx.cs" Inherits="BMI_SOAP_CLIENT.Default" %>

<!DOCTYPE html>

<html xmlns="http://www.w3.org/1999/xhtml">
<head runat="server">
    <title></title>
</head>
<body>
    <form id="form1" runat="server">
        <br />
        <br />
        <div><br/><br/>
              <p style="text-align:center;"> <b>                 
                    <asp:Label ID="Label1" style="text-align:center" runat="server" Text="BMI Calculation SOC Application" Font-Bold="True" Font-Size="Large" Font-Underline="False" ForeColor="#660033"></asp:Label>
              </b></p>              

            <br/>

            <p style="text-align:center;">
                <asp:Label ID="Label2" runat="server" Text="Enter Weight [lb]  "></asp:Label>&nbsp;
                <asp:TextBox ID="TextBox1" runat="server" ></asp:TextBox> <br/> <br/>

                <asp:Label ID="Label3" runat="server" Text="Enter Height [in] "></asp:Label>&nbsp; 
                <asp:TextBox ID="TextBox2" runat="server" ></asp:TextBox> <br/> <br/>

                <asp:Button ID="Button1" runat="server"  Text="Generate BMI (Soap)" OnClick="Button1_Click" BackColor="#66CCFF" Font-Bold="True" /> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                <asp:Button ID="Button2" runat="server"  Text="My Health Details (Soap)" OnClick="Button2_Click" BackColor="#66CCFF" Font-Bold="True" /><br /><br />
             </p>
                <asp:Label ID="Label4" Style="margin-left:499px;" runat="server" Text="BMI Value"></asp:Label>&nbsp; 
                <asp:TextBox ID="TextBox3"  runat="server" Height="20px" Width="282px" ></asp:TextBox> <br/> <br/>
                <asp:Label ID="Label5" Style="margin-left:499px;" runat="server" Text="Risk"></asp:Label>&nbsp; 
                <asp:TextBox ID="TextBox4" Style="margin-left:50px;" runat="server" Height="24px" Width="205px" ></asp:TextBox> <br/> <br/>
                <asp:Label ID="Label6" Style="margin-left:499px;" runat="server" Text="More"></asp:Label>&nbsp; 
                <asp:TextBox ID="TextBox5" Style="margin-left:50px;" TextMode="MultiLine" runat="server" Height="64px" Width="451px" ></asp:TextBox> <br/> <br/>

             <p style="text-align:center;">
                <asp:Button ID="Button3" runat="server"  Text="Generate BMI (Rest)" OnClick="Button3_Click" BackColor="#66CCFF" Font-Bold="True" /> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                 <asp:Button ID="Button4" runat="server"  Text="My Health Details (Rest)" OnClick="Button4_Click" BackColor="#66CCFF" Font-Bold="True" /><br /><br />
             </p>   
            <asp:Label ID="Label7" Style="margin-left:499px;" runat="server" Text="Health Details (Rest)"></asp:Label>&nbsp; 
            <asp:TextBox ID="TextBox6" Style="margin-left:50px;" TextMode="MultiLine" runat="server" Height="64px" Width="451px" ></asp:TextBox>

        </div>

    </form>
</body>
</html>
