using System;
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
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        int current_zone = 1;

        public MainWindow()
        {
            InitializeComponent();
        }

        private void Next_zone_Click(object sender, RoutedEventArgs e)
        {
            if(++current_zone == 3)
            {
                current_zone = 1;
            }
            zone_lbl.Content = "Strefa " + current_zone.ToString();
        }
    }
}
