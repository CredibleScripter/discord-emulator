import time

print("\n" + "=" * 40)
print("      🌟 DISCORD EMULATOR 🌟")
print("=" * 40)
print("\n🔄 Loading... This may take a while depending on the number of channels.")
time.sleep(1) 
print("✅ Ready!\n")



import customtkinter as ctk
from discord_api import send_message
from ui import (
    DEFAULT_FONT,
    fetch_messages,
    on_send_message,
    show_emoji_picker,
    quit_program
)
from config_manager import load_config
from discord_api import changeUserIdStatus

false = False
true = True

# Load configuration
config = load_config()
current_channel = None


# Get channels from config
channels = config.get("CHANNELS", [])
if not channels:
    channels = [
        {"name": "Macca's", "id": "1339547962723926048"}
    ]



current_channel = channels[0]["id"]  # Set the first channel as default
current_channel_name = channels[0]["name"]



def send_sick_dog_message():
    global current_channel
    send_message(current_channel, "i am cool discord emulator user because stormys client sucks dog")

def switch_channel(channel_obj, chat_box):
    global current_channel, current_channel_name
    current_channel = channel_obj["id"]  # Update active channel
    current_channel_name = channel_obj["name"]
    
    print(f"Switched channel to {current_channel_name} ({current_channel})")

    # Clear chat box before loading messages
    chat_box.configure(state="normal")
    chat_box.delete(1.0, "end")
    chat_box.configure(state="disabled")

    # Fetch messages for the selected channel
    fetch_messages(chat_box, current_channel)


def main():
    # Use system appearance for native integration
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    # Create the main chat window with standard OS window decorations.
    chat_window = ctk.CTk()
    chat_window.title("Discord Chat")
    chat_window.geometry("600x500")

    # Create chat box (text area)
    chat_box = ctk.CTkTextbox(chat_window, width=460, height=300, wrap="word", font=DEFAULT_FONT)
    chat_box.grid(row=1, column=1, padx=20, pady=10, sticky="nsew")
    fetch_messages(chat_box, current_channel)  # Start fetching messages only for the default channel

    # Create message input field
    message_input = ctk.CTkEntry(chat_window, width=460, font=DEFAULT_FONT)
    message_input.grid(row=2, column=1, padx=20, pady=10, sticky="ew")
    message_input.bind("<Return>", lambda event: on_send_message(event, message_input, chat_box, current_channel))

    # Quit button (in addition to native window controls)
    quit_button = ctk.CTkButton(chat_window, text="Quit", width=50, height=30, fg_color="grey", font=DEFAULT_FONT,
                                command=lambda: quit_program(chat_window))
    quit_button.grid(row=2, column=2, padx=0, pady=0)

    quit_button = ctk.CTkButton(chat_window, text="Toggle UserIds", width=50, height=30, fg_color="Blue", font=DEFAULT_FONT,
                                command=lambda: changeUserIdStatus())
    quit_button.grid(row=1, column=2, padx=0, pady=0)


    # Create a frame for channel buttons on the left
    button_frame = ctk.CTkFrame(chat_window, width=40, height=400)
    button_frame.grid(row=1, column=0, rowspan=2, padx=5, pady=10, sticky="ns")

    # Create a button for each channel from the config
    for i, channel in enumerate(channels):
        btn = ctk.CTkButton(
            button_frame,
            text=channel["name"],
            width=15,
            height=30,
            font=DEFAULT_FONT,
            command=lambda ch=channel: switch_channel(ch, chat_box)
        )
        btn.grid(row=i, column=0, padx=5, pady=10)

    # Dizzycord button
    dizycord_button = ctk.CTkButton(chat_window, text="Discord Emulator V1.2.3", width=100, height=30, font=DEFAULT_FONT,
                                    command=send_sick_dog_message)
    dizycord_button.grid(row=0, column=1, padx=10, pady=10)

    # Emoji button
    emoji_button = ctk.CTkButton(chat_window, text="Emoji", width=50, font=DEFAULT_FONT,
                                 command=lambda: show_emoji_picker(message_input))
    emoji_button.grid(row=3, column=1, padx=20, pady=5)
    # Configure grid weights for responsiveness
    chat_window.grid_rowconfigure(1, weight=1)
    chat_window.grid_columnconfigure(1, weight=1)

    # Start fetching messages in the background
    fetch_messages(chat_box, current_channel)

    chat_window.mainloop()

if __name__ == "__main__":
    main()
