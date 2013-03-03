/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package simplepeer;

import java.io.File;

/**
 *
 * @author Jason
 */
public class DirectoryHash extends Thread {
    
    private File hashDir;
    
    public DirectoryHash(File hashDir) {
        this.hashDir = hashDir;
    }
    
    public void run(){
        
    }
}
