import os

base_command = "./ffmpeg "
file_input = None
output_path = None
debugger = False

class App:
    def set_file_input(self, path):
        global file_input, base_command
        file_input = path 
        base_command = f"{base_command} -i {path}"
        return self

    def set_output_path(self, path):
        global output_path, base_command
        output_path = path
        return self
    
    def use_debugger(self):
        global debugger
        debugger = True

    def compress_video(self):
        # -vcodec libx265 sets the codec to libx265 (H.265)
        # -crf 28 controls the quality: lower values mean higher quality (default is 23).
        global base_command
        base_command = f"{base_command} -vcodec libx265 -crf 28"
        self.build()

    def extract_audio_from_video(self):
        # vn remove audio from video
        # -acodec copy keeps the original audio codec without re-encoding.
        global base_command
        base_command = f"{base_command} -vn -acodec copy"
        self.build()

    def trim_video(self, start_time, end_time):
        global base_command
        base_command = f"{base_command} -ss {start_time} -t {end_time} -c copy"
        self.build()

    def scale_video_resolution(self, width, height):
        # -vf applies a video filter. scale=width:height
        global base_command
        base_command = f"{base_command} -vf scale={width}:{height} -c copy"
        self.build()

    def change_frame_rate(self, fps):
        global base_command
        base_command = f"{base_command} -r {fps} -c copy"
        self.build()

    def extract_frames_as_images(self, fps):
        # -r {fps} saves x frame per second.
        global base_command
        base_command = f"{base_command} -r {fps} -f image2"
        self.set_output_path("frame_%04d.png")
        self.build()

    def create_video_from_images(self, fps = 24):
        # set the file input to something like frame_%04d.png
        global base_command
        base_command = f"{base_command} -framerate {fps} -c:v libx265"
        self.build()

    def add_subtitle_to_video(self, subtitle_path):
        global base_command
        base_command = f"{base_command} -vf subtitles={subtitle_path} -c copy"
        self.build()

    def merge_video_and_audio(self, audio_path):
        # -c:v copy copies the video codec (avoiding re-encoding).
        # -c:a aac re-encodes the audio to AAC format.
        global base_command
        base_command = f"{base_command} -i {audio_path} -c:v copy -c:a aac"
        self.build()

    def change_video_bitrate(self, bitrate):
        # set input like 1M, it sets the video bitrate to 1 Mbps.
        global base_command
        base_command = f"{base_command} -b:v {bitrate}"
        self.build()

    def remove_audio_from_video(self):
        # -an removes the audio
        global base_command
        base_command = f"{base_command} -an"
        self.build(self)

    def add_audio_to_video(self, audio_path):
        # -map 0:v selects the video from the first input (video).
        # -map 1:a selects audio from the second input (audio).
        # -c:v copy copies the video without re-encoding.
        # -shortest makes the output video match the shortest stream length.
        global base_command
        base_command = f"{base_command} -i {audio_path} -map 0:v -map 1:a -c:v copy -shortest"
        self.build()

    def adjust_video_speed(self, speed):
        global base_command
        base_command = f"{base_command} -filter:v \"setpts={speed}*PTS\" -c copy"
        self.build()

    def adjust_audio_speed(self, speed):
        global base_command
        base_command = f"{base_command} -filter:a \"atempo={speed}\" -c copy"
        self.build()

    def crop_video(self, x, y, width, height):
        global base_command
        base_command = f"{base_command} -vf \"crop={width}:{height}:{x}:{y}\" -c copy"
        self.build()

    def add_watermark_to_video(self, watermark_path, x = 10, y = 10):
        # overlay x:y places watermark watermark.png at x:y pixels from the top-left corner.
        global base_command
        base_command = f"{base_command} -i {watermark_path} -filter_complex \"overlay={x}:{y}\" -c copy"
        self.build()

    def loop_video(self, x):
        global base_command
        base_command = f"{base_command} -stream_loop {x} -c copy"
        self.build()

    def convert_to_gif(self, fps, height, width):
        global base_command
        base_command = f"{base_command} \"fps={fps},scale={width}:{height}\""
        self.build()

    def build(self):
        global file_input, output_path, base_command 
        if file_input is None:
            raise ValueError("file input cannot be empty")
        if output_path is None:
            output_path = f"./output/{file_input.__str__()}"

        base_command = f"{base_command} {output_path}"
        if debugger:
            execute = input(f"{base_command} (y/n): ")
            if str(execute).lower() == 'y':
                print(f"executing: {base_command}")
                os.system(base_command)
            else:
                print("terminated")
        else:
            print(f"executing: {base_command}")
            os.system(base_command)
