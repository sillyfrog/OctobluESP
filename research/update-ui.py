#!/usr/bin/env python

import requests
import os

UUID = os.environ['UUID']
TOKEN = os.environ['TOKEN']

def main():
    print "sending..."
    req = requests.patch('http://meshblu.octoblu.com/v2/devices/'+UUID,
            headers={
                "meshblu_auth_uuid":UUID,
                "meshblu_auth_token":TOKEN
            },
        json=SCHEMA)
    print req.text


SCHEMA = {
   "schemas" : {
      "version" : "2.0.0",
      "form" : {
         "main" : {
          "required" : [
                     "input",
                     "function",
          ],
          "type" : "object",
        },
      },
      "response" : {
         "main" : {
            "properties" : {
                  "required" : [
                     "function",
                     "input",
                  ],
                  "type" : "object",
                  "properties" : {
                     "function" : {
                        "type" : "string"
                     },
                     "input" : {
                        "type" : "string"
                     }
                  }
               }
         },
      },
      "message" : {
         "main" : {
            "required" : [
               "function"
            ],
            "type" : "object",
            "properties" : {
                     "input" : {
                        "type" : "string",
                        "title" : "Input",
                        "description" : "Input to pass to the function"
                     },
                     "function" : {
                        "type" : "string",
                        "title" : "Function Name",
                        "description" : "Select the function to call",
                        "enum" : [
                           "FirstFunc",
                           "NextFunc"
                        ]
                     },
            }
         },
      },
   }
}


if __name__ == '__main__':
    main()

