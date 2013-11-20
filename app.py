import web
from utils import LoadBalancer as LB
import requests
import time
import json

lb = LB(3)
        
urls = (
    '/', 'home',
    '/getInfo', 'getInfo',
    '/addNode', 'addNode',
    '/delNode', 'delNode'
)
app = web.application(urls, globals())

render = web.template.render('templates')
class home:        
    def GET(self):
        global render
        return render.index()

class getInfo:
    def GET(self):
        web.header('Content-Type', 'application/json')
        return json.dumps(lb.stats())

class addNode:
    def GET(self):
        lb.newuser()
        web.header('Content-Type', 'application/json')
        return json.dumps(lb.stats())

class delNode:
    def GET(self):
        user_data = web.input()
        if 'user' in user_data.userid:
            lb.remuser(int(user_data.userid.replace('user','')))
        web.header('Content-Type', 'application/json')
        return json.dumps(lb.stats())

if __name__ == "__main__":
    app.run()
