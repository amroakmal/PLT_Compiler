
namespace PLT
{
    partial class Form1
    {
        /// <summary>
        ///  Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        ///  Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        ///  Required method for Designer support - do not modify
        ///  the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.openFileDialog1 = new System.Windows.Forms.OpenFileDialog();
            this.rulesFileTextBox = new System.Windows.Forms.TextBox();
            this.rulesBtn = new System.Windows.Forms.Button();
            this.programBtn = new System.Windows.Forms.Button();
            this.programFileTextBox = new System.Windows.Forms.TextBox();
            this.button3 = new System.Windows.Forms.Button();
            this.cfgTextBox = new System.Windows.Forms.TextBox();
            this.contentTextBox = new System.Windows.Forms.TextBox();
            this.StartBtn = new System.Windows.Forms.Button();
            this.SuspendLayout();
            // 
            // openFileDialog1
            // 
            this.openFileDialog1.FileName = "openFileDialog1";
            // 
            // rulesFileTextBox
            // 
            this.rulesFileTextBox.Location = new System.Drawing.Point(12, 12);
            this.rulesFileTextBox.Name = "rulesFileTextBox";
            this.rulesFileTextBox.Size = new System.Drawing.Size(546, 27);
            this.rulesFileTextBox.TabIndex = 0;
            // 
            // rulesBtn
            // 
            this.rulesBtn.Location = new System.Drawing.Point(564, 12);
            this.rulesBtn.Name = "rulesBtn";
            this.rulesBtn.Size = new System.Drawing.Size(130, 29);
            this.rulesBtn.TabIndex = 1;
            this.rulesBtn.Text = "Load rules";
            this.rulesBtn.UseVisualStyleBackColor = true;
            this.rulesBtn.Click += new System.EventHandler(this.rulesBtn_Click);
            // 
            // programBtn
            // 
            this.programBtn.Location = new System.Drawing.Point(564, 47);
            this.programBtn.Name = "programBtn";
            this.programBtn.Size = new System.Drawing.Size(130, 29);
            this.programBtn.TabIndex = 3;
            this.programBtn.Text = "Load program";
            this.programBtn.UseVisualStyleBackColor = true;
            this.programBtn.Click += new System.EventHandler(this.programBtn_Click);
            // 
            // programFileTextBox
            // 
            this.programFileTextBox.Location = new System.Drawing.Point(12, 48);
            this.programFileTextBox.Name = "programFileTextBox";
            this.programFileTextBox.Size = new System.Drawing.Size(546, 27);
            this.programFileTextBox.TabIndex = 2;
            // 
            // button3
            // 
            this.button3.Location = new System.Drawing.Point(564, 82);
            this.button3.Name = "button3";
            this.button3.Size = new System.Drawing.Size(130, 29);
            this.button3.TabIndex = 5;
            this.button3.Text = "Load CFG";
            this.button3.UseVisualStyleBackColor = true;
            this.button3.Click += new System.EventHandler(this.button3_Click);
            // 
            // cfgTextBox
            // 
            this.cfgTextBox.Location = new System.Drawing.Point(12, 82);
            this.cfgTextBox.Name = "cfgTextBox";
            this.cfgTextBox.Size = new System.Drawing.Size(546, 27);
            this.cfgTextBox.TabIndex = 4;
            // 
            // contentTextBox
            // 
            this.contentTextBox.Location = new System.Drawing.Point(12, 115);
            this.contentTextBox.Multiline = true;
            this.contentTextBox.Name = "contentTextBox";
            this.contentTextBox.Size = new System.Drawing.Size(682, 393);
            this.contentTextBox.TabIndex = 6;
            // 
            // StartBtn
            // 
            this.StartBtn.Location = new System.Drawing.Point(12, 514);
            this.StartBtn.Name = "StartBtn";
            this.StartBtn.Size = new System.Drawing.Size(682, 29);
            this.StartBtn.TabIndex = 7;
            this.StartBtn.Text = "Start";
            this.StartBtn.UseVisualStyleBackColor = true;
            this.StartBtn.Click += new System.EventHandler(this.StartBtn_Click);
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 20F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackColor = System.Drawing.SystemColors.Control;
            this.ClientSize = new System.Drawing.Size(706, 555);
            this.Controls.Add(this.StartBtn);
            this.Controls.Add(this.contentTextBox);
            this.Controls.Add(this.button3);
            this.Controls.Add(this.cfgTextBox);
            this.Controls.Add(this.programBtn);
            this.Controls.Add(this.programFileTextBox);
            this.Controls.Add(this.rulesBtn);
            this.Controls.Add(this.rulesFileTextBox);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedSingle;
            this.MaximizeBox = false;
            this.Name = "Form1";
            this.Text = "PLT Compiler";
            this.Load += new System.EventHandler(this.Form1_Load);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.OpenFileDialog openFileDialog1;
        private System.Windows.Forms.TextBox rulesFileTextBox;
        private System.Windows.Forms.Button rulesBtn;
        private System.Windows.Forms.Button programBtn;
        private System.Windows.Forms.TextBox programFileTextBox;
        private System.Windows.Forms.Button button3;
        private System.Windows.Forms.TextBox cfgTextBox;
        private System.Windows.Forms.TextBox contentTextBox;
        private System.Windows.Forms.Button StartBtn;
    }
}

