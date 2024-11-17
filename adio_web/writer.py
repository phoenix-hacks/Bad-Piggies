
import subprocess
subprocess.run(['python', '-m', 'pip', 'install', 'moviepy'])
from moviepy.editor import *
clip=VideoFileClip(r"static/uploads\video.mp4")

# reduce the volume, pass the clip that is defined prior and the scaledvolume variables takes an input from 0 to 5
def volume(clip,scaledvolume):
    clip=clip.volumex(scaledvolume)
    return clip

# writes edits to a new file, takes clip/video as an input should be called at the end of every file
def writeEnd(video, filename="static/processed_videos\video_processed.mp4", fps=24):
    video.write_videofile(r'static/processed_videos\video_processed.mp4', fps=fps,threads=4,preset='ultrafast')

# this sets the colour to black and white in the video
def blackAndWhite(video):
    video=video.fx(vfx.blackwhite)
    return video

# trims the clip between two "seconds" frames, consider the the inputs to be 8 and 12, then it'll trim the clip between the 8th and the 12th second
def trimClip(clip,t1,t2):
    video=clip.subclip(t1,t2)
    return video

# sets the speed of the video (video playback speed)
def adjustSpeed(clip, speed_factor=1.0):
    return clip.fx(vfx.speedx, speed_factor)

# returns a text that can be added to the video
def text_clip(clip:VideoFileClip,text:str,font_size:int,color:str,duration:int):
    txt_clip = TextClip(text, fontsize = font_size, color = color)
    txt_clip = txt_clip.set_pos('center').set_duration(duration)  
    list_clip = [clip,txt_clip]
    clip = CompositeVideoClip(list_clip) # use these two lines when you need to add a text to a clip
    return clip

def gif(clip,start,end):
    clip=clip.subclip(start,end)
    clip.write_gif("output.gif")
    
def rotateClip(clip,value):
    clip = clip.rotate(value)
    return clip

def resizeClip(clip,value=None,height=None,width=None):
    height=clip.size[1] if height==None else height
    width=clip.size[0] if width==None else width
    if(value!=None):
        clip = clip.resize(value)
    else:
        clip = clip.resize(height=height,width=width)
    return clip

    
def addBackgroundMusic(video, audio_file=None, start_time=0, volume=0.8):
    audio = AudioFileClip(audio_file).volumex(volume)
    audio = audio.set_start(start_time)
    clip = video.set_audio(audio)
    return clip
    
def brightness(clip,factor):
    clip=vfx.colorx(clip,factor)
    return clip

clip = rotateClip(clip,10)

writeEnd(clip)

