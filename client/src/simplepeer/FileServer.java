/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package simplepeer;

import java.io.IOException;
import java.net.ServerSocket;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author Jason
 */
public class FileServer extends Thread{
    ServerSocket serverSocket = null;
    boolean listening;
    
    public FileServer(){
        listening = true;
        try{
            serverSocket = new ServerSocket(1020);
        }
        catch (IOException ex){
            Logger.getLogger(MainWindow.class.getName()).log(Level.SEVERE, null, ex);
        }
    }
    
    public void run() {
        while (listening){
            try{
                new FileSenderThread(serverSocket.accept()).start();
            }
            catch (IOException ex){
                Logger.getLogger(MainWindow.class.getName()).log(Level.SEVERE, null, ex);
            }
        }
    }
}
