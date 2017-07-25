import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
public class XMLToJSONBuilder
{
	private static final String PRIMARY_KEY = "nmaprun", ITERABLE_KEY = "host", START_TIME_KEY = "startstr";
	private	static final String ID_FIELD = "nmap_id", CONTENT_FIELD = "content",
								START_FIELD = "start", CLASS_NAME_FIELD = "className", CLASS_NAME_VALUE = "nmap",
								CONTAINER_FIELD = "nmap_data";
	private static final int INDENT_FACTOR = 4;
	private JSONObject json, rawJSON;
	private JSONArray iterable;//depends on the nmap command run, but in the case of nmap -sP 10.0.0.0/24, a list of hosts are returned. Therefore, when the json object is built, the 'host' key is iterated over.
	private String xml, startTime;
	private StringBuilder nmapJSON;
	private  enum JSON_TYPES
	{
		JSON_OBJECT, JSON_STRING, JSON_INT
	}


	public XMLToJSONBuilder(String filePath)
	{
		this.xml = buildXMLString(filePath);
		this.rawJSON = xmlToJSON(xml);
		this.json = this.rawJSON.getJSONObject(PRIMARY_KEY);
		this.startTime = this.json.getString(START_TIME_KEY);
		this.nmapJSON = new StringBuilder();
		try
		{
			this.iterable = this.json.getJSONArray(ITERABLE_KEY);
			buildHostListJSON();
		}
		catch(JSONException e)
		{
			buildSingleHostJSON();
		}
	}

	public XMLToJSONBuilder(String filePath, boolean useRaw)
	{
		this.xml = buildXMLString(filePath);
		this.rawJSON = xmlToJSON(xml);

	}

	public String getRawJSON()
	{
		return this.rawJSON.toString(INDENT_FACTOR);
	}

	private String buildXMLString(String filePath)
	{
	    StringBuilder xml = new StringBuilder();
	    BufferedReader br = null;
	    String line;

	    try
	    {
	    	br = new BufferedReader(new FileReader(new File(filePath)));
			while((line=br.readLine())!= null)
			{
			    xml.append(line.trim());
			}
	    }
	    catch (Exception e)
	    {
	    	e.printStackTrace();
	    }

	    return xml.toString();
	}

	private JSONObject xmlToJSON(String xml)
	{
	   return XML.toJSONObject(xml);
	}

	public String getNmapJSON()
	{
		return new JSONObject(new JSONTokener(this.nmapJSON.toString())).getJSONArray(CONTAINER_FIELD).toString(INDENT_FACTOR);
	}

	private void buildHostListJSON()
	{
		    boolean appendEndStringWithComma;
		    String endString, data;

		    System.out.println("Building nmap json file...");

		    this.nmapJSON.append("{\"" + CONTAINER_FIELD + "\":[");

		    for(int i = 0; i < this.iterable.length(); i++)
		    {
		    	appendEndStringWithComma = i < this.iterable.length() - 1;
			    data = this.iterable.getJSONObject(i).toString();

				this.nmapJSON.append("{" + (appendKeyValuePair(ID_FIELD, (i+1),JSON_TYPES.JSON_INT)));
				this.nmapJSON.append(",");
				this.nmapJSON.append((appendKeyValuePair(CONTENT_FIELD, data,JSON_TYPES.JSON_OBJECT)));
				this.nmapJSON.append(",");
				this.nmapJSON.append((appendKeyValuePair(START_FIELD, this.startTime,JSON_TYPES.JSON_STRING)));
				this.nmapJSON.append(",");
				this.nmapJSON.append((appendKeyValuePair(CLASS_NAME_FIELD, CLASS_NAME_VALUE, JSON_TYPES.JSON_STRING)));
				endString = (appendEndStringWithComma ? "}, " : "}");

				this.nmapJSON.append(endString);
		    }

		this.nmapJSON.append("]}");
		System.out.println("Done.");
	}

	private void buildSingleHostJSON()
	{
		String host = this.json.getJSONObject("host").toString();

		System.out.println("Building nmap json file...");

		this.nmapJSON.append("{\"" + CONTAINER_FIELD + "\":[");
		this.nmapJSON.append("{" + (appendKeyValuePair(ID_FIELD, (1),JSON_TYPES.JSON_INT)));
		this.nmapJSON.append(",");
		this.nmapJSON.append((appendKeyValuePair(CONTENT_FIELD, host,JSON_TYPES.JSON_OBJECT)));
		this.nmapJSON.append(",");
		this.nmapJSON.append((appendKeyValuePair(START_FIELD, this.startTime,JSON_TYPES.JSON_STRING)));
		this.nmapJSON.append(",");
		this.nmapJSON.append((appendKeyValuePair(CLASS_NAME_FIELD, CLASS_NAME_VALUE, JSON_TYPES.JSON_STRING)));
		this.nmapJSON.append("}");
		this.nmapJSON.append("]}");

		System.out.println("Done...");
	}

	private String appendKeyValuePair(String key, Object value, JSON_TYPES type)
	{
	    switch(type)
	    {
	    	case JSON_INT : return "\"" + key + "\":" + (int)value;
	    	case  JSON_OBJECT:  return "\"" + key + "\":" + (String)value;
	    	case JSON_STRING: return "\"" + key + "\":" + "\"" + (String)value + "\"";
	    	default:  return "\"" + key + "\":" + "\"" + (String)value + "\"" ;
	    }
	}
	
}
