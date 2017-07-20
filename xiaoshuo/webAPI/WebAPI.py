import web
from . import model



urls= (
    '/','Index',
    '/Search(/d+)','Search'
)

render = web.template.render('templates/',cache = False)

qqq
#首页
class Index:
    def GET(self):
        posts = model.get_all()
        return render.index(posts)




class Search:
    def GET(self,id):
        posts = model.get_chapter(id)
        return render.search(posts)


#查找页