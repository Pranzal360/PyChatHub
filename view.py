from flet import *
from views.login_view import Authentication
from views.register_view import Register
from views.chat_view import ChatScreen
from components.crudinFirebase import logout
def views_handler(page):
    
    return{
        '/':View(
            route='/',
            controls=[
                Authentication(page)
            ]
        ),
        '/signup':View(
            route = '/signup',
            controls= [
                Register(page)
            ]
        ),

        }

    

def chat_handler(page,uid=None,name=None,tokenid=None):
    
    
    def logout(e):
        logout
        page.client_storage.clear()

        page.go('/')
    
    return{
        '/chat': View(
            route='/chat',
            controls=[
                AppBar(title=Text('Sangalo',text_align=TextAlign.CENTER),actions=[
                    IconButton(icon=icons.LOGOUT,on_click=logout)
                ],center_title=True),ChatScreen(page,uid,name,tokenid)
            ]
        )

    }


#     wid = page.window_width
    heig = page.window_height