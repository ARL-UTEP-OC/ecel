import java.io.*;
import java.util.*;
import java.text.*;

public class ManualScreenshotToJSON {
	static long numItems = 0;
	public static void main(String args[]) {
//sample output:
//[{content:" ", className:"imgPoint", title:"<link>", start:'2016-06-09 17:36:51', end:'2016-06-09 17:36:51' },
//{content:" ", className:"imgPoint", title:"<link>", start:'2016-06-09 17:36:51', end:'2016-06-09 17:36:51' },
//]
		try {
			if (args.length != 2)
			{
				System.out.println("Usage: java ClicksToJSON <PathToImages> <Output Path>");
				System.exit(-1);
			}
    		String path = args[0];
			System.out.println("Parsing manual screenshot data");

			File dir = new File(path);
			File[] directoryListing = dir.listFiles(new FilenameFilter() {
                public boolean accept(File dir, String name) {
                    return name.toLowerCase().endsWith(".png");
                }
            });

			if (directoryListing != null && directoryListing.length > 0) {
    			String answer = "[\n";

    			String outputPath = args[1];
    			String parsedFilename[];
    			SimpleDateFormat fromFormat = new SimpleDateFormat("yyyyMMdd-HHmmss");
    			SimpleDateFormat toFormat = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss");
    			toFormat.setTimeZone(TimeZone.getTimeZone("UTC"));
    			String tmpDate = "";
    			String validDateFormat = "";
    			//For each file in the directory...

				for(int i=0; i<directoryListing.length; i++)
				{
				    File child = directoryListing[i];
					parsedFilename = child.getName().trim().split("-");

					if(parsedFilename.length < 2)
						continue;
					//unescape characters for use by html
					answer += "\t{\"manualscreen_id\" : "+(numItems++)+",\n";
					answer += "\t\"content\" : \" \",\n";
					answer += "\t\"type\" : \"point\",\n";
					answer += "\t\"classname\" : \"imgPoint\",\n";
					answer += "\t\"title\" : \""+quote(child.getAbsolutePath())+"\",\n";
					answer += "\t\"comment\" : \"";
					for(int j=0; j< parsedFilename.length -2; j++)
                        answer += parsedFilename[j] + (j==parsedFilename.length-3?"":"-");
					answer += "\",\n";
					for(int j=parsedFilename.length-2; j< parsedFilename.length; j++)
                        tmpDate = parsedFilename[parsedFilename.length-2] + "-" + parsedFilename[parsedFilename.length-1].replace(".png","");
                    System.out.println("\tparsing: " + tmpDate);
                    validDateFormat = toFormat.format(fromFormat.parse(tmpDate));
					answer += "\t\"start\" : \"" + validDateFormat + "\"\n";
					answer += "\t}"+ (i==directoryListing.length-1?"\n":",\n\n");
				}
			answer += "\n]";
            //System.out.println(answer + "]\n}");
            System.out.println("\tFinished parsing manual screenshot data");
            FileOutput.WriteToFile(outputPath + "/snap.JSON", answer);
			}
		else
		{
		    System.out.print("\tNo data items found");
		}
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
