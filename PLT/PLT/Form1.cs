using System;
using System.Diagnostics;
using System.IO;
using System.Windows.Forms;

namespace PLT
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void rulesBtn_Click(object sender, EventArgs e)
        {
            if (openFileDialog1.ShowDialog() == DialogResult.OK)
            {
                rulesFileTextBox.Text = openFileDialog1.FileName;
                contentTextBox.Text = File.ReadAllText(openFileDialog1.FileName);
                var path = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "grammar.txt");
                File.Copy(openFileDialog1.FileName, path);
            }
        }

        private void programBtn_Click(object sender, EventArgs e)
        {
            if (openFileDialog1.ShowDialog() == DialogResult.OK)
            {
                programFileTextBox.Text = openFileDialog1.FileName;
                contentTextBox.Text = File.ReadAllText(openFileDialog1.FileName);
                var path = Path.Combine(AppDomain.CurrentDomain.BaseDirectory,"program.txt");
                File.Copy(openFileDialog1.FileName, path);
            }
        }

        private void button3_Click(object sender, EventArgs e)
        {
            if (openFileDialog1.ShowDialog() == DialogResult.OK)
            {
                cfgTextBox.Text = openFileDialog1.FileName;
                contentTextBox.Text = File.ReadAllText(openFileDialog1.FileName);
                var path = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "input_CFG_LL.txt");
                File.Copy(openFileDialog1.FileName, path);
            }
        }

        static void ExecuteCommand(string command)
        {
            int exitCode;
            ProcessStartInfo processInfo;
            Process process;

            processInfo = new ProcessStartInfo("cmd.exe", "/c " + command);
            processInfo.CreateNoWindow = true;
            processInfo.UseShellExecute = false;
            // *** Redirect the output ***
            processInfo.RedirectStandardError = true;
            processInfo.RedirectStandardOutput = true;

            process = Process.Start(processInfo);
            process.WaitForExit();

            // *** Read the streams ***
            // Warning: This approach can lead to deadlocks, see Edit #2
            string output = process.StandardOutput.ReadToEnd();
            string error = process.StandardError.ReadToEnd();

            exitCode = process.ExitCode;

            process.Close();
        }

        private void StartBtn_Click(object sender, EventArgs e)
        {
            ExecuteCommand("python main.py");
            System.Threading.Thread.Sleep(5000);
            GenerateFile();
            
            new FirstSetsForm().Show();
            new FollowSetsForm().Show();
            new ProductionsForm().Show();
            new PredictTableForm().Show();
            new ParsingForm().Show();
            new LeftMostForm().Show();
            new TokensForm().Show();
            new LinesTypesForm().Show();
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            if (File.Exists("grammar.txt")) File.Delete("grammar.txt");
            if (File.Exists("program.txt")) File.Delete("program.txt");
            if (File.Exists("output.txt")) File.Delete("output.txt");
            if (File.Exists("input_CFG_LL.txt")) File.Delete("input_CFG_LL.txt");
            if (File.Exists("tokens.txt")) File.Delete("tokens.txt");

            if (File.Exists("lines-types.txt")) File.Delete("lines-types.txt");
            if (File.Exists("first.txt")) File.Delete("first.txt");
            if (File.Exists("follow.txt")) File.Delete("follow.txt");
            if (File.Exists("productions.txt")) File.Delete("productions.txt");
            if (File.Exists("predict-table.txt")) File.Delete("predict-table.txt");
            if (File.Exists("parsing.txt")) File.Delete("parsing.txt");
            
            if (File.Exists("leftmost.txt")) File.Delete("leftmost.txt");
        }

        void GenerateFile()
        {
            var lines = File.ReadAllLines("output.txt");

            for (int i = 0; i < lines.Length; i++)
            {
                if (lines[i].Contains("//////////")) lines[i] = "//////////";
            }

            var total = string.Join(Environment.NewLine, lines);
            var segments = total.Split("//////////");
       

            using (StreamWriter sw = new StreamWriter("lines-types.txt"))
            {
                sw.Write(segments[0]);
                sw.Flush();
            }

            using (StreamWriter sw = new StreamWriter("first.txt"))
            {
                sw.Write(segments[1].Trim());
                sw.Flush();
            }

            using (StreamWriter sw = new StreamWriter("follow.txt"))
            {
                sw.Write(segments[2].Trim());
                sw.Flush();
            }

            using (StreamWriter sw = new StreamWriter("productions.txt"))
            {
                sw.Write(segments[4].Trim());
                sw.Flush();
            }

            using (StreamWriter sw = new StreamWriter("predict-table.txt"))
            {
                sw.Write(segments[5].Trim());
                sw.Flush();
            }

            using (StreamWriter sw = new StreamWriter("parsing.txt"))
            {
                sw.Write(segments[6].Trim());
                sw.Flush();
            }
            using (StreamWriter sw = new StreamWriter("leftmost.txt"))
            {
                sw.Write(segments[7].Trim());
                sw.Flush();
            }
        }


    }
}
