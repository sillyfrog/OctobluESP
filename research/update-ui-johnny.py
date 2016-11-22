#!/usr/bin/env python

import requests
import os

UUID = os.environ['UUID']
TOKEN = os.environ['TOKEN']

def main():
    print "sending..."
    req = requests.patch('https://meshblu.octoblu.com/v2/devices/'+UUID,
            headers={
                "meshblu_auth_uuid":UUID,
                "meshblu_auth_token":TOKEN
            },
        json=SCHEMA)
    print req.text


SCHEMA = {
   "schemas" : {
      "form" : {
         "message" : {
            "AnalogWrite" : {
               "angular" : [
                  "data.component",
                  "data.value"
               ]
            },
            "DigitalWrite" : {
               "angular" : [
                  "data.component",
                  "data.state"
               ]
            },
            "LcdPcf8574A" : {
               "angular" : [
                  "data.component",
                  "data.text"
               ]
            },
            "Esc" : {
               "angular" : [
                  "data.component",
                  "data.speed"
               ]
            },
            "LcdJhd1313M1" : {
               "angular" : [
                  "data.component",
                  "data.text"
               ]
            },
            "ServoContinuous" : {
               "angular" : [
                  "data.component",
                  "data.direction"
               ]
            },
            "Servo" : {
               "angular" : [
                  "data.component",
                  "data.servo_action",
                  "data.sweep",
                  "data.to_value"
               ]
            },
            "Oled" : {
               "angular" : [
                  "data.component",
                  "data.text"
               ]
            }
         },
         "configure" : {
            "Default" : {
               "angular" : [
                  "options.autoDetect",
                  "options.port",
                  "options.interval",
                  {
                     "add" : "Add Component",
                     "style" : {
                        "add" : "btn-success"
                     },
                     "key" : "options.components",
                     "items" : [
                        "options.components[].name",
                        "options.components[].action",
                        {
                           "condition" : "model.options.components[arrayIndex].action==\"digitalRead\" || model.options.components[arrayIndex].action==\"digitalWrite\" || model.options.components[arrayIndex].action==\"analogRead\" || model.options.components[arrayIndex].action==\"analogWrite\" || model.options.components[arrayIndex].action==\"servo\" || model.options.components[arrayIndex].action==\"esc\"",
                           "key" : "options.components[].pin"
                        },
                        {
                           "key" : "options.components[].address",
                           "condition" : "model.options.components[arrayIndex].action==\"oled-i2c\" || model.options.components[arrayIndex].action==\"LCD-PCF8574A\" || model.options.components[arrayIndex].action==\"LCD-JHD1313M1\" || model.options.components[arrayIndex].action==\"PCA9685-Servo\""
                        }
                     ]
                  }
               ]
            }
         }
      },
      "message" : {
         "DigitalWrite" : {
            "required" : [
               "metadata"
            ],
            "x-group-name" : "I/O",
            "title" : "Digital Write",
            "x-form-schema" : {
               "angular" : "message.DigitalWrite.angular"
            },
            "x-response-schema" : "DigitalWrite",
            "type" : "object",
            "properties" : {
               "metadata" : {
                  "type" : "object",
                  "properties" : {
                     "jobType" : {
                        "type" : "string",
                        "enum" : [
                           "DigitalWrite"
                        ],
                        "default" : "DigitalWrite"
                     },
                     "respondTo" : {}
                  },
                  "required" : [
                     "jobType"
                  ]
               },
               "data" : {
                  "required" : [
                     "component"
                  ],
                  "type" : "object",
                  "properties" : {
                     "state" : {
                        "type" : "string",
                        "enum" : [
                           "1",
                           "0"
                        ]
                     },
                     "component" : {
                        "type" : "string",
                        "title" : "Component Name",
                        "description" : "Configure your device to add components"
                     }
                  }
               }
            }
         },
         "AnalogWrite" : {
            "required" : [
               "metadata"
            ],
            "x-group-name" : "I/O",
            "title" : "Analog Write",
            "x-response-schema" : "AnalogWrite",
            "x-form-schema" : {
               "angular" : "message.AnalogWrite.angular"
            },
            "type" : "object",
            "properties" : {
               "data" : {
                  "type" : "object",
                  "properties" : {
                     "value" : {
                        "type" : "number"
                     },
                     "component" : {
                        "title" : "Component Name",
                        "type" : "string",
                        "description" : "Configure your device to add components"
                     }
                  },
                  "required" : [
                     "component"
                  ]
               },
               "metadata" : {
                  "type" : "object",
                  "properties" : {
                     "respondTo" : {},
                     "jobType" : {
                        "enum" : [
                           "AnalogWrite"
                        ],
                        "default" : "AnalogWrite",
                        "type" : "string"
                     }
                  },
                  "required" : [
                     "jobType"
                  ]
               }
            }
         },
         "LcdPcf8574A" : {
            "x-response-schema" : "LcdPcf8574A",
            "x-form-schema" : {
               "angular" : "message.LcdPcf8574A.angular"
            },
            "properties" : {
               "metadata" : {
                  "required" : [
                     "jobType"
                  ],
                  "properties" : {
                     "jobType" : {
                        "default" : "LcdPcf8574A",
                        "enum" : [
                           "LcdPcf8574A"
                        ],
                        "type" : "string"
                     },
                     "respondTo" : {}
                  },
                  "type" : "object"
               },
               "data" : {
                  "required" : [
                     "component"
                  ],
                  "type" : "object",
                  "properties" : {
                     "text" : {
                        "type" : "string"
                     },
                     "component" : {
                        "description" : "Configure your device to add components",
                        "title" : "Component Name",
                        "type" : "string"
                     }
                  }
               }
            },
            "type" : "object",
            "title" : "LCD-PCF8574A",
            "x-group-name" : "Display",
            "required" : [
               "metadata"
            ]
         },
         "Esc" : {
            "required" : [
               "metadata"
            ],
            "x-group-name" : "Motor Control",
            "title" : "ESC",
            "x-form-schema" : {
               "angular" : "message.Esc.angular"
            },
            "x-response-schema" : "Esc",
            "type" : "object",
            "properties" : {
               "metadata" : {
                  "required" : [
                     "jobType"
                  ],
                  "type" : "object",
                  "properties" : {
                     "respondTo" : {},
                     "jobType" : {
                        "type" : "string",
                        "enum" : [
                           "Esc"
                        ],
                        "default" : "Esc"
                     }
                  }
               },
               "data" : {
                  "required" : [
                     "component"
                  ],
                  "type" : "object",
                  "properties" : {
                     "component" : {
                        "description" : "Configure your device to add components",
                        "type" : "string",
                        "title" : "Component Name"
                     },
                     "speed" : {
                        "type" : "number"
                     }
                  }
               }
            }
         },
         "ServoContinuous" : {
            "title" : "Continuous Servo",
            "x-response-schema" : "ServoContinuous",
            "type" : "object",
            "x-form-schema" : {
               "angular" : "message.ServoContinuous.angular"
            },
            "properties" : {
               "metadata" : {
                  "type" : "object",
                  "properties" : {
                     "jobType" : {
                        "enum" : [
                           "ServoContinuous"
                        ],
                        "default" : "ServoContinuous",
                        "type" : "string"
                     },
                     "respondTo" : {}
                  },
                  "required" : [
                     "jobType"
                  ]
               },
               "data" : {
                  "properties" : {
                     "component" : {
                        "type" : "string",
                        "title" : "Component Name",
                        "description" : "Configure your device to add components"
                     },
                     "direction" : {
                        "enum" : [
                           "CW",
                           "CCW",
                           "STOP"
                        ],
                        "title" : "Direction",
                        "type" : "string"
                     }
                  },
                  "type" : "object",
                  "required" : [
                     "component"
                  ]
               }
            },
            "x-group-name" : "Motor Control",
            "required" : [
               "metadata"
            ]
         },
         "LcdJhd1313M1" : {
            "x-group-name" : "Display",
            "required" : [
               "metadata"
            ],
            "properties" : {
               "metadata" : {
                  "required" : [
                     "jobType"
                  ],
                  "type" : "object",
                  "properties" : {
                     "respondTo" : {},
                     "jobType" : {
                        "default" : "LcdJhd1313M1",
                        "enum" : [
                           "LcdJhd1313M1"
                        ],
                        "type" : "string"
                     }
                  }
               },
               "data" : {
                  "properties" : {
                     "text" : {
                        "type" : "string"
                     },
                     "component" : {
                        "description" : "Configure your device to add components",
                        "type" : "string",
                        "title" : "Component Name"
                     }
                  },
                  "type" : "object",
                  "required" : [
                     "component"
                  ]
               }
            },
            "x-response-schema" : "LcdJhd1313M1",
            "x-form-schema" : {
               "angular" : "message.LcdJhd1313M1.angular"
            },
            "type" : "object",
            "title" : "LCD-JHD1313M1"
         },
         "Servo" : {
            "type" : "object",
            "x-response-schema" : "Servo",
            "x-form-schema" : {
               "angular" : "message.Servo.angular"
            },
            "properties" : {
               "metadata" : {
                  "properties" : {
                     "respondTo" : {},
                     "jobType" : {
                        "type" : "string",
                        "enum" : [
                           "Servo"
                        ],
                        "default" : "Servo"
                     }
                  },
                  "type" : "object",
                  "required" : [
                     "jobType"
                  ]
               },
               "data" : {
                  "required" : [
                     "component"
                  ],
                  "properties" : {
                     "to_value" : {
                        "x-schema-form" : {
                           "condition" : "model.data.servo_action == \"to\""
                        },
                        "type" : "number",
                        "title" : "To",
                        "description" : "An angle value 0 - 180"
                     },
                     "component" : {
                        "description" : "Configure your device to add components",
                        "type" : "string",
                        "title" : "Component Name"
                     },
                     "servo_action" : {
                        "enum" : [
                           "to",
                           "sweep",
                           "stop"
                        ],
                        "title" : "Function",
                        "type" : "string"
                     },
                     "sweep" : {
                        "x-schema-form" : {
                           "condition" : "model.data.servo_action == \"sweep\""
                        },
                        "properties" : {
                           "min" : {
                              "type" : "number"
                           },
                           "max" : {
                              "type" : "number"
                           }
                        },
                        "type" : "object",
                        "title" : "Sweep"
                     }
                  },
                  "type" : "object"
               }
            },
            "title" : "Servo",
            "x-group-name" : "Motor Control",
            "required" : [
               "metadata"
            ]
         },
         "Oled" : {
            "x-response-schema" : "Oled",
            "properties" : {
               "metadata" : {
                  "required" : [
                     "jobType"
                  ],
                  "properties" : {
                     "respondTo" : {},
                     "jobType" : {
                        "type" : "string",
                        "default" : "Oled",
                        "enum" : [
                           "Oled"
                        ]
                     }
                  },
                  "type" : "object"
               },
               "data" : {
                  "properties" : {
                     "text" : {
                        "type" : "string"
                     },
                     "component" : {
                        "description" : "Configure your device to add components",
                        "title" : "Component Name",
                        "type" : "string"
                     }
                  },
                  "type" : "object",
                  "required" : [
                     "component"
                  ]
               }
            },
            "x-form-schema" : {
               "angular" : "message.Oled.angular"
            },
            "type" : "object",
            "title" : "OLED XXXX",
            "x-group-name" : "Display",
            "required" : [
               "metadata"
            ]
         }
      },
      "response" : {
         "Esc" : {
            "properties" : {
               "metadata" : {
                  "properties" : {
                     "code" : {
                        "type" : "integer"
                     },
                     "status" : {
                        "type" : "string"
                     }
                  },
                  "type" : "object",
                  "required" : [
                     "status",
                     "code"
                  ]
               }
            }
         },
         "DigitalWrite" : {
            "properties" : {
               "metadata" : {
                  "required" : [
                     "status",
                     "code"
                  ],
                  "type" : "object",
                  "properties" : {
                     "code" : {
                        "type" : "integer"
                     },
                     "status" : {
                        "type" : "string"
                     }
                  }
               }
            }
         },
         "AnalogWrite" : {
            "properties" : {
               "metadata" : {
                  "properties" : {
                     "status" : {
                        "type" : "string"
                     },
                     "code" : {
                        "type" : "integer"
                     }
                  },
                  "type" : "object",
                  "required" : [
                     "status",
                     "code"
                  ]
               }
            }
         },
         "LcdPcf8574A" : {
            "properties" : {
               "metadata" : {
                  "required" : [
                     "status",
                     "code"
                  ],
                  "properties" : {
                     "code" : {
                        "type" : "integer"
                     },
                     "status" : {
                        "type" : "string"
                     }
                  },
                  "type" : "object"
               }
            }
         },
         "Servo" : {
            "properties" : {
               "metadata" : {
                  "type" : "object",
                  "properties" : {
                     "code" : {
                        "type" : "integer"
                     },
                     "status" : {
                        "type" : "string"
                     }
                  },
                  "required" : [
                     "status",
                     "code"
                  ]
               }
            }
         },
         "Oled" : {
            "properties" : {
               "metadata" : {
                  "type" : "object",
                  "properties" : {
                     "code" : {
                        "type" : "integer"
                     },
                     "status" : {
                        "type" : "string"
                     }
                  },
                  "required" : [
                     "status",
                     "code"
                  ]
               }
            }
         },
         "LcdJhd1313M1" : {
            "properties" : {
               "metadata" : {
                  "required" : [
                     "status",
                     "code"
                  ],
                  "properties" : {
                     "status" : {
                        "type" : "string"
                     },
                     "code" : {
                        "type" : "integer"
                     }
                  },
                  "type" : "object"
               }
            }
         },
         "ServoContinuous" : {
            "properties" : {
               "metadata" : {
                  "required" : [
                     "status",
                     "code"
                  ],
                  "type" : "object",
                  "properties" : {
                     "code" : {
                        "type" : "integer"
                     },
                     "status" : {
                        "type" : "string"
                     }
                  }
               }
            }
         }
      },
      "configure" : {
         "Default" : {
            "title" : "Default Configuration",
            "x-form-schema" : {
               "angular" : "configure.Default.angular"
            },
            "type" : "object",
            "properties" : {
               "options" : {
                  "properties" : {
                     "port" : {
                        "type" : "string",
                        "description" : "The serial port your board is on",
                        "required" : False,
                        "default" : "/dev/ttyACM0"
                     },
                     "autoDetect" : {
                        "default" : True,
                        "title" : "Auto Detect Port?",
                        "type" : "boolean"
                     },
                     "components" : {
                        "items" : {
                           "type" : "object",
                           "properties" : {
                              "name" : {
                                 "description" : "Name this component anything you like. (i.e Left_Motor). Sensor output will show up under this name in payload",
                                 "required" : True,
                                 "type" : "string",
                                 "title" : "Name"
                              },
                              "pin" : {
                                 "title" : "Pin",
                                 "type" : "string",
                                 "description" : "Pin used for this component",
                                 "required" : False
                              },
                              "action" : {
                                 "required" : True,
                                 "enum" : [
                                    "digitalWrite",
                                    "digitalRead",
                                    "analogWrite",
                                    "analogRead",
                                    "servo",
                                    "servo-continuous",
                                    "PCA9685-Servo",
                                    "oled-i2c",
                                    "LCD-PCF8574A",
                                    "LCD-JHD1313M1",
                                    "MPU6050",
                                    "esc"
                                 ],
                                 "title" : "Action",
                                 "type" : "string"
                              },
                              "address" : {
                                 "title" : "address",
                                 "type" : "string",
                                 "required" : False,
                                 "description" : "i2c address used for this component"
                              }
                           },
                           "required" : [
                              "name",
                              "action"
                           ]
                        },
                        "type" : "array"
                     },
                     "interval" : {
                        "required" : False,
                        "description" : "The Interval in milliseconds to send Sensor readings.",
                        "enum" : [
                           "200",
                           "500",
                           "1000",
                           "1500",
                           "2000"
                        ],
                        "default" : "500",
                        "type" : "string"
                     }
                  },
                  "type" : "object",
                  "title" : "Options"
               }
            }
         }
      },
      "version" : "2.0.0"
   }
}


if __name__ == '__main__':
    main()

