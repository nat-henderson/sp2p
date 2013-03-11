/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package simplepeer;

/**
 *
 * @author Jason
 */
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.URL;
import java.net.URLConnection;
import java.net.URLEncoder;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
 
public class HttpRequestUtility {
    
    /**
     * Makes a HTTP request to a URL and receive response
     * @param requestUrl the URL address
     * @param method Indicates the request method, "POST" or "GET"
     * @param params a map of parameters send along with the request
     * @return An array of String containing text lines in response
     * @throws IOException
     */
    public static String[] sendHttpRequest(String requestUrl, String method,
            Map<String, String> params) throws IOException {
        List<String> response = new ArrayList<String>();
        
       StringBuffer requestParams = new StringBuffer();
        
       if (params != null && params.size() > 0) {
           Iterator<String> paramIterator = params.keySet().iterator();
           while (paramIterator.hasNext()) {
               String key = paramIterator.next();
               String value = params.get(key);
               requestParams.append(URLEncoder.encode(key, "UTF-8"));
               requestParams.append("=").append(URLEncoder.encode(value, "UTF-8"));
               requestParams.append("&");
           }
       }
        
       URL url = new URL(requestUrl);
       URLConnection urlConn = url.openConnection();
       urlConn.setUseCaches(false);
        
       // the request will return a response
       urlConn.setDoInput(true);
        
       if ("POST".equals(method)) {
           // set request method to POST
           urlConn.setDoOutput(true);
       } else {
           // set request method to GET
           urlConn.setDoOutput(false);
       }
        
       if ("POST".equals(method) && params != null && params.size() > 0) {
           OutputStreamWriter writer = new OutputStreamWriter(urlConn.getOutputStream());
           writer.write(requestParams.toString());
           writer.flush();   
       }
        
       // reads response, store line by line in an array of Strings
       BufferedReader reader = new BufferedReader(new InputStreamReader(urlConn.getInputStream()));
 
        String line = "";
        while ((line = reader.readLine()) != null) {
            response.add(line);
        }
        
        reader.close();
        
        
        return (String[]) response.toArray(new String[0]);
    }
}
