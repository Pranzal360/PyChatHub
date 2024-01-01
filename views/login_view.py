from flet import *
from color_settings import *
from crudinFirebase import authenticate,get_refresh_token,reset_pwd
from datetime import datetime
from time import sleep
from additional_funcs import set_expirey

# TODO: remember me and forgot password

class Authentication(UserControl):
    def __init__(self, page):
        self.page = page
        # self.check_rememberme()
        super().__init__()

    def to_signup(self, e):
        self.page.go("/signup")

    def close_bottomsheet(self,e):
        
        self.email = self.reset_email.value + self.reset_email.suffix_text
        self.progress_bar.visible = True
        self.page.update()
        reset_pwd(self.email)
        self.bottom_sheet.open = False
        self.page.update()
    
    def password_reset(self, e):
        # self.page.go('/reset')
        self.reset_email =  TextField(hint_text="email",
            prefix_icon=icons.ACCOUNT_CIRCLE,

            color="#f2f2f2",
            border_radius=10,
            autofocus=True,
            bgcolor="#383636",
            cursor_color="lightblue",
            border_color="#383636",
            suffix_text='@gmail.com',
            helper_text='Note: Exclude @gmail.com',)
        self.progress_bar = ProgressBar(visible=False)
        self.bottom_sheet = BottomSheet(
            Container(
                Column(
                    [
                        self.progress_bar,
                        self.reset_email,
                        ElevatedButton(
                            text="Send Reset Link",
                            bgcolor="lightblue",
                            color="#ffffff",
                            height=40,
                            on_click=self.close_bottomsheet
                        )
                    ]
                ),
                margin=Margin(10,30,10,10)
            ),
            open=True,
        )
        
        self.page.overlay.append(self.bottom_sheet)
        self.page.update()

 
    def build(self):
        
        def submit(e):
            email = username.value+username.suffix_text
            passw = password.value
            username.disabled = True
            password.disabled = True
            self.submit_btn.disabled = True
            self.update()
            print(email, passw)

            self.page.overlay.append(stack_progressRing)
            self.page.update()
            if username.value != "" and password.value != "":
                try:
                    uid, name,idToken,refresh_token = authenticate(email, passw)
                    username.border_color = "green"
                    password.border_color = "green"
                    username.error_text = ""
                    password.error_text = ""
                    print("auth done")
                    remember_me_btn = remember_me.value
                    self.page.overlay.clear()
                    self.page.update()
                    # getting the expirey date
                    exp = set_expirey()
                    # set shared prefences !
                    self.page.client_storage.set('height',str(self.page.window_height))
                    self.page.client_storage.set("uid", uid)
                    self.page.client_storage.set("name", name)
                    self.page.client_storage.set("token", idToken)
                    self.page.client_storage.set("refresh_token", refresh_token)
                    self.page.client_storage.set("remember", remember_me_btn)
                    self.page.client_storage.set('expires_on',exp)
                    # open chat_class insance as login is successful
                    sleep(0.33)
                    self.page.go("/chat")

                except Exception as e:
                    username.disabled = False
                    password.disabled = False
                    self.submit_btn.disabled = False
                    print(e)
                    username.error_text = "Enter your correct email"
                    username.error_style = TextStyle(size=15)
                    password.value = ""
                    password.error_text = "Enter your correct password"
                    password.error_style = TextStyle(size=15)
                    self.update()
                    self.page.overlay.clear()
                    self.page.update()

            else:
                username.disabled = False
                password.disabled = False
                self.submit_btn.disabled = False
                username.error_text = "Enter your email"
                username.error_style = TextStyle(size=15)


                password.error_text = "Enter your password"
                password.error_style = TextStyle(size=15)
                self.submit_btn.disabled = False
                self.update()
                self.page.overlay.clear()
                self.page.update()

        self.wel_text = Text("Welcome!", color="lightblue", size=20, weight="bold")
        self.pls = Text("please login to your account", color="white", size=16)

        username = TextField(
            hint_text="email",
            prefix_icon=icons.ACCOUNT_CIRCLE,
            width=420,
            color="#f2f2f2",
            border_radius=10,
            autofocus=True,
            bgcolor="#383636",
            cursor_color="lightblue",
            border_color="#383636",
            suffix_text='@gmail.com',
            helper_text='Note: Exclude @gmail.com',
        )

        password = TextField(
            hint_text="password",
            prefix_icon=icons.LOCK_ROUNDED,
            border_radius=10,
            width=420,
            password=True,
            bgcolor="#383636",
            color="#f2f2f2",
            cursor_color="lightblue",
            border_color="#383636",
            on_submit=submit,
            can_reveal_password=True,
        )

        self.submit_btn = ElevatedButton(
            text="Login",
            bgcolor="lightblue",
            color="#ffffff",
            width=420,
            height=40,
            on_click=submit,
        )

        progressRing = ProgressRing(
            color="green",
            top=400,
            left=800,
        )

        remember_me = Checkbox(label="Remember Me", value=False)

        signuptext_1 = Text(" Don't have an account yet?", size=16)
        signuptext_2 = Text("Click here to Signup", color="lightblue", size=16)
        sign_2 = Container(
            content=signuptext_2,
            on_click=self.to_signup,
            ink=True,
        )
        row_of_signup = Row([signuptext_1, sign_2])

        forgot_password = Text(" Forgot Password?", color="#dc143c", size=16)
        forgot_password_btn = Container(
            content=forgot_password,
            on_click=self.password_reset,
            ink=True,
        )
        dark_container = Container(bgcolor="#1f1b1b", opacity=0.5)
        stack_progressRing = Stack(controls=[dark_container, progressRing], expand=True)
        colm = Column(
            spacing=5,
            expand=True,
            controls=[
                self.wel_text,
                self.pls,
                username,
                password,
                remember_me,
                self.submit_btn,
                row_of_signup,
                Divider(),
                forgot_password_btn,
            ],
        )

        container = Container(
            content=colm, padding=80, width=600, col=6, margin=Margin(50, 0, 10, 0)
        )

        container2 = Image(
            src="../assets/sysadmin_darkmode.png",
            height=490,
            width=600,
            col=6,
        )

        row = ResponsiveRow(controls=[container, container2], expand=True)

        cont = Container(content=row, margin=Margin(20, 135, 10, 0))

        return cont
