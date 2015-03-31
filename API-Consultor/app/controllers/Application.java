package controllers;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import org.json.*;


import play.mvc.*;
import views.html.*;

public class Application extends Controller {

    public static Result index() {
        return ok(index.render("API CONSULTOR is ready."));
    }
    
    public static Result prueba(){
    	return ok("Todo esta perfecto");
    }
    
    public static Result consulta(String marca , String modelo , String anio){
    	
    	Result respuesta = null;
    	String resp = "";
    	
    	JSONObject ult = new JSONObject();
    	try  {
            String url = "https://api.edmunds.com/"+"api/vehicle/v2/"+marca+"/"+modelo+"/"+anio+"/styles"+"?view=full&fmt=json&api_key=6zca5s7tcwmd53pjdbn7tqzw";
            URL obj = new URL(url);
    		HttpURLConnection con = (HttpURLConnection) obj.openConnection();
    		con.setRequestMethod("GET");
    		int responseCode = con.getResponseCode();
    		
    		BufferedReader in = new BufferedReader(
    		        new InputStreamReader(con.getInputStream()));
    		String inputLine;
    		StringBuffer response = new StringBuffer();
     
    		while ((inputLine = in.readLine()) != null) {
    			response.append(inputLine);
    		}
    		in.close();

    		
    		resp = response.toString();
    		
    		
    		
    		// obtenemos info del JSON de edmunds
    		
    		try {
				JSONObject json = new JSONObject(resp);
				
				
				
			JSONArray ar = 	json.optJSONArray("styles");
			
			boolean automatico = false;
			
			boolean manual = false;
			
			double promedio = 0;
			
			int maxPuertas = 0;
			
			int maxColores = 0;
			
			int maxVelocidades = 0;
		
			double max = 0;
			
			double min = Double.POSITIVE_INFINITY;
			
			double maxHorsePower = 0;
			
			String motor = "";
			
			String id = "";
			
			for (int i = 0; i < ar.length() ; i ++){
				JSONObject temp =  (JSONObject)ar.opt(i);
				
				System.out.println(temp);
				
				id = temp.optString("id");
				
				motor = temp.optJSONObject("engine").optString("type");
				
				// obtenemos max , min , promedio , numPuertas , colores
				double horse = temp.optJSONObject("engine").optDouble("horsepower");
				if(horse > maxHorsePower){
					maxHorsePower = horse;
				}
				
				
				int speeds = temp.optJSONObject("transmission").optInt("numberOfSpeeds");
				if(speeds > maxVelocidades){
					maxVelocidades = speeds;
				}
				
				String trans = temp.optJSONObject("transmission").optString("transmissionType");
				if(trans.equals("AUTOMATIC")){
					automatico = true;
				}else {
					manual = true;
				}
				
				int col = temp.optJSONArray("colors").length();
				if(col > maxColores){
					maxColores = col;
				}
				
				int pu = temp.optInt("numOfDoors");
				if(pu > maxPuertas){
					maxPuertas = pu;
				}
				
				double precio = temp.optJSONObject("price").optDouble("baseMSRP");
				
				promedio += precio;
				
				if(precio > max ){
					max = precio;
				}
				
				if(precio < min ){
					min = precio;
				}
			}
			
			promedio = promedio/ ar.length();
			
			ult.append("id", id);
			ult.append("automatico",automatico);
			ult.append("manual", manual);
			ult.append("precioPromedio", promedio);
			ult.append("precioMax", max);
			ult.append("precioMin", min);
			ult.append("maxPuertas", maxPuertas);
			ult.append("maxColores", maxColores);
			ult.append("maxVelocidades", maxVelocidades);
			ult.append("maxHP", maxHorsePower);
			ult.append("motor", motor);
			
			
			} catch (JSONException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
    		

        } catch (IOException ex) {
        }
    	
    	return ok(ult.toString());
    	
   // 	return ok("La marca del carro es "+marca + "\n  El modelo es "+ modelo +
    //			" \n  y el anio es " + anio);
    }
}
