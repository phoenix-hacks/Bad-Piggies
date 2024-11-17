import ollama
import subprocess
import time

def llmotpt(userinput:str,input_path:str,output_path:str,audio_path:str=None):
    response = ollama.chat(model='llama3.1', messages=[{
'role': 'user',
        'content': f"""
Your task is to analyse the user input and output the function with the required parameters from the user message.

Function definitions:
from moviepy.editor import *
#The input clip takes user path and NOT 'video'
clip=VideoFileClip(r"{input_path}")


# reduce the volume, pass the clip that is defined prior and the scaledvolume variables takes an input from 0 to 5
def volume(clip,scaledvolume):
    clip=clip.volumex(scaledvolume)
    return clip

# writes edits to a new file, takes clip/video as an input should be called at the end of every file
def writeEnd(video, filename=r"{output_path}", fps=24):
    video.write_videofile(filename, fps=fps,threads=4)

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

# saves the clip as a gif file
def gif(clip,start,end):
    clip=clip.subclip(start,end)
    clip.write_gif("output.gif")

# rotates the clip by a given angle
def rotateClip(clip,value):
    clip = clip.rotate(value)
    return clip

# resizes the clip, either based on a scale value, height or width
def resizeClip(clip,value=None,height=None,width=None):
    height=clip.size[1] if height==None else height
    width=clip.size[0] if width==None else width
    if(value!=None):
        clip = clip.resize(value)
    else:
        clip = clip.resize(height=height,width=width)
    return clip

# adds background music to a clip from an audio file
def addBackgroundMusic(video, audio_file={audio_path}, start_time=0, volume=0.8):
    audio = AudioFileClip(audio_file).volumex(volume)
    audio = audio.set_start(start_time)
    clip = video.set_audio(audio)
    return clip

# changes the brightness of the clip
def brightness(clip,factor):
    clip=vfx.colorx(clip,factor)
    return clip

Example:
1. User input: Reduce the volume to 0 and change the colour to black and white in the given video.
Expected output:
clip = volume(clip,0)
clip = blackAndWhite(clip)

2. User input: Trim the clip from the 8th second to the 15th second and set the speed to 1.5x.
Expected output:
clip = trimClip(clip,8,15)
clip = adjustSpeed(clip,1.5)

3. User input: Add the text "Hello World", to the video with a font size of 15 for 10 seconds
Expected output:
clip = text_clip(clip,"Hello World", 15,'black',10)

4. User input: Can you rotate the video by 90 degrees and save the video as a gif between the 10th and 20th second?
Expected output:
clip = rotateClip(clip,90)
gif(clip,10,20)

5. User input: Can you scale this video by a factor of 2
Expected output:
clip = resizeClip(clip,2)

6. User input: Can you add the background music provided ({audio_path})
Expected output:
clip = addBackgroundMusic(clip,'{audio_path}')

7. User input: Can you increase the brightness of the video?
Expected output:
clip = brightness(clip,1.5)

Remember, output only the function calls with the required parameters which are equated to 'clip'. Output in plaintext, if multiple functions are to be called
then use nextline for each function. Do not hallucinate and make up your own functions. Just output what is asked and do what is told.
Consistently give the correct output.

User input: {userinput}
"""},],options={'num_ctx':8192})
    
    output_llm = response['message']['content']


    py_file = f"""
import subprocess
subprocess.run(['python', '-m', 'pip', 'install', 'moviepy'])
from moviepy.editor import *
clip=VideoFileClip(r"{input_path}")

# reduce the volume, pass the clip that is defined prior and the scaledvolume variables takes an input from 0 to 5
def volume(clip,scaledvolume):
    clip=clip.volumex(scaledvolume)
    return clip

# writes edits to a new file, takes clip/video as an input should be called at the end of every file
def writeEnd(video, filename="{output_path}", fps=24):
    video.write_videofile(r'{output_path}', fps=fps,threads=4,preset='ultrafast')

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

    
def addBackgroundMusic(video, audio_file={audio_path}, start_time=0, volume=0.8):
    audio = AudioFileClip(audio_file).volumex(volume)
    audio = audio.set_start(start_time)
    clip = video.set_audio(audio)
    return clip
    
def brightness(clip,factor):
    clip=vfx.colorx(clip,factor)
    return clip

{output_llm}

writeEnd(clip)

"""
    

    with open('writer.py','w') as f:
        f.write(py_file)
    f.close()
    print("L")
    
    subprocess.run(["python","writer.py"])
#llmotpt("Please increase the brightness of the video")
