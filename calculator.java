import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.io.*;

public class calculator extends JFrame implements ActionListener {
    JTextArea area = new JTextArea();
    JMenuItem open, save, exit;

    public calculator() {
        setTitle("Mini Word Editor");
        setSize(500, 400);

        JMenuBar mb = new JMenuBar();
        JMenu file = new JMenu("File");

        open = new JMenuItem("Open");
        save = new JMenuItem("Save");
        exit = new JMenuItem("Exit");

        open.addActionListener(this);
        save.addActionListener(this);
        exit.addActionListener(this);

        file.add(open);
        file.add(save);
        file.add(exit);
        mb.add(file);

        add(new JScrollPane(area));
        setJMenuBar(mb);

        setDefaultCloseOperation(EXIT_ON_CLOSE);
        setVisible(true);
    }

    public void actionPerformed(ActionEvent e) {
        try {
            if (e.getSource() == open) {
                JFileChooser fc = new JFileChooser();
                if (fc.showOpenDialog(this) == JFileChooser.APPROVE_OPTION) {
                    area.read(new FileReader(fc.getSelectedFile()), null);
                }
            }
            if (e.getSource() == save) {
                JFileChooser fc = new JFileChooser();
                if (fc.showSaveDialog(this) == JFileChooser.APPROVE_OPTION) {
                    area.write(new FileWriter(fc.getSelectedFile()));
                }
            }
            if (e.getSource() == exit) {
                System.exit(0);
            }
        } catch (Exception ex) {
        }
    }

    public static void main(String[] args) {
        new calculator();
    }
}
