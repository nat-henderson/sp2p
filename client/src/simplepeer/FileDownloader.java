/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package simplepeer;

import java.io.BufferedReader;
import java.io.DataInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author Jason
 */
public class FileDownloader implements Runnable {
    private String ip;
    private String filename;
    private String hash;
    private String port;
    
    public FileDownloader(){
        
    }
    
    public FileDownloader(String ip, String filename, String hash, String port){
        
    }
    
    @Override
    public void run(){
        downloadFile();
    }
    
    private void downloadFile(){
        Socket dlSocket = null;
        PrintWriter out = null;
        //BufferedReader in = null;
        InputStream in = null;

        try {
            dlSocket = new Socket(ip, Integer.parseInt(port));
            out = new PrintWriter(dlSocket.getOutputStream(), true);
            //in = new BufferedReader(new InputStreamReader(
            //                            dlSocket.getInputStream()));
            in = new DataInputStream(dlSocket.getInputStream());
        } catch (UnknownHostException e) {
            System.err.println("Unable to contact " + ip + ".");
            System.exit(1);
        } catch (IOException e) {
            System.err.println("Couldn't get I/O for the connection to: " + ip + ".");
            System.exit(1);
        }

        try{
            out.println(filename+"~!~"+hash);
            
            FileOutputStream outStream = 
                      new FileOutputStream(filename);
            byte[] buffer = new byte[200000];
            int bytesRead = 0, counter = 0;
 
            while (bytesRead >= 0) {
                bytesRead = in.read(buffer);
                if (bytesRead >= 0) {
                    outStream.write(buffer, 0, bytesRead);
                    counter += bytesRead;
                    System.out.println("total bytes read: " +
                                                    counter);
                }
                if (bytesRead < 1024) {
                    outStream.flush();
                    break;
                }
            }
 
            System.out.println("Download Successful!");
            outStream.close();
            
            out.close();
            in.close();
            dlSocket.close();
        }
        catch (IOException ex){
                Logger.getLogger(MainWindow.class.getName()).log(Level.SEVERE, null, ex);
        }
    }
}
