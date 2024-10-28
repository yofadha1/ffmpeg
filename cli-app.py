import app

application = app.App()
menu_list = [
    {"menu": "compress video", "command": application.compress_video},
    {"menu": "convert video format", "command": application.build},
    {"menu": "convert audio format", "command": application.build},
    {"menu": "extract audio from video", "command": application.extract_audio_from_video},
    {"menu": "remove audio from video", "command": application.remove_audio_from_video},
    {"menu": "trim video", "command": application.trim_video},
    {"menu": "scale video resolution", "command": application.scale_video_resolution},
    {"menu": "change frame rate", "command": application.change_frame_rate},
    {"menu": "extract frames as images", "command": application.extract_frames_as_images},
    {"menu": "create video from images", "command": application.create_video_from_images},
    {"menu": "add subtitle to video", "command": application.add_subtitle_to_video},
    {"menu": "merge video and audio", "command": application.merge_video_and_audio},
    {"menu": "change video bitrate", "command": application.change_video_bitrate},
    {"menu": "add audio to video", "command": application.add_audio_to_video},
    {"menu": "adjust video speed", "command": application.adjust_video_speed},
    {"menu": "adjust audio speed", "command": application.adjust_audio_speed},
    {"menu": "crop video", "command": application.crop_video},
    {"menu": "add watermark to video", "command": application.add_watermark_to_video},
    {"menu": "loop video x times", "command": application.loop_video},
    {"menu": "convert video to gif", "command": application.convert_to_gif}
]


def print_menu():
    global menu_list
    for i, n in enumerate(menu_list, 1):
        print(f"{i}. {n['menu']}")


if __name__ == '__main__':
    print_menu()
    selected_menu = int(input("select menu: "))
    input_path = input("input path: ")
    output_path = input("output_path: ")
    # for debug purpose
    # input_path = './10s.mp4'
    # output_path = './output/10s.mp4'
    application.set_file_input(input_path)
    application.set_output_path(output_path)
    application.use_debugger()
    command = menu_list[selected_menu - 1]['command']
    command_vars = command.__code__.co_varnames[1:]
    command_argcount = command.__code__.co_argcount
    if command_argcount == 1:
        try:
            command()
        except Exception as e:
            print(f"error: {e}")
    else:
        try:
            application_vars = []
            for i in range(1, command_argcount):
                var = input(f"input {command_vars[i - 1]}: ")
                application_vars.append({command_vars[i - 1]: var})
            command(**{k: v for d in application_vars for k, v in d.items()})
        except Exception as e:
            print(f"error: {e}")
