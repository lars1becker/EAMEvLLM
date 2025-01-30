from code_editor import code_editor 

def get_code_editor(code):
    custom_btns = [{
        "name": "Copy",
        "feather": "Copy",
        "hasText": True,
        "alwaysOn": True,
        "commands": ["copyAll", 
                     ["infoMessage", 
                      {
                       "text":"Copied to clipboard!",
                       "timeout": 2500, 
                       "classToggle": "show"
                      }
                     ]
                    ],
        "style": {"right": "0.4rem"}
        },
        {
          "name": "Save",
          "feather": "Save",
          "primary": True,
          "hasText": True,
          "alwaysOn": True,
          "showWithIcon": True,
          "commands": ["submit"],
          "style": {"right": "5.4rem"}
        },
    ]
    css_string = '''
    background-color: #bee1e5;

    body > #root .ace-streamlit-dark~& {
       background-color: #262830;
    }

    .ace-streamlit-dark~& span {
       color: #fff;
       opacity: 0.6;
    }

    span {
       color: #000;
       opacity: 0.5;
    }

    .code_editor-info.message {
       width: inherit;
       margin-right: 75px;
       order: 2;
       text-align: center;
       opacity: 0;
       transition: opacity 0.7s ease-out;
    }

    .code_editor-info.message.show {
       opacity: 0.6;
    }

    .ace-streamlit-dark~& .code_editor-info.message.show {
       opacity: 0.5;
    }
    '''
    # create info bar dictionary
    info_bar = {
      "name": "language info",
      "css": css_string,
      "style": {
                "order": "1",
                "display": "flex",
                "flexDirection": "row",
                "alignItems": "center",
                "width": "100%",
                "height": "2.5rem",
                "padding": "0rem 0.75rem",
                "borderRadius": "8px 8px 0px 0px",
                "zIndex": "9993"
               },
      "info": [{
                "name": "python",
                "style": {"width": "100px"}
               }]
    }

    return code_editor(code=code, buttons=custom_btns, info=info_bar, options={'wrap':True, 'showLineNumbers':True}) 