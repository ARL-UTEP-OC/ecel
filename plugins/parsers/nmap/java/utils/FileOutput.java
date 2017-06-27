package utils;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
 
public class FileOutput {
	public static void WriteToFile(String filename, String content) {
		try {
 
			File file = new File(filename);
 
			// if file doesnt exists, then create it
			if (!file.exists()) {
				file.createNewFile();
			}
 
			FileWriter fw = new FileWriter(file.getAbsoluteFile(), false);
			BufferedWriter bw = new BufferedWriter(fw);
			bw.append(content);
			bw.close();
 
			//System.out.println("Done writing to " + filename);
 
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
}
