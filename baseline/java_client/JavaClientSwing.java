/**
 * Java Swing Client - Baseline Implementation
 * 
 * This client connects to the Python TCP server and provides a GUI for:
 * - Entering commands (CSV loading, plotting, Python code)
 * - Viewing text output
 * - Displaying generated visualizations
 * 
 * Based on the research paper's Java GUI framework requirements.
 */
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.io.*;
import java.net.Socket;

public class JavaClientSwing extends JFrame {
    private JTextArea inputArea;
    private JTextArea outputArea;
    private JLabel imageLabel;
    private JButton sendButton;
    private Socket socket;
    
    private static final String HOST = "localhost";
    private static final int PORT = 5000;
    private static final int BUFFER_SIZE = 24576;
    
    public JavaClientSwing() {
        initializeGUI();
    }
    
    private void initializeGUI() {
        setTitle("Python Data Visualization Client - Swing");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setSize(1000, 700);
        setLocationRelativeTo(null);
        
        // Create main panel with border layout
        JPanel mainPanel = new JPanel(new BorderLayout(10, 10));
        mainPanel.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));
        
        // Input panel (top)
        JPanel inputPanel = new JPanel(new BorderLayout(5, 5));
        inputPanel.setBorder(BorderFactory.createTitledBorder("Input Commands"));
        inputArea = new JTextArea(5, 50);
        inputArea.setFont(new Font(Font.MONOSPACED, Font.PLAIN, 12));
        inputArea.setLineWrap(true);
        inputArea.setWrapStyleWord(true);
        JScrollPane inputScroll = new JScrollPane(inputArea);
        inputPanel.add(inputScroll, BorderLayout.CENTER);
        
        sendButton = new JButton("Send");
        sendButton.addActionListener(e -> sendCommand());
        inputPanel.add(sendButton, BorderLayout.EAST);
        
        // Output panel (middle)
        JPanel outputPanel = new JPanel(new BorderLayout(5, 5));
        outputPanel.setBorder(BorderFactory.createTitledBorder("Output Results"));
        outputArea = new JTextArea(10, 50);
        outputArea.setFont(new Font(Font.MONOSPACED, Font.PLAIN, 12));
        outputArea.setEditable(false);
        JScrollPane outputScroll = new JScrollPane(outputArea);
        outputPanel.add(outputScroll, BorderLayout.CENTER);
        
        // Visualization panel (bottom)
        JPanel vizPanel = new JPanel(new BorderLayout(5, 5));
        vizPanel.setBorder(BorderFactory.createTitledBorder("Visualization"));
        imageLabel = new JLabel("No visualization loaded", JLabel.CENTER);
        imageLabel.setHorizontalAlignment(JLabel.CENTER);
        imageLabel.setVerticalAlignment(JLabel.CENTER);
        imageLabel.setPreferredSize(new Dimension(800, 400));
        JScrollPane vizScroll = new JScrollPane(imageLabel);
        vizScroll.setPreferredSize(new Dimension(800, 400));
        vizPanel.add(vizScroll, BorderLayout.CENTER);
        
        // Add panels to main panel
        mainPanel.add(inputPanel, BorderLayout.NORTH);
        mainPanel.add(outputPanel, BorderLayout.CENTER);
        mainPanel.add(vizPanel, BorderLayout.SOUTH);
        
        add(mainPanel);
        
        // Add keyboard shortcut (Ctrl+Enter to send)
        inputArea.addKeyListener(new KeyAdapter() {
            @Override
            public void keyPressed(KeyEvent e) {
                if (e.isControlDown() && e.getKeyCode() == KeyEvent.VK_ENTER) {
                    sendCommand();
                }
            }
        });
    }
    
    private void sendCommand() {
        String command = inputArea.getText().trim();
        if (command.isEmpty()) {
            JOptionPane.showMessageDialog(this, "Please enter a command", "Error", JOptionPane.ERROR_MESSAGE);
            return;
        }
        
        // Disable button during execution
        sendButton.setEnabled(false);
        outputArea.append("> " + command + "\n");
        
        try {
            // Create socket connection
            socket = new Socket(HOST, PORT);
            
            // Send command
            PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
            out.println(command);
            out.flush();
            
            // Receive response
            InputStream in = socket.getInputStream();
            
            // Check if response is an image (chart command)
            if (command.equals("chart")) {
                // Read image size (4 bytes)
                byte[] sizeBytes = new byte[4];
                int bytesRead = 0;
                while (bytesRead < 4) {
                    int n = in.read(sizeBytes, bytesRead, 4 - bytesRead);
                    if (n == -1) break;
                    bytesRead += n;
                }
                
                if (bytesRead == 4) {
                    int imageSize = (sizeBytes[0] << 24) | ((sizeBytes[1] & 0xFF) << 16) | 
                                   ((sizeBytes[2] & 0xFF) << 8) | (sizeBytes[3] & 0xFF);
                    
                    // Read image data
                    ByteArrayOutputStream imageBuffer = new ByteArrayOutputStream();
                    byte[] buffer = new byte[8192];
                    int totalRead = 0;
                    
                    while (totalRead < imageSize) {
                        int n = in.read(buffer, 0, Math.min(buffer.length, imageSize - totalRead));
                        if (n == -1) break;
                        imageBuffer.write(buffer, 0, n);
                        totalRead += n;
                    }
                    
                    // Display image
                    byte[] imageData = imageBuffer.toByteArray();
                    ImageIcon icon = new ImageIcon(imageData);
                    
                    // Scale image if too large
                    Image img = icon.getImage();
                    int width = icon.getIconWidth();
                    int height = icon.getIconHeight();
                    
                    if (width > 800 || height > 400) {
                        double scale = Math.min(800.0 / width, 400.0 / height);
                        width = (int)(width * scale);
                        height = (int)(height * scale);
                        img = img.getScaledInstance(width, height, Image.SCALE_SMOOTH);
                        icon = new ImageIcon(img);
                    }
                    
                    imageLabel.setIcon(icon);
                    imageLabel.setText("");
                    outputArea.append("Chart generated successfully\n");
                } else {
                    outputArea.append("Error: Could not read image size\n");
                }
            } else {
                // Read text response
                BufferedReader reader = new BufferedReader(new InputStreamReader(in));
                StringBuilder response = new StringBuilder();
                String line;
                
                // Read with timeout
                long startTime = System.currentTimeMillis();
                while ((line = reader.readLine()) != null) {
                    response.append(line).append("\n");
                    if (System.currentTimeMillis() - startTime > 5000) break; // 5 second timeout
                }
                
                if (response.length() == 0) {
                    // Try reading raw bytes
                    ByteArrayOutputStream buffer = new ByteArrayOutputStream();
                    byte[] data = new byte[BUFFER_SIZE];
                    int n = in.read(data);
                    if (n > 0) {
                        response.append(new String(data, 0, n, "UTF-8"));
                    }
                }
                
                String output = response.toString();
                outputArea.append(output);
                if (!output.endsWith("\n")) {
                    outputArea.append("\n");
                }
            }
            
        } catch (IOException e) {
            outputArea.append("Error: " + e.getMessage() + "\n");
            e.printStackTrace();
        } finally {
            try {
                if (socket != null) {
                    socket.close();
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
            sendButton.setEnabled(true);
            outputArea.append("---\n");
        }
    }
    
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel(UIManager.getSystemLookAndFeel());
            } catch (Exception e) {
                e.printStackTrace();
            }
            
            JavaClientSwing client = new JavaClientSwing();
            client.setVisible(true);
        });
    }
}

