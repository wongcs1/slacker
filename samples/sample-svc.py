import cherrypy

datalist = [{'item': 0, 'foo': 'bar'}]

class DataListWebService:
    exposed = True

    @cherrypy.tools.json_out()
    def GET(self, item):
        item = int(item)
        try:
	    return datalist[item]
	except IndexError:
	    return {'error': 'no such item'}

    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in() 
    def POST(self):
        to_store = cherrypy.request.json
        to_store['item'] = len(datalist) 
        datalist.append(to_store)
	return {'item': to_store['item'] }

    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in() 
    def PUT(self):
        try:
            to_update = cherrypy.request.json
            item = to_update['item']
	    datalist[item] = to_update
	    return to_update 
	except IndexError:
	    return {'error': 'no such item'}

    @cherrypy.tools.json_out()
    def DELETE(self, item):
        try:
            item = int(item)
            datalist[item] = None
        except IndexError:
            # if asked to delete a nonexistent item, don't
            # sweat it
            pass
        finally:
            return {'item': item, 'deleted': True}


if __name__ == '__main__':
    conf = {
        '/' : {
	    'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
	    'tools.response_headers.on': True,
	    'tools.response_headers.headers': [('Content-Type', 'application/json')],
	    }
	  }
    cherrypy.config.update({'server.socket_port' : 8000})
    cherrypy.quickstart(DataListWebService(), '/', conf)
