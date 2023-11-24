from flet import *

from view import views_handler, chat_handler
from color_settings import *
from crudinFirebase import get_refresh_token, logout
from flet import Page 

def main(page: Page):
    page.window_maximized = True
    page.window_resizable = False
    page.theme_mode = "dark"
    page.bgcolor = background_color
    
    def event(e):
        print(e.data)
        page.client_storage.set('window_event',str(e.data))
    
    page.on_window_event = event

    def re_login(e):
        container_to_relogin = Container(
            Text("Please reload the window, we are not able to log you in"),
            expand=True,
            opacity=0.5,
        )
        page.add(container_to_relogin)
        print("please re login")

    print(page.client_storage.get('token'))
    page.on_disconnect = logout
    page.on_close = logout
    # page.scroll = ScrollMode.ADAPTIVE
    page.on_connect = re_login
    refresh_token = page.client_storage.get("refresh_token")
    def route_change(route):
        if page.route ***REMOVED*** "/chat":
            
            name = page.client_storage.get("name")
            uid = page.client_storage.get("uid")
            newid = page.client_storage.get("token")

            print(f"{name},uid = {uid}")
            print(newid)
            page.views.clear()
            page.views.append(chat_handler(page, uid, name, newid)[page.route])
        else:
            page.views.clear()
            page.views.append(views_handler(page)[page.route])

    page.on_route_change = route_change
    # get the value of remember me
    remember = page.client_storage.get("remember")
    if remember:
        container = Container(
            Text("Loading . . . ", text_align="center", size=24, weight="bold"),
            expand=True,
            alignment=alignment.center,
            animate=animation.Animation(1000, "bounceInOut"),
        )
        page.add(container)
        newid = get_refresh_token(refresh_token=refresh_token)
        page.client_storage.remove("token")
        page.client_storage.set("token", newid)
        page.go("/chat")
        page.remove(container)

    else:
        page.go("/")


app(target=main, assets_dir="assets")
