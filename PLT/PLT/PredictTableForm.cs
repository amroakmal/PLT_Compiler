using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Windows.Forms;

namespace PLT
{
    public partial class PredictTableForm : Form
    {
        public PredictTableForm()
        {
            InitializeComponent();
        }

        private void PredictTableForm_Load(object sender, EventArgs e)
        {
            var dataTable = ConvertCSVtoDataTable("predict-table.txt");

            dataGridView1.DataSource = dataTable;
            dataGridView1.AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.DisplayedCells;
        }


        public int HeadersLength(string filePath)
        {
            string line1 = File.ReadAllLines(filePath).First();

            return line1.Split("|").Length;
        }

        public DataTable ConvertCSVtoDataTable(string strFilePath)
        {
            DataTable dt = new DataTable();
            using (StreamReader sr = new StreamReader(strFilePath))
            {
                // header
    
                var len = HeadersLength(strFilePath);

                for (int i = 0; i < len; i++) dt.Columns.Add("");

                // rows

                while (!sr.EndOfStream)
                {
                    string[] rows = sr.ReadLine().Split("|");
                    DataRow dr = dt.NewRow();
                    for (int i = 0; i < len; i++)
                    {
                        dr[i] = rows[i];
                    }
                    dt.Rows.Add(dr);
                }

            }


            return dt;
        }
    }
}
