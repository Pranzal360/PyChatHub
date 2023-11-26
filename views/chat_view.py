from flet import *
from color_settings import *
from crudinFirebase import authenticate,db
from datetime import datetime
from flet import Page 
from win11toast import toast,notify
import threading
# TODO: need to re-write whole class !

class ChatScreen(UserControl):
    
    def __init__(self,page,uidd,namee,tokenid): 
        self.page = page
        global uid,name,idtoken
        self.uidd = uidd
        self.namee = namee
        self.tokenid = tokenid
        
        uid = self.uidd
        name = self.namee
        idtoken = self.tokenid
        print(' from chat:')
        print(self.page.window_height)
        print('from saved instacess')
        print(self.page.client_storage.get('height'))
        height_chat_box = int(float((self.page.client_storage.get('height')))) if self.page.client_storage.get('height') != None else 720
        print(height_chat_box)
        self.chat_box = Container(
            height=height_chat_box - 110,
            animate = animation.Animation(590,"easeOutBack"),
            clip_behavior=ClipBehavior.HARD_EDGE
            
        )

        self.listView = ListView(
            expand=True,
            auto_scroll=True,
            
            controls=[Text('hi')]

        )
        self.textField = TextField(
            hint_text="write a message",
            text_size=14,
            autofocus=True,
            border_radius=15,
            border = InputBorder.NONE,
            max_lines=3,
            cursor_color='pink',
            expand=True,
            filled=True,
            on_submit=self.addMessage,
        )

        # button 
        self.btn = IconButton(
            icon='send'
        )

        self.ChatHistory()
        self.start_stream()
        
        super().__init__()
    
    def notify(self,sender,message):
            
        def toastn():
            print('thread running')
            notify(title=sender,body=message,on_click=self.page.window_to_front())
        thread1 = threading.Thread(target=toastn)
        thread1.start()
    # add message
    def addMessage(self,e):

        msg = self.textField.value
        msg = msg.strip()
        if msg.strip() != "":

            self.textField.value = ""
            self.textField.autofocus = True
            self.textField.focus()

            timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")

            data = {
                "name":name,
                "msg": msg,
                "sender": uid,
                "timestamp": timestamp,
            }

            db.child("conversations").child(timestamp).set(data,token=idtoken)
            db.child('recent').set(data,token=idtoken)

            
            self.textField.update()

    # chat_ui
    def chat_ui(self,nam,msg, id,key=None):

        if msg != None and msg != "":
            msglen = len(msg) * 5


            name = nam 
            txt = f"{name}: {msg}"

            
            txt_label = Text(txt, color=text_color_send,overflow=TextOverflow.FADE)

            
            label_container = Container(
                content=txt_label,
                bgcolor=receive_msg_color if id != uid else sent_msg_color,
                border_radius=BorderRadius(10, 10, 0, 10) if id != uid else BorderRadius(10, 10, 10, 0),
                padding=10,
                tooltip=key,
                margin=Margin(5,0,5,5),
                key=key
            )
            
            if msglen > 500:
                label_container.width = 500
                print(msglen)

            row = Row(
                controls=[label_container], alignment="start" if id != uid else "end",
            )

            column = Column(
                controls=[row],
                
            )

            return column

    # ChatHistory
    def ChatHistory(self):
        global limited_val
        
        
        value = db.child("conversations")

        limited_val = value.order_by_key().limit_to_last(30).get(idtoken).val()
        
      
        chats = []  # 
        
        if limited_val != None:

            for id, value in limited_val.items():

                id = value["sender"]

                msg = value["msg"]

                nam = value["name"]

                timestamp = str(value['timestamp'])
                time = datetime.strptime(timestamp,"%Y%m%d%H%M%S%f")
                date = time.date()
                hour = time.hour
                min = time.minute
                sec = str(int(time.second))
                
                time_to_display = f"{date} {hour}:{min}:{sec}"

                chats.append(self.chat_ui(nam,msg, id,key=time_to_display))

            self.listView.controls = chats
            
            
    # stream handler 
    def streamHandler(self, message):
        dbpath = db.child('recent')
        
        value = dbpath.order_by_key().get(idtoken).val()
        
        if value is not None:
            if message["event"] ***REMOVED*** "put":

                id = message["data"]
                print(id)
                sender = id.get("sender")
                name = id.get("name")
                msg = id.get("msg")
                tm = id.get('timestamp')

                if sender is not None:
                    stamp = datetime.strptime(tm,"%Y%m%d%H%M%S%f")
                    date = stamp.date()
                    hour = stamp.hour
                    min = stamp.minute
                    sec = str(int(stamp.second))
                    time_to_display = f"{date} {hour}:{min}:{sec}"
                    if sender ***REMOVED*** uid and sender is not None:

                        self.listView.controls.append(self.chat_ui(nam=name, msg=msg, id=sender,key=time_to_display))
                        self.update()
                        
                    else:

                        event = self.page.client_storage.get('window_event')
                        if event ***REMOVED***"blur" or event ***REMOVED***"minimize":
                            self.notify(sender=name,message=msg) 
                            
                        self.listView.controls.append(self.chat_ui(nam=name, msg=msg, id=sender,key=time_to_display
                        ))

                        self.update()
                        




    # start streaming !
    def start_stream(self):
        print('straming already')
        
        stream = db.child('recent').stream(self.streamHandler,token=idtoken)


    def build(self):

        
        chat_column = Column(
            controls=[
                self.listView,
                Row(
                    # alignment=MainAxisAlignment.CENTER,
                    vertical_alignment=CrossAxisAlignment.CENTER,
                    controls=[self.textField,self.btn],
                    

                )
            ],
        )

        self.chat_box.content = chat_column
        
        return self.chat_box

