from flet import *
from color_settings import *
import re
from requests.exceptions import HTTPError
from crudinFirebase import create_user, check_username
from validate_email_address import validate_email

# TODO: signup verification and minor ui changes

class Register(UserControl):
    def __init__(self, page):

        self.usernameField = TextField(
            hint_text="Enter a username",
            border_radius=8,
            color="#d7d7d7",
            bgcolor="#383636",
            focused_border_color="lightblue",
            label="Username",
            border_color="#383636",
            on_focus=self.uname_help,
            on_blur=self.uname_lost,
        )
        self.emailField = TextField(
            hint_text="Email",
            label="Email",
            suffix_text="@gmail.com",
            border_radius=8,
            color="#d7d7d7",
            bgcolor="#383636",
            border_color="#383636",
            focused_border_color="lightblue",
            helper_text="Note: Exclude @gmail.com from your email address",
        )

        self.passwordField = TextField(
            hint_text="Password",
            password=True,
            border_radius=8,
            can_reveal_password=True,
            color="#d7d7d7",
            bgcolor="#383636",
            border_color="#383636",
            focused_border_color="lightblue",
        )
        self.passwordConfirm = TextField(
            hint_text="Confirm",
            password=True,
            border_radius=8,
            color="#d7d7d7",
            bgcolor="#383636",
            border_color="#383636",
            focused_border_color="lightblue",
            on_submit=self.submit,
            can_reveal_password=True,
        )
        self.submit_btn = ElevatedButton(
            text="Sign Up",
            width=800,
            height=40,
            bgcolor=button_bg_color,
            color="#d7d7d7",
            on_click=self.submit,
        )
        self.imageView = Image(
            col=6,
            src="../assets/signup_scrn.png",
            width=600,
            height=400,
        )
        self.progressRing = ProgressRing(
            color="blue",
            top=400,
            left=800,
        )
        self.dark_container = Container(
            bgcolor='#1f1b1b',
            opacity=.5
        )
        self.stack = Stack(
            controls=[self.dark_container,self.progressRing],
            expand=True,
        )

        return super().__init__()

    def uname_help(self, *args):
        self.usernameField.helper_text = (
            "Username must not contain symbols like '@','.',[ ]','#','/','?', "
        )
        self.update()

    def uname_lost(self, *args):
        self.usernameField.helper_text = ""
        self.update()

    def is_valid_username(self, username):
        # Firebase does not allow certain characters in keys
        forbidden_characters = r"[@.?$#\[\]/\x00-\x1F]"
        self.passwordField.error_text = ""
        self.passwordConfirm.error_text = ""
        self.page.update()

        if len(username) > 12:
            self.usernameField.error_text = "Username must be less then 12 characters"
            self.passwordConfirm.disabled = False

            self.submit_btn.disabled = False
            self.update()
            self.page.overlay.clear()
            self.page.update()
            return False

        if re.search(forbidden_characters, username):
            self.usernameField.error_text = "Invalid username: Username must not contain symbols like '@','.',[ ]','#','/'"
            self.passwordConfirm.disabled = False

            self.submit_btn.disabled = False
            self.update()
            self.page.overlay.clear()
            self.page.update()
            return False

        return True

    def is_valid_password(self, password):

        if len(password) < 6:

            self.passwordField.error_text = (
                "Please use a password between 6 and 16 characters"
            )
            self.passwordConfirm.error_text = (
                "Please use a password between 6 and 16 characters"
            )
            self.page.close_dialog()
            self.passwordConfirm.disabled = False

            self.submit_btn.disabled = False
            self.update()

            return False
        return True

    def is_valid_email(self, email):
        if validate_email(email) ***REMOVED*** False:

            self.emailField.error_text = "Invalid email: Exclude @gmail.com if used "

            self.passwordConfirm.disabled = False
            self.submit_btn.disabled = False
            self.update()
            self.page.overlay.clear()
            self.page.update()
            return False

        return True

    def submit(self, e):

        if all(
            s != ""
            for s in [
                self.usernameField.value.strip(),
                self.emailField.value.strip(),
                self.passwordField.value.strip(),
                self.passwordConfirm.value.strip(),
            ]
        ):

            self.submit_btn.disabled = True
            self.passwordConfirm.disabled = True

            self.update()

            if self.passwordField.value != self.passwordConfirm.value:

                self.passwordField.error_text = "Passwords do not match. Please ensure that the passwords you entered in both fields are the same."
                self.passwordConfirm.error_text = "Passwords do not match. Please ensure that the passwords you entered in both fields are the same."
                self.passwordConfirm.disabled = False
                self.submit_btn.disabled = False
                self.update()

            else:
                if self.is_valid_password(self.passwordField.value):
                    self.page.overlay.append(self.stack)
                    self.page.update()
                    
                    if self.is_valid_username(self.usernameField.value):
                        email = self.emailField.value + self.emailField.suffix_text
                        if self.is_valid_email(email):
                            self.emailField.error_text = ""
                            self.usernameField.error_text = ""
                            self.passwordConfirm.error_text = ""
                            self.passwordField.error_text = ""
                            self.update()

                            try:
                                if create_user(email,self.passwordConfirm.value,self.usernameField.value.lower()):
                                    self.page.add(
                                        SnackBar(
                                            content=Text(
                                                "Sign Up successful, redirecting to login",
                                                color="green",
                                            ),
                                            bgcolor="#232222",
                                            open=True,
                                        )
                                    )
                                    self.emailField.value = ""
                                    self.usernameField.value = ""
                                    self.passwordConfirm.value = ""
                                    self.passwordField.value = ""

                                    self.update()
                                    self.page.overlay.clear()
                                    self.page.update()
                                    self.page.go("/")
                                else:

                                    self.usernameField.error_text = (
                                        "Username already exsits !"
                                    )

                                    self.passwordConfirm.disabled = False
                                    self.submit_btn.disabled = False
                                    self.update()
                                    self.page.overlay.clear()
                                    self.page.update()

                            except HTTPError as e:
                                if "EMAIL_EXISTS" in str(e):

                                    self.update()

                                    self.emailField.error_text = "Email already in use ! Please use another email"
                                    self.passwordConfirm.disabled = False

                                    self.submit_btn.disabled = False
                                    self.update()
                                    self.page.overlay.clear()
                                    self.page.update()
                                else:

                                    self.passwordConfirm.disabled = False
                                    self.submit_btn.disabled = False
                                    self.update()
                                    self.page.overlay.clear()
                                    self.page.update()
                                    print(e)

                    else:
                        print("invalid Username detected")
                else:
                    print("Invalid password detected")

        else:
            self.page.add(
                SnackBar(
                    content=Text("Fields should not be empty", color="red"),
                    open=True,
                    bgcolor="#232222",
                )
            )
            self.update()

    def route_changer(self, e):
        Page.go(self.page, route="/")

    def build(self):

        welcome_text = " Create new account"
        footer_text = Text(" Already have an Account?",size=16)
        footer_text2 = Text("Click here to Login",color="lightblue",size=16)
        text_btn = Container(footer_text2, ink=True, on_click=self.route_changer)
        row = Row(
            controls=[footer_text,text_btn],
            wrap=True,
        )
        text = Text(
            welcome_text, size=24, color="lightblue", weight="bold", text_align="center"
        )
        column = Column(
            col=6,
            controls=[
                text,
                self.usernameField,
                self.emailField,
                self.passwordField,
                self.passwordConfirm,
                self.submit_btn,
                row,
            ],
            run_spacing=8,
        )
        container = Container(
            content=column,
            col=6,
            margin=10,
            padding=10,
            alignment=alignment.bottom_center,
        )
        respRow = ResponsiveRow(controls=[container, self.imageView])

        window_container = Container(
            respRow,
            margin=Margin(20, 200, 20, 0),
        )

        return window_container
