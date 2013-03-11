/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package simplepeer;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.ObjectOutputStream;
import java.net.Socket;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author Jason
 */
public class FileSenderThread extends Thread{
    
    private Socket connection;
    private ObjectOutputStream outStream;
    
    public FileSenderThread(Socket connection){
        this.connection = connection;
        try {
            outStream = new ObjectOutputStream(
                                connection.getOutputStream());
            outStream.flush();
             
        } catch (IOException e) {
            System.out.println("Output stream Error!");
        }
    }
    
    public void run(){
        BufferedReader in = null;
        try {
            in = new BufferedReader(new InputStreamReader(connection.getInputStream()));
            String fileReq = in.readLine();

            String hash = fileReq.split("~!~")[0];

            File file = MainWindow.fileMap.get(hash);

            long fileSize = file.length();
            long completed = 0;
            int step = 150000;
            // creates the file stream
            FileInputStream fileStream = new FileInputStream(file);
            // sending a message before streaming the file
            outStream.writeObject("SENDING_FILE|" + 
                                 file.getName() + 
                                 "|" + fileSize);
            byte[] buffer = new byte[step];
            while (completed <= fileSize) {
                fileStream.read(buffer);
                outStream.write(buffer);
                completed += step;
            }
            outStream.writeObject("SEND_COMPLETE");
            fileStream.close();
        }
        catch (IOException ex) {
                Logger.getLogger(FileSenderThread.class.getName()).log(Level.SEVERE, null, ex);
            } finally {
                try {
                    in.close();
                } catch (IOException ex) {
                    Logger.getLogger(FileSenderThread.class.getName()).log(Level.SEVERE, null, ex);
            }
        }
    }
}
