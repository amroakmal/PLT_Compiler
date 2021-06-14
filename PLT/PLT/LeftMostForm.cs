using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.IO;
using System.Text;
using System.Windows.Forms;

namespace PLT
{
    public partial class LeftMostForm : Form
    {
        public LeftMostForm()
        {
            InitializeComponent();
        }

        private void LeftMostForm_Load(object sender, EventArgs e)
        {
            var dataTable = ConvertCSVtoDataTable("leftmost.txt");

            dataGridView1.DataSource = dataTable;
            dataGridView1.AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.DisplayedCells;
        }


        public DataTable ConvertCSVtoDataTable(string strFilePath)
        {
            DataTable dt = new DataTable();
            using (StreamReader sr = new StreamReader(strFilePath))
            {
                // header

                dt.Columns.Add("");

                // rows

                while (!sr.EndOfStream)
                {
                    var rows = sr.ReadLine();
                    DataRow dr = dt.NewRow();
                    dr[0] = rows;

                    dt.Rows.Add(dr);
                }

            }


            return dt;
        }
    }
}
