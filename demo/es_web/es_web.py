#-*-coding:utf-8-*-
import web
from search_kafka_demo import key_search
import search_kafka_demo
from web import form

render = web.template.render("/usr/local/lib/python2.7/dist-packages/web/templates", globals={"m1":search_kafka_demo})

urls = (
    '/', 'textindex',
    "/search",'textindex',
)
app = web.application(urls, globals())

search = form.Form(
    form.Textbox(id="index",name='index:',size=43,algin='center'),
    form.Textbox(id="keywords",name='keywords:',size=43,algin='center'),
    form.Button(id='search',name='search',action='search',type='submit')
)

class textindex:
    def GET(self):
        f = search()
        return render.test1(f)

    def POST(self):
        f = search()
        #index=web.input(id='index')
        #keywords=web.input(id='keywords')
        #print f['index'].value, f['keywords'].value
        #print index, keywords
        if not f.validates():
            return render.test2(f)

        else:
            #print f['index'].value, f['keywords'].value
            #key_search(index, keywords)
            return render.test2(f)



if __name__ == "__main__":
    web.internalerror = web.debugerror

    app.run()