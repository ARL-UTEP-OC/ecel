import java.io.*;
import java.util.*;
import java.text.*;

public class TimedToJSON {
    static long numItems = 0;
	public static void main(String args[]) {
		try {
			if (args.length != 2)
			{
				System.out.println("Usage: java TimedToJSON <PathToImages> <Output Path>");
				System.exit(-1);
			}
			System.out.println("Parsing timed snapshot data");
			String answer = "[\n";

			String path = args[0];
			String outputPath = args[1];
			String parsedFilename[];
			String timestamp;
		    SimpleDateFormat toFormat = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss");
		    toFormat.setTimeZone(TimeZone.getTimeZone("UTC"));
			//For each file in the directory...
			File dir = new File(path);
						File[] directoryListing = dir.listFiles(new FilenameFilter() {
                public boolean accept(File dir, String name) {
                    return name.toLowerCase().endsWith(".png");
                }
            });
			if (directoryListing != null && directoryListing.length > 0) {
				for (int i=0; i< directoryListing.length; i++)
				{
				    File child = directoryListing[i];
					parsedFilename = child.getName().trim().split("_");
					timestamp = toFormat.format(new Date(((long)Double.parseDouble(parsedFilename[0])*1000)));
					if(parsedFilename.length < 2)
						continue;
					//unescape characters for use by html
					answer += "\t{\"timed_id\" : "+(numItems++)+",\n";
					answer += "\t\"content\" : \" \",\n";
					answer += "\t\"type\" : \"point\",\n";
					answer += "\t\"classname\" : \"imgPoint\",\n";
					answer += "\t\"title\" : \""+quote(child.getAbsolutePath())+"\",\n";
					answer += "\t\"start\" : \"" + timestamp + "\"\n";
					answer += "\t}"+ (i==directoryListing.length-1?"\n":",\n\n");
				}
			}
		else
			System.out.println("\tNo timed data items found");
		answer += "]\n";
		System.out.println("\tFinished parsing timed snapshot data");
        FileOutput.WriteToFile(outputPath + "/timed.JSON", answer);
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	/**
	* Code adapted from Jettison JSONObject open source software:
	* http://grepcode.com/file/repo1.maven.org/maven2/org.codehaus.jettison/jettison/1.3.3/org/codehaus/jettison/json/JSONObject.java#JSONObject
	*/
	public static String quote(String string) {
         if (string == null || string.length() == 0) {
             return "";
         }

         char         c = 0;
         int          i;
         int          len = string.length();
         StringBuilder sb = new StringBuilder(len + 4);
         String       t;

         //sb.append('"');
         for (i = 0; i < len; i += 1) {
             c = string.charAt(i);
             switch (c) {
             case '\\':
             case '"':
                 sb.append('\\');
                 sb.append(c);
                 break;
             case '/':
 //                if (b == '<') {
                     sb.append('\\');
 //                }
                 sb.append(c);
                 break;
             case '\b':
                 sb.append("\\b");
                 break;
             case '\t':
                 sb.append("\\t");
                 break;
             case '\n':
                 sb.append("\\n");
                 break;
             case '\f':
                 sb.append("\\f");
                 break;
             case '\r':
                sb.append("\\r");
                break;
             default:
                 if (c < ' ') {
                     t = "000" + Integer.toHexString(c);
                     sb.append("\\u" + t.substring(t.length() - 4));
                 } else {
                     sb.append(c);
                 }
             }
         }
         //sb.append('"');
         return sb.toString();
     }
}
