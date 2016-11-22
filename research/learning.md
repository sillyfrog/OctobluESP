# Connecting to Octoblu using an ESP8266

Below are my notes from my testing and what I have learnt trying to connect with octoblu.com. The solution looks pretty cool - I'm concerned Citrix is going to let it die, but thought I would try and connect to it anyway and using it while I can, primarily using an ESP8266, coded and programmed using the Arduino IDE.

## Getting events into and from Octoblue/meshblu

This page https://developer.octoblu.com/ has an overview of how everything ties together - but I couldn't find much info as to how to actually make events/input/output happen with "Things".

The solution that I have found to work (so far) is using an "Generic Thing". After signing up to Octoblu, do the following:
- Click on "Things" at the top, then "All Things"
- Search for "Generic", and click "Generic Thing"
- Connect the generic device
- Register a "New thing", and give it a Name and a Type (I use esp8266 for the type)
- Once registered, in the list of "My Things", find the thing just created and click on it
- Now record the UUID, and click "Generate Token", and record the token.

That should be all on the Octoblu side.

## Interacting with your Thing

Once I had the Thing created, trying to get events to and from it and actually get the Flow to trigger was not working for right away, after much messing around and looking at various documents, I _think_ this is the "correct" way. This is the most relevant document here: https://meshblu-http.readme.io/ . You need **both** v1 and v2 of the API to make things work.

For example, in a bash/command line prompt, assuming the following set up (I use a Mac, it should work on Linux as well, not exactly sure how to do in Windows, I expect it would be similar):

```
export UUID=f211...
export TOKEN=94e5...
```
(Obviously put the UUID and Token copied earlier in the above, be sure to have them the correct way around!)

To found out about the device, and make sure things are working, use `whoamid`:
```
curl --header "meshblu_auth_uuid: $UUID" --header "meshblu_auth_token: $TOKEN" https://meshblu.octoblu.com/v2/whoami
```

To see _everything_ happening with the Thing, in real time:
```
curl --header "meshblu_auth_uuid: $UUID" --header "meshblu_auth_token: $TOKEN" https://meshblu-http-streaming.octoblu.com/subscribe/
```

To see just stuff you likely care about (i.e.: incoming events):
```
curl --header "meshblu_auth_uuid: $UUID" --header "meshblu_auth_token: $TOKEN" https://meshblu-http-streaming.octoblu.com/subscribe/$UUID/received
```

To update the state of the device, for example to bring it "Online" (if it's offline, it is greyed out in "My Things" and the device will report Offline when you click on it. I'm not sure if this actually matters):
```
curl --header "meshblu_auth_uuid: $UUID" --header "meshblu_auth_token: $TOKEN" --header "Content-Type: application/json" --request PATCH https://meshblu.octoblu.com/v2/devices/$UUID --data '{"online":true}'
```

To trigger the Thing, with some actual data, which will be passed to the flow and connected Things:
```
curl --header "meshblu_auth_uuid: $UUID" --header "meshblu_auth_token: $TOKEN" --request POST --header "Content-Type: application/json" https://meshblu.octoblu.com/broadcasts --data '{"payload": {"foo":"some bar"}}'
```
Best I can tell, having the actual data in the `payload` property (rather than just in the base) is the right thing to do - but I didn't see any official documentation on that. The documentation is here: https://meshblu-http.readme.io/docs/broadcasts this link is not in the sidebar on readme.io!

If you had the Thing in a Flow, with a "Debug" Thing attached, you would see that object in the JSON in the debug tab in Octoblu.


## Configuring the Thing

Once the above is done you may want to allow the Thing to be configured. From research and bumping around the internet, I figured out that the Things in the UI use Angular Schema http://schemaform.io/ . I think it's an old version and/or it's modified. I didn't spend a lot of time understanding it, but if you look in the examples at `update-ui.py` you can see what this schema looks like (this is a Python object that's converted to JSON). If you run `update-ui.py` with the same environment as setup above, and then go to your flow with the thing, you will see you now have options to configure a couple of items. There is also an example called `update-ui-johnny.py`, this has the schema I extracted from a Johnny-Five Thing - it's considerably more complex, and also covers fields on the Configure screen.

These Python scripts are just using the PATCH method mentioned above, updating the `schema` key, but because the JSON is so big, I found editing it easier in a big file and running it with Python.

# Getting Events on the ESP

The next challenge was getting these events/messages on the ESP as they came through. Using the subscribe methods above works, however I found the HTTP session length was just 2 minutes of no activity, at which point it would drop out and have to reconnect.

I looked at a number of other options:
- CoAP: Looked promising, but I could not actually get it to see any incoming events, plus as it's UDP, unless the firewall has a uncommon very long connection tracking cache time, the return event packets won't make it back in.
- MQTT: I could not get this to subscribe to events either.
- XMPP: This is what I settled on, generating raw XMPP packets in the ESP, and with some artificial "ping" packets, the connection stays alive, which is great. This is what's included in this repo.

## Getting Events via XMPP

After some testing with telnet/netcat, I have what I think is a minimal set of XMPP commands to connect to the remote server, and subscribe to a channel. The file `xmpp-test.py` shows where I got to, and what I'm actually using in the code.

From here, when a command comes in, it can then call the registered function with the passed input and do what ever action it needs to.

