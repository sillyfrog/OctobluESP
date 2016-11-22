
#ifndef OctobluESP_h
#define OctobluESP_h
#include "OctobluESP.h"
#include "Arduino.h"
#include <ESP8266WiFi.h>

#define MAX_FUNCTIONS 6
#define PING_INTERVAL 5*60*1000
#define RESPONSE_TIMEOUT 60*1000

class Octoblu
{
    public:
        Octoblu(char *uuid, char *token);
        void registerFunction(void (*func)(String), String name);
        void eventsLoop();
        /*
         * method: the HTTP method, eg: "GET", "PATCH", "POST"
         * path: the HTTP path, eg: "/v2/devices/"
         * contentType: maybe blank for "text/plain", otherwise 
         *      eg: "application/json"
         * content: The body of the request, maybe empty. If not empty the 
         *      Content-Length header will be set. */
        String httpRequest(String method, String path, String contentType, 
            String content);
        void bringOnline(void);
        void bringOffline(void);
        void broadcastMessage(String message);
        void updateThing(String payload);
    private:
        void (*_functions[MAX_FUNCTIONS]) (String param);
        String _functionNames[MAX_FUNCTIONS];
        void fireFunction(String funcName, String input);
        int _functionCount;
        void updateFunctionList(void);
        WiFiClient xmppclient;
        WiFiClient httpclient;
        unsigned long nextping = 0;
        String readUntil(String terminator);
        void sendAuthDetails(void);
        void subscribe(void);
        char *_uuid;
        char *_token;
        bool _updateRegisteredFunctions = false;
        bool _bringOnline = true;
        void _request(String jobType, String json);

};

#endif
