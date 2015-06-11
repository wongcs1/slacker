__author__ = 'cwong_000'

url = {
    'user_directory' : 'http://localhost',
    'auth'           : 'http://localhost',
    'signup'       : 'http://localhost',
    'messages'       : 'http://meat.stewpot.nz',
    'channels'       : 'http://alexandermcneill.nz',
    'msg_reader'     : 'http://localhost',
    'msg_writer'     : 'http://localhost',
}

port = {
    'user_directory' : 8000,
    'auth'           : 8001,
    'signup'         : 8002,
    'channels'       : 8003,
    'messages'       : 8004,
    'msg_reader'     : 8005,
    'msg_writer'     : 8006,
}

services_path = {
    'User directory'    : '../user_dir',
    'Authentication'    : '../auth',
    'Sign up'           : '../signup',
    'Message service'   : '../msg_service',
    'Channel service'   : '../channel_service',
    'Message reader'    : '../msg_read',
    'Message writer'    : '../msg_writer_svc',
}

services_script_name = {
    'User directory'    : 'user_dir',
    'Authentication'    : 'Authentication',
    'Sign up'           : 'sign_up',
    'Message service'   : 'msg_service',
    'Channel service'   : 'channel_service',
    'Message reader'    : 'msg_read',
    'Message writer'    : 'msg_writer_svc',
}