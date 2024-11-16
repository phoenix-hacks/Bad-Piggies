from moviepy.editor import *

def volume(clip,scaledvolume):  
    clip=clip.volumex(scaledvolume)
    return clip
def addBackgroundMusic(video, audio_file, start_time=0, volume=0.8):
    audio = AudioFileClip(audio_file).volumex(volume)
    audio = audio.set_start(start_time)
    video = video.set_audio(audio)
    return video
def addText(text:str, fontsize:int,font:str,color:str,bg_color:str):
    txt=TextClip(text,fontsize=fontsize,font=font,color=color,bg_color=bg_color)
    return txt

def repositionText(txt:TextClip,posstr:str=None,position:tuple[float,float]=(0,0)):
    txt = txt.set_position(posstr if posstr!=None else position)
    return txt
def compositeVideo(clips:list):
    video=CompositeVideoClip([clips])
    return video
def concatVids(clips:list):
    video=concatenate_videoclips(clips)
    return video
def stackAndPositionVids(clips:dict):
    video=compositeVideo([i.set_position(clips[i]) if clips[i]!=(0,0) else i for i in clips ])
    video.preview()
    return video
def trimClip(clip,t1,t2):
    video=clip.subclip(t1,t2)
    return video
def adjustSpeed(clip, speed_factor=1.0):
    return clip.fx(vfx.speedx, speed_factor)
def blackAndWhite(video):
    video=video.fx(vfx.blackwhite)
    return video
def writeEnd(video, filename="Untitled.mp4", fps=24):
    video.write_videofile(filename, fps=fps, codec="libx264", audio_codec="aac", threads=4, preset="ultrafast")

