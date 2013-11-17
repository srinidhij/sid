import web
        
urls = (
    '/(.*)', 'hello'
)
app = web.application(urls, globals())

class hello:        
    def GET(self, name):
        if not name: 
            name = 'World'
        #return 'Hello, ' + name + '!'
	return web.ctx['env']['REMOTE_ADDR'] + ':' + web.ctx['env']['REMOTE_PORT'];

if __name__ == "__main__":
    app.run()
