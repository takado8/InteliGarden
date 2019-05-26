using System;
using System.IO;
using Newtonsoft.Json;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace userApp
{
    /// Background="#afd275"
    /// 
    public partial class MainWindow : Window
    {
        ftp _ftp;
        string path = "";
        Dictionary<string, string> state;

        public MainWindow()
        {
            InitializeComponent();
        }

        private void Window_Loaded(object sender, RoutedEventArgs e)
        {
            path = Directory.GetCurrentDirectory();
            //_ftp = new ftp("ftp://serwer1868028.home.pl/", "inteligarden01@serwer1868028.home.pl", "sgHR5$6yUO12jqQ3");
            //_ftp.Download("/state.json", path + "/state.json");
            var file = File.ReadAllText(path + "/state.json");

            state = JsonConvert.DeserializeObject<Dictionary<string, string>>(file);

            if (state["pump_1_interval"] != null) interval_1_tb.Text = state["pump_1_interval"];     
            if (state["pump_2_interval"] != null) interval_2_tb.Text = state["pump_2_interval"];
            if (state["pump_1_water_amount"] != null) water_amount_1_tb.Text = state["pump_1_water_amount"];
            if (state["pump_2_water_amount"] != null) water_amount_2_tb.Text = state["pump_2_water_amount"];
            if (state["water_level"] != null) water_level_lbl.Content = "Poziom wody: " + state["water_level"];
            if (state["tank_capacity"] != null) tank_max_tb.Text = state["tank_capacity"];

        }

        private void Interval_1_tb_TextChanged(object sender, TextChangedEventArgs e)
        {
            if (state != null && interval_1_tb.Text != "" && state["pump_1_interval"] != interval_1_tb.Text)
            {
                string value;
                if(lbl_days_1.Content.ToString() == "dni.")
                {
                    float val = float.Parse(interval_1_tb.Text) * 86400;  // days for seconds
                    value = val.ToString();
                }
                else
                {
                    value = interval_1_tb.Text;
                }
                state["pump_1_interval"] = value;
                string serialized = JsonConvert.SerializeObject(state);
                File.WriteAllText(path + "/state.json", serialized);
            }
        }

        private void Lbl_days_1_MouseDown(object sender, MouseButtonEventArgs e)
        {
            if (lbl_days_1.Content.ToString() == "dni.")
            {
                lbl_days_1.Content = "sek.";
                interval_1_tb.Text = (float.Parse(interval_1_tb.Text) * 86400).ToString();
            }
            else
            {
                lbl_days_1.Content = "dni.";
                interval_1_tb.Text = (float.Parse(interval_1_tb.Text) / 86400).ToString();
            }
        }
    }
}
