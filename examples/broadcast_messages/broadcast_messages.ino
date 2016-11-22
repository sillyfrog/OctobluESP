#include <ESP8266WiFi.h>
#include <OctobluESP.h>

char ssid[] = "...";  //  your network SSID (name)
char pass[] = "...";       // your network password

/*
 Get this info in Octoblu by doing the following:
    * Login at https://app.octoblu.com
    * Got go "Things" > All Things
    * Find "Generic Thing", and click on it.
    * "Connect" it, give it a name and a type, this can be anything.
    * In My Things click on the Thing just created, here you can see the UUID
    * Then click on "Generate Token" and record the Token!
    * Update the values below
    * You can then add the Thing you have created to your Flows. */
char uuid[] = "...";    // The UUID of your Thing
char token[] = "...";   // The Token for your Thing

Octoblu octoblu = Octoblu(uuid, token);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  Serial.println(".");
  
  WiFi.begin(ssid, pass);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");  
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  // put your main code here, to run repeatedly:

  delay(500);
  Serial.print('.');
  octoblu.eventsLoop();

  octoblu.broadcastMessage("{\"somevalue\": 99}");
}

