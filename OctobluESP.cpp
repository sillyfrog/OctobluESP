

#include "OctobluESP.h"
#include <ArduinoJson.h>
#include <rBase64.h>

#define DEBUG
//#undef DEBUG

#ifdef DEBUG
  #define DebugLn(s) Serial.println((s))
  #define Debug(s) Serial.print((s))
#else
  #define DebugLn(s)
  #define Debug(s)
#endif

char uuidhost[] = "meshblu.octoblu.com";

static const char connect_template[] PROGMEM = "<stream:stream xmlns=\"jabber:client\" xmlns:stream=\"http://etherx.jabber.org/streams\" version=\"1.0\" to=\"meshblu.octoblu.com\">";

static const char auth_template1[] PROGMEM = "<auth xmlns=\"urn:ietf:params:xml:ns:xmpp-sasl\" mechanism=\"PLAIN\">";
static const char auth_template2[] PROGMEM = "</auth>";

static const char sub_template1[] PROGMEM = "<iq to=\"meshblu-xmpp.octoblu.com\" type=\"set\" id=\"thissubscription\"><request><metadata><jobType>CreateSubscription</jobType><toUuid>";
static const char sub_template2[] PROGMEM = "</toUuid></metadata><rawData>{\"subscriberUuid\":\"";
static const char sub_template3[] PROGMEM = "\",\"emitterUuid\":\"";
static const char sub_template4[] PROGMEM = "\",\"type\":\"message.received\"}</rawData></request></iq>";

static const char server_ping[] = "<iq to=\"meshblu-xmpp.octoblu.com\" type=\"get\"><request><metadata><jobType>GetStatus</jobType></metadata></request></iq>";

static const char ui_schema_template1[] PROGMEM = R"jsonstring(
{"schemas": {"message": {"main": {"required": ["function"], "type": "object", "properties": {"function": {"enum": [)jsonstring";
static const char ui_schema_template2[] PROGMEM = R"jsonstring(
], "type": "string", "description": "Select the function to call", "title": "Function Name"}, "input": {"type": "string", "description": "Input to pass to the function", "title": "Input"}}}}, "version": "2.0.0", "response": {"main": {"properties": {"required": ["function", "input"], "type": "object", "properties": {"function": {"type": "string"}, "input": {"type": "string"}}}}}, "form": {"main": {"required": ["input", "function"], "type": "object"}}}})jsonstring";

static const char request_template1[] PROGMEM = "<iq to=\"meshblu-xmpp.octoblu.com\" type=\"set\" id=\"";
static const char request_template2[] PROGMEM = "\"><request><metadata><jobType>";
static const char request_template3[] PROGMEM = "</jobType><toUuid>";
static const char request_template4[] PROGMEM = "</toUuid></metadata><rawData>";
static const char request_template5[] PROGMEM = "</rawData></request></iq>";
//static const char update_template3[] PROGMEM = "</toUuid></metadata><rawData>{\"$set\":";
//static const char update_template4[] PROGMEM = "}</rawData></request></iq>";



char meshbluHost[] = "meshblu-xmpp.octoblu.com";

// library interface description
Octoblu::Octoblu(char *uuid, char *token)
{
    _uuid = uuid;
    _token = token;
    _functionCount = 0;
};

void Octoblu::eventsLoop(void) {
  if (!xmppclient.connected()) {
    DebugLn("Reconnecting...");
    xmppclient.connect(meshbluHost, 5222);
    String nextString = String(FPSTR(connect_template));
    xmppclient.println(nextString);
    readUntil("</stream:features>");
    // Now authenticate
    sendAuthDetails();
    readUntil("/>");
    subscribe();
    readUntil("</iq>");
    DebugLn("Connected!");
    nextping = millis() + PING_INTERVAL;
  }

  while (xmppclient.available()) {
    readUntil("<raw-data>");
    String data = xmppclient.readStringUntil('<');
    DynamicJsonBuffer jsonBuffer;
    JsonObject& json = jsonBuffer.parseObject(data);
    if (!json.success()) {
      //Serial.println("JSON parsing failed!");
      return;
    }
    else {
      String payload = json["payload"];
      // I'm not sure why it's in a payload sometimes, but cater for it.
      if (payload.length() > 0) {
        String functionP = json["payload"]["function"];
        String inputP = json["payload"]["input"];
        fireFunction(functionP, inputP);
      } else {
        String function = json["function"];
        String input = json["input"];
        fireFunction(function, input);
      }
    }
    readUntil("age>");
    yield();
  }

  // See if anything else has been scheduled internally
  if (_updateRegisteredFunctions) {
    updateFunctionList();
    _updateRegisteredFunctions = false;
  }
  if (_bringOnline) {
    bringOnline();
    _bringOnline = false;
  }
  if (millis() > nextping) {
    nextping = millis() + PING_INTERVAL;
    xmppclient.println(server_ping);
    readUntil("</iq>");
  }
}

void Octoblu::registerFunction(void (*func)(String), String name) {
    if (_functionCount == MAX_FUNCTIONS) {
        DebugLn("No more room for more functions to be registered");
        return;
    }
    _functions[_functionCount] = func;
    _functionNames[_functionCount] = name;
    _functionCount += 1;
    _updateRegisteredFunctions = true;
}

// Updates the list of functions in the UI on the Octoblu server for this thing
void Octoblu::updateFunctionList(void) {
    String request = String(FPSTR(ui_schema_template1));
    for (int i; i < _functionCount; i++) {
        request += '"' + _functionNames[i] + '"';
        if (i < _functionCount - 1) {
            request += ",";
        }
    }
    request += FPSTR(ui_schema_template2);
    updateThing(request);
}


void Octoblu::fireFunction(String funcName, String input) {
    for (int i; i < _functionCount; i++) {
        if (funcName == _functionNames[i]) {
            Debug("Calling function: " + funcName);
            DebugLn(String("(") + input + ")");
            (*_functions[i])(input);
            return;
        }
    }
    DebugLn("No match found for: " + funcName);
}

void Octoblu::broadcastMessage(String json) {
    json = String("{\"devices\":[\"*\"],\"payload\":") + json + "}"; 
    _request("SendMessage", json);
}

void Octoblu::updateThing(String json) {
    json = String("{\"$set\":") + json + "}"; 
    _request("UpdateDevice", json);
}

void Octoblu::_request(String jobType, String json) {
  String nextString = String(FPSTR(request_template1));
  xmppclient.print(nextString);
  xmppclient.print(_uuid);
  nextString = String(FPSTR(request_template2));
  xmppclient.print(nextString);
  xmppclient.print(jobType);
  nextString = String(FPSTR(request_template3));
  xmppclient.print(nextString);
  xmppclient.print(_uuid);
  nextString = String(FPSTR(request_template4));
  xmppclient.print(nextString);
  xmppclient.print(json);
  nextString = String(FPSTR(request_template5));
  xmppclient.print(nextString);
  DebugLn(readUntil("</iq>"));
}

//<iq to="meshblu-xmpp.octoblu.com" type="set" id="53b28fc0-9e8c-11e6-a18b-9db544b953b8"><request><metadata><jobType>SendMessage</jobType></metadata><rawData>{"devices":["*"],"payload":{"temp":666}}</rawData></request></iq>
//<iq to="meshblu-xmpp.octoblu.com" type="set" id="53b268b0-9e8c-11e6-a18b-9db544b953b8"><request><metadata><jobType>UpdateDevice</jobType><toUuid>f211674b-97e6-490e-9dc4-e61bbb9022b8</toUuid></metadata><rawData>{"$set":{"online":true}}</rawData></request></iq>

void Octoblu::bringOnline() {
    updateThing("{\"online\": true}");
}

void Octoblu::bringOffline() {
    updateThing("{\"online\": false}");
}


String Octoblu::httpRequest(String method, String path, String contentType, 
        String content) {
    if (httpclient.connected()) {
        httpclient.stop();
    }
    httpclient.connect("meshblu.octoblu.com", 80);
    httpclient.println(method + " " + path + " HTTP/1.0");
    httpclient.println(String("meshblu_auth_uuid: ") + _uuid);
    httpclient.println(String("meshblu_auth_token: ") + _token);
    httpclient.println(String("Host: ") + "meshblu.octoblu.com");
    httpclient.println("Connection: close");
    if (contentType.length() == 0) {
        contentType = String("text/plain");
    }
    httpclient.println("Content-Type: " + contentType);
    if (content.length() > 0) {
        httpclient.println(String("Content-Length: ") + content.length());
    }
    httpclient.println();
    httpclient.print(content);
    unsigned long readTimeout = millis() + RESPONSE_TIMEOUT;
    String response = String();
    while (httpclient.connected() and millis() < readTimeout) {
        response += httpclient.readString();
        delay(5);
    }
    return response;
}

String Octoblu::readUntil(String terminator) {
  // Reads from the stream until the terminating tag/string is found
  String data;
  unsigned int prevlength = 0;
  unsigned long readend = millis() + RESPONSE_TIMEOUT;
  char endchar = terminator.charAt(terminator.length()-1);
  while (xmppclient.connected() && millis() < readend) {
    data += xmppclient.readStringUntil(endchar);
    if (data.length() > prevlength) {
      data += endchar;
      prevlength = data.length();
    }
    yield();
    if (data.endsWith(terminator)) {
      nextping = millis() + PING_INTERVAL;
      return data;
    }
  }
  // If we got here, something is wrong, disconnect
  while (xmppclient.available()) {
    xmppclient.read();
  }
  xmppclient.stop();
  data = "";
  return data;
}

void Octoblu::sendAuthDetails() {
  String nextString = String(FPSTR(auth_template1));
  xmppclient.print(nextString);
  int uuidlen = strlen(_uuid);
  int uuidhostlen = strlen(uuidhost);
  int tokenlen = strlen(_token);
  int rawLen = uuidlen + uuidlen + tokenlen + uuidhostlen + 4;
  size_t encodedLen = rbase64_enc_len(rawLen);
  size_t copyPos = 0;
  char raw[rawLen];
  char encoded[encodedLen];
  
  memcpy(raw+copyPos, _uuid, uuidlen);
  copyPos += uuidlen;
  raw[copyPos] = '@';
  copyPos += 1;
  memcpy(raw+copyPos, uuidhost, uuidhostlen);
  copyPos += uuidhostlen;
  raw[copyPos] = '\0';
  copyPos += 1;
  memcpy(raw+copyPos, _uuid, uuidlen);
  copyPos += uuidlen;
  raw[copyPos] = '\0';
  copyPos += 1;
  memcpy(raw+copyPos, _token, tokenlen);
  copyPos += tokenlen;
  raw[copyPos] = '\0';
  
  rbase64_encode(encoded, raw, copyPos);
  
  xmppclient.print(encoded);
  nextString = String(FPSTR(auth_template2));
  xmppclient.println(nextString);
}

void Octoblu::subscribe() {
  String nextString = String(FPSTR(sub_template1));
  xmppclient.print(nextString);
  xmppclient.print(_uuid);
  nextString = String(FPSTR(sub_template2));
  xmppclient.print(nextString);
  xmppclient.print(_uuid);
  nextString = String(FPSTR(sub_template3));
  xmppclient.print(nextString);
  xmppclient.print(_uuid);
  nextString = String(FPSTR(sub_template4));
  xmppclient.print(nextString);
}


