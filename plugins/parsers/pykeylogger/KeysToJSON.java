import java.io.*;
import java.util.*;
import java.text.*;

public class KeysToJSON{
    static long numItems = 0;
	public static void main(String args[]) {
		try {
			if (args.length != 2)
			{
				System.out.println("Usage: java KeysToJSON <filename> <output-directory>");
				System.exit(-1);
			}
			System.out.println("Parsing keystroke data");
			String answer = "[\n";
			String filename = args[0];
			String outputPath = args[1];
			int count = 0;

			//sample: {\"content\" :\"<2 p/s\", \"className\" :\"traffic\", \"title\" : \"eth:ipv6:udp:dhcpv6\" \n', \"start\" : \"Wed Oct 08 10:56:33 EDT 2014\"},

			FileReader fr = new FileReader(filename);
			BufferedReader br = new BufferedReader(fr);
			String line;
			String parsedLine[];
			int delayBeforeNewString = 2;
			String timestamp;
		    SimpleDateFormat toFormat = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss");
		    toFormat.setTimeZone(TimeZone.getTimeZone("UTC"));
			double currKeyTime = 0;
			double prevKeyTime = 0;
			double currWindowStartTime = 0;
			String setOfKeys = "";
			line = br.readLine();
			if(line != null)
			{
			currWindowStartTime = Double.parseDouble(line.trim().split("\\|",-1)[1]);
			prevKeyTime = currWindowStartTime;

			//check if we have another line to read
			while (line != null) {
				count++;
				//remove new line and split the line using | as the delimeter
				//parsedLine = line.trim().split("\\|",-1);
				parsedLine = line.split("\\|",-1);
				//if we have data
				if(parsedLine.length > 1)
				{
				currKeyTime = Double.parseDouble(parsedLine[1]);
				//if this line is within the time threshold and it is not the last line
				if(parsedLine[parsedLine.length-1].contains("KeyName:")){
						parsedLine[parsedLine.length-1] = parsedLine[parsedLine.length-1].replace("KeyName:","");
				}
				//if(currKeyTime - prevKeyTime < delayBeforeNewString && !parsedLine[parsedLine.length-1].equals("[Return]") && br.ready()){ REMOVED FOR TESTING TIMEFRAMES AF
				if(currKeyTime - prevKeyTime < delayBeforeNewString && br.ready()){
					
					//need to add the space back in (trim removes it).
					if(parsedLine[parsedLine.length-1].equals("")){
						setOfKeys += " ";
					}
					else{												
						setOfKeys += parsedLine[parsedLine.length-1];
					}
				}
				else{
					if(!setOfKeys.trim().equals(""))
					{
					    timestamp = toFormat.format(new Date(((long)(prevKeyTime*1000))));
						//unescape characters for use by html
						answer += "\t{\"keypresses_id\" : "+(numItems++)+", ";
						answer += "\"content\" : \"";
						answer += quote(setOfKeys);
						answer += "\", ";
						
						answer += "\"className\" : \"Keypresses";
						answer += "\", ";
										
						answer += "\"start\" : \"";
						//answer += new Date(((long)(currWindowStartTime*1000))).toString() + "\",";
						answer += timestamp.toString();
						answer += "\"";
						answer += "}";
						
						if(parsedLine[parsedLine.length-1].equals(""))
							setOfKeys = " ";
						else
							setOfKeys = parsedLine[parsedLine.length-1];
						currWindowStartTime = currKeyTime;
						//check if this was the last of the input, if not add a comma
						if(br.ready())
							answer += ",";
						answer += "\n";
					}
				}
			}
				prevKeyTime = currKeyTime;
				line = br.readLine();
			} 
		}
		//System.out.println(answer + "\n]");
		System.out.println("\tFinished processing keystroke data");
		br.close();
		//if there are no keystrokes
		if(line == null && count == 0){
			answer += "\t{\"keypresses_id\" : 0, \"content\" : \"No detected 	keystrokes\", \"className\" : \"Keypresses\", \"start\" : \"";
			timestamp = toFormat.format(new Date(((long)(prevKeyTime*1000))));
			answer += timestamp.toString();
			answer += "\"";
			answer += "} \n";
		}
		answer += "]\n";
        FileOutput.WriteToFile(outputPath + "/keypressData.JSON", answer);
        //System.out.println(answer);
		}
		catch (FileNotFoundException e) {
			System.out.println("\tNo keys file exists.");
		}
		catch (Exception e) {
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
