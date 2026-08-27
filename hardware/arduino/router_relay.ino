 #include <ESP8266WiFi.h>

#include <ESP8266WebServer.h>
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

#define  relay D5

ESP8266WebServer server(80);
    void handleRoot() {

                    server.send(200, "text/plain","READY");
                      }
                      
    void handleOn() {
                     digitalWrite(relay,HIGH);
                    server.send(200, "text/plain","DONE");
                      }
                      
    void handleOff() {
                     digitalWrite(relay,LOW);
                    server.send(200, "text/plain","DONE");
                     }

void setup() {
Serial.begin(115200);

  WiFi.disconnect();
  WiFi.mode(WIFI_STA);
  
  WiFi.begin(ssid, password);


  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());


pinMode(relay,OUTPUT);   
   

digitalWrite(relay,LOW);

  server.on("/", handleRoot);
  server.on("/don",handleOn);  
  server.on("/dof",handleOff);
  server.begin();

}

void loop() {
server.handleClient();
}
