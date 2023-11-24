from flet import *
from color_settings import *
from crudinFirebase import authenticate,db
from datetime import datetime
from flet import Page 

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

        self.wid = 1280
        self.heig = 720
        self.chat_box = Container(
            height=self.heig-20,
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
            max_lines=3,
            # color="white",
            # cursor_color="white",
            expand=True,
            border_color=text_input_border,
            on_submit=self.addMessage,
            focused_color=text_input_border,
            bgcolor=text_input_bg,

        )

        # button 
        self.btn = IconButton(
            icon='send'
        )

        self.ChatHistory()
        self.start_stream()
        
        super().__init__()
    
    # add message
    def addMessage(self,e):

        msg = self.textField.value
        msg = msg.strip()
        if msg.strip() != "":

            self.textField.value = ""

            timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")

            data = {
                "name":name,
                "msg": msg,
                "sender": uid,
                "timestamp": timestamp,
            }

            db.child("conversations").child(timestamp).set(data,token=idtoken)
            
            self.textField.update()

    # chat_ui
    def chat_ui(self,nam,msg, id):

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
                
                margin=Margin(5,0,5,5),
                animate=animation.Animation(300,'bounceIn')
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
        print(idtoken)
        limited_val = value.order_by_key().limit_to_last(30).get(idtoken).val()
      
        chats = []  # 
        
        if limited_val != None:

            for id, value in limited_val.items():

                id = value["sender"]

                msg = value["msg"]

                nam = value["name"]
                chats.append(self.chat_ui(nam,msg, id))

            self.listView.controls = chats
            
    # stream handler 
    def streamHandler(self, message):
        print('i am not working')
        
        if limited_val is not None:
            if message["event"] ***REMOVED*** "put":

                id = message["data"]
 

                sender = id.get("sender")
                name = id.get("name")
                msg = id.get("msg")
                if sender is not None:
                    if sender ***REMOVED*** uid and sender is not None:

                        self.listView.controls.append(self.chat_ui(nam=name, msg=msg, id=sender))
                        self.update()
                    else:


                        self.listView.controls.append(self.chat_ui(nam=name, msg=msg, id=sender))
                        self.update()
        



    # start streaming !
    def start_stream(self):
        print('straming already')
        stream = db.child("conversations").stream(self.streamHandler,token=idtoken)
    

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

