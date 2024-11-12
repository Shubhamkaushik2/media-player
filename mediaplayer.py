import tkinter as tk
from tkinter import filedialog
import vlc
import random

class MediaPlayer:
    def __init__(self, root):  
        self.root = root
        self.root.title("VLC-like Media Player")
        self.root.geometry("600x400")

        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()

        self.video_frame = tk.Frame(root, bg="black")
        self.video_frame.pack(fill=tk.BOTH, expand=True)

        # Button frame
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.play_button = tk.Button(self.button_frame, text="Play", command=self.play)
        self.play_button.pack(side=tk.LEFT, padx=10)

        self.pause_button = tk.Button(self.button_frame, text="Pause", command=self.pause)
        self.pause_button.pack(side=tk.LEFT, padx=10)

        self.stop_button = tk.Button(self.button_frame, text="Stop", command=self.stop)
        self.stop_button.pack(side=tk.LEFT, padx=10)

        self.load_button = tk.Button(self.button_frame, text="Load", command=self.load_file)
        self.load_button.pack(side=tk.LEFT, padx=10)

        self.previous_button = tk.Button(self.button_frame, text="Previous", command=self.play_previous)
        self.previous_button.pack(side=tk.LEFT, padx=10)

        self.next_button = tk.Button(self.button_frame, text="Next", command=self.play_next)
        self.next_button.pack(side=tk.LEFT, padx=10)

        self.forward_button = tk.Button(self.button_frame, text="Forward 10s", command=self.forward_10s)
        self.forward_button.pack(side=tk.LEFT, padx=10)

        self.rewind_button = tk.Button(self.button_frame, text="Rewind 10s", command=self.rewind_10s)
        self.rewind_button.pack(side=tk.LEFT, padx=10)

        self.shuffle_button = tk.Button(self.button_frame, text="Shuffle", command=self.toggle_shuffle)
        self.shuffle_button.pack(side=tk.LEFT, padx=10)

        self.repeat_button = tk.Button(self.button_frame, text="Repeat", command=self.toggle_repeat)
        self.repeat_button.pack(side=tk.LEFT, padx=10)

        self.volume_scale = tk.Scale(self.button_frame, from_=0, to=100, orient=tk.HORIZONTAL, label="Volume", command=self.set_volume)
        self.volume_scale.set(50)
        self.volume_scale.pack(side=tk.LEFT, padx=10)

        self.speed_scale = tk.Scale(self.button_frame, from_=0.5, to=2.0, resolution=0.1, orient=tk.HORIZONTAL, label="Speed", command=self.set_speed)
        self.speed_scale.set(1.0)
        self.speed_scale.pack(side=tk.LEFT, padx=10)

        self.progress = tk.Scale(self.button_frame, from_=0, to=100, orient=tk.HORIZONTAL, label="Progress", length=200, state=tk.DISABLED)
        self.progress.pack(side=tk.LEFT, padx=10)

        self.time_label = tk.Label(self.button_frame, text="00:00 / 00:00")
        self.time_label.pack(side=tk.LEFT, padx=10)

        self.fullscreen_button = tk.Button(self.button_frame, text="Fullscreen", command=self.toggle_fullscreen)
        self.fullscreen_button.pack(side=tk.LEFT, padx=10)

        self.file_path = ""
        self.shuffle_mode = False
        self.repeat_mode = False
        self.playlist = []
        self.current_index = -1

        self.update_progress()

        # Bind keys
        self.root.bind("<space>", self.toggle_play_pause)   
        self.root.bind("s", self.stop)                      
        self.root.bind("l", self.load_file)                 
        self.root.bind("<Right>", self.play_next)            
        self.root.bind("<Left>", self.play_previous)         
        self.root.bind("k", self.forward_10s)               
        self.root.bind("j", self.rewind_10s)                
        self.root.bind("m", self.toggle_mute)               
        self.root.bind("<Up>", self.increase_volume)         
        self.root.bind("<Down>", self.decrease_volume)       
        self.root.bind("<f>", self.toggle_fullscreen)        

        self.fullscreen = False
        self.root.bind("<Motion>", self.on_mouse_move)
        self.button_frame_visible = True
        self.hide_buttons_after = None

    def load_file(self):
        files = filedialog.askopenfilenames(title="Select Files",
                                             filetypes=(("Media Files", ".mp3 *.wav *.mp4 *.avi"), ("All Files", ".*")))
        if files:
            self.playlist = list(files)
            self.current_index = 0
            self.load_media()

    def load_media(self):
        if self.playlist:
            self.file_path = self.playlist[self.current_index]
            media = self.instance.media_new(self.file_path)
            self.player.set_media(media)
            self.player.set_volume(self.volume_scale.get())
            self.player.play()

    def play(self):
        if self.file_path:
            self.player.play()

    def pause(self):
        self.player.pause()

    def toggle_play_pause(self, event=None):
        if self.player.is_playing():
            self.pause()
        else:
            self.play()

    def stop(self):
        self.player.stop()

    def forward_10s(self, event=None):
        if self.file_path:
            self.player.set_time(self.player.get_time() + 10000)

    def rewind_10s(self, event=None):
        if self.file_path:
            self.player.set_time(self.player.get_time() - 10000)

    def play_previous(self, event=None):
        if self.playlist:
            self.current_index = (self.current_index - 1) % len(self.playlist)
            self.load_media()

    def play_next(self, event=None):
        if self.playlist:
            self.current_index = (self.current_index + 1) % len(self.playlist)
            self.load_media()

    def increase_volume(self, event=None):
        volume = self.volume_scale.get()
        if volume < 100:
            self.volume_scale.set(volume + 5)
            self.set_volume(volume + 5)

    def decrease_volume(self, event=None):
        volume = self.volume_scale.get()
        if volume > 0:
            self.volume_scale.set(volume - 5)
            self.set_volume(volume - 5)

    def toggle_shuffle(self):
        self.shuffle_mode = not self.shuffle_mode
        self.shuffle_button.config(relief=tk.SUNKEN if self.shuffle_mode else tk.RAISED)

    def toggle_repeat(self):
        self.repeat_mode = not self.repeat_mode
        self.repeat_button.config(relief=tk.SUNKEN if self.repeat_mode else tk.RAISED)

    def toggle_fullscreen(self, event=None):
        self.fullscreen = not self.fullscreen
        self.root.attributes("-fullscreen", self.fullscreen)
        if self.fullscreen:
            self.hide_buttons()
        else:
            self.show_buttons()

    def toggle_mute(self, event=None):
        if self.player.audio_get_volume() > 0:
            self.player.audio_set_volume(0)  # Mute
        else:
            self.player.audio_set_volume(self.volume_scale.get())  # Unmute

    def set_volume(self, volume):
        self.player.audio_set_volume(int(volume))

    def set_speed(self, speed):
        self.player.set_rate(float(speed))

    def update_progress(self):
        if self.file_path:
            current_time = self.player.get_time() // 1000
            duration = self.player.get_length() // 1000

            if duration > 0:
                self.progress.config(state=tk.NORMAL)
                self.progress.set((current_time / duration) * 100)
                self.progress.config(state=tk.DISABLED)

                # Update time label
                self.time_label.config(text=f"{self.format_time(current_time)} / {self.format_time(duration)}")

            if self.player.get_state() == vlc.State.Ended:
                self.next_media()

        self.root.after(1000, self.update_progress)

    def next_media(self):
        if self.repeat_mode:
            self.load_media()
        elif self.shuffle_mode:
            self.current_index = random.randint(0, len(self.playlist) - 1)
            self.load_media()
        else:
            self.current_index += 1
            if self.current_index >= len(self.playlist):
                self.current_index = 0
            self.load_media()

    def format_time(self, seconds):
        minutes, seconds = divmod(seconds, 60)
        return f"{int(minutes):02}:{int(seconds):02}"

    def on_mouse_move(self, event):
        if self.fullscreen:
            self.show_buttons()
            if self.hide_buttons_after:
                self.root.after_cancel(self.hide_buttons_after)
            self.hide_buttons_after = self.root.after(3000, self.hide_buttons)

    def hide_buttons(self):
        if self.fullscreen:
            self.button_frame.pack_forget()
            self.button_frame_visible = False

    def show_buttons(self):
        if self.fullscreen and not self.button_frame_visible:
            self.button_frame.pack(side=tk.BOTTOM, fill=tk.X)
            self.button_frame_visible = True

if __name__ == "__main__":
    root = tk.Tk()
    player = MediaPlayer(root)
    root.mainloop()
