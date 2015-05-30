def msg_response(response_message, response_code, messages=None):
    r_dict = { 
            "msg_read_response" : {
                "response_message" : response_message,
                "response_code": response_code, },
            "messages": messages,
            }
    return r_dict

        
