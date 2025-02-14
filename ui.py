import threading
import customtkinter as ctk
from discord_api import get_latest_messages, send_message

DEFAULT_FONT = ("Segoe UI Emoji", 12)

def update_chat_box(chat_box, messages):
    """Updates the chat box widget with new messages."""
    if messages:
        # Reverse so that the oldest message is at the top
        messages = messages[::-1]
        chat_box.configure(state="normal")
        chat_box.delete(1.0, "end")
        for msg in messages:
            chat_box.insert("end", f"{msg}\n")
        chat_box.yview("end")
        chat_box.configure(state="disabled")

def fetch_messages(chat_box, channel, update_interval=500):
    """Fetches messages periodically for the given channel."""
    def task():
        messages = get_latest_messages(channel)
        chat_box.after(0, lambda: update_chat_box(chat_box, messages))
        chat_box.after(update_interval, lambda: fetch_messages(chat_box, channel, update_interval))

    threading.Thread(target=task, daemon=True).start()


def on_send_message(event, message_input, chat_box, channel):
    """Sends a message when the user presses Enter."""
    message = message_input.get()
    if message:
        send_message(channel, message)
        message_input.delete(0, "end")

def insert_emoji(emoji, message_input):
    """Inserts the selected emoji into the message input field."""
    message_input.insert("end", emoji)

def show_emoji_picker(message_input):
    """
    Opens a small emoji picker window with a grid of emojis.
    Clicking an emoji inserts it into the message input field.
    """
    picker_window = ctk.CTkToplevel(message_input)
    picker_window.title("Emoji Picker")
    emojis = ['😀', '😂', '😍', '👍', '❤️', '😢', '😎', '🎉', '😡', '👏']
    
    for i, emoji in enumerate(emojis):
        btn = ctk.CTkButton(
            picker_window,
            text=emoji,
            width=40,
            height=40,
            font=DEFAULT_FONT,
            command=lambda e=emoji: insert_emoji(e, message_input)
        )
        btn.grid(row=i // 5, column=i % 5, padx=5, pady=5)
    
    close_btn = ctk.CTkButton(picker_window, text="Close", font=DEFAULT_FONT, command=picker_window.destroy)
    close_btn.grid(row=(len(emojis) // 5) + 1, column=0, columnspan=5, pady=5)

def quit_program(chat_window):
    """Closes the application."""
    chat_window.quit()
