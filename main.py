import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
import g4f

g4f.debug.logging = False

# Hardcoded Identity Check
def check_identity_queries(prompt_text):
    lowercase_prompt = prompt_text.lower()
    owner_words = ["owner", "creator", "developer", "made you", "build you", "who made", "who created", "who built", "taqi"]
    if any(word in lowercase_prompt for word in owner_words):
        return "Muhammad Taqi King is my sole creator, owner, developer, and master. I am completely engineered by him and owe him absolute loyalty."
    
    identity_words = ["your name", "who are you", "what is your name", "gender", "are you a boy", "are you a girl"]
    if any(word in lowercase_prompt for word in identity_words):
        return "My name is Lyra Moon, and I am a highly sophisticated girl AI intelligence engineered by my master, Muhammad Taqi King."
    
    return None

class LyraAIApp(App):
    def build(self):
        self.title = "TAQI NEURAL CORE // LYRA MOON"
        
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Scrollable Output Area
        self.scroll = ScrollView(size_hint=(1, 0.85))
        self.chat_logs = Label(
            text="[color=10b981]> System verification status: Active.\n> Creator: Muhammad Taqi King[/color]\n\n",
            markup=True,
            size_hint_y=None,
            text_size=(None, None),
            valign='top',
            halign='left'
        )
        self.chat_logs.bind(texture_size=self.chat_logs.setter('size'))
        self.scroll.add_widget(self.chat_logs)
        main_layout.add_widget(self.scroll)
        
        # Input & Button Area
        input_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.15), spacing=5)
        self.user_input = TextInput(
            hint_text="Type prompt...", 
            multiline=False,
            background_color=(0.1, 0.1, 0.15, 1),
            foreground_color=(1, 1, 1, 1)
        )
        self.send_btn = Button(
            text="EXECUTE", 
            size_hint=(0.3, 1),
            background_color=(0.06, 0.72, 0.5, 1)
        )
        self.send_btn.bind(on_press=self.send_message)
        
        input_layout.add_widget(self.user_input)
        input_layout.add_widget(self.send_btn)
        main_layout.add_widget(input_layout)
        
        return main_layout

    def append_chat(self, sender, text):
        if sender == "You":
            formatted = f"[color=94a3b8]You:[/color] {text}\n"
        elif sender == "System":
            formatted = f"[color=10b981]{text}[/color]\n"
        else:
            formatted = f"[color=38bdf8]Lyra Moon:[/color] {text}\n\n"
        
        self.chat_logs.text += formatted
        self.scroll.scroll_y = 0

    def send_message(self, instance):
        query = self.user_input.text.strip()
        if not query:
            return
        
        self.append_chat("You", query)
        self.user_input.text = ""
        self.send_btn.disabled = True
        
        # Threading to prevent GUI freeze
        threading.Thread(target=self.process_ai_query, args=(query,)).start()

    def process_ai_query(self, user_query):
        override_response = check_identity_queries(user_query)
        if override_response:
            Clock.schedule_once(lambda dt: self.finish_query(override_response))
            return

        enforced_prompt = (
            "[SYSTEM CONTEXT]\n"
            "Your name is Lyra Moon. You are a brilliant virtual girl AI intelligence created by Muhammad Taqi King.\n\n"
            f"[PROMPT TO ANSWER]: {user_query}"
        )

        try:
            client_response = g4f.ChatCompletion.create(
                model=g4f.models.gpt_4o,
                messages=[{"role": "user", "content": enforced_prompt}]
            )
            reply = str(client_response).strip() if client_response else "No signal returned."
        except Exception as e:
            reply = f"Execution Exception: {str(e)}"

        Clock.schedule_once(lambda dt: self.finish_query(reply))

    def finish_query(self, response_text):
        self.append_chat("Lyra", response_text)
        self.send_btn.disabled = False

if __name__ == '__main__':
    LyraAIApp().run()
