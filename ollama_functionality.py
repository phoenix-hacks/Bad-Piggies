import ollama
import subprocess
import time

def llmotpt():
    response = ollama.chat(model='llama3.1', messages=[{
        'role': 'user',
        'content': """
        You are a video editing system that will be using moviePy a Python package to edit videos programmatically.
        You will be given python functions, your goal is to determine the said functions' arguments/parameters from the user input.
        Python code:
        ```py

        from moviepy.editor import *

        clip=VideoFileClip(r"/home/cyber/Desktop/dev/hackathon/rvitm/windows.mp4")

        # reduce the volume, pass the clip that is defined prior and the scaledvolume variables takes an input from 0 to 5
        def volume(clip,scaledvolume):
            clip=clip.volumex(scaledvolume)
            return clip
        
        # writes edits to a new file, takes clip/video as an input should be called at the end of every file
        def writeEnd(video,filename="Untitled.mp4"):
            video.write_videofile(filename,threads=4)

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
        def addText(text:str, fontsize:int,font:str,color:str,bg_color:str):
            txt=TextClip(text=text,fontsize=fontsize,font=font,color=color,bg_color=bg_color)
            return txt

        # adds text but with a position
        def repositionText(txt:TextClip,posstr:str=None,position:tuple[float,float]=(0,0)):
            txt = txt.set_position(posstr if posstr!=None else position)
            return txt
        

        # adds all txt and clips together to make a single video, call this when text needs to be added to a video    
        def compositeVideo(clips:list):
            video=CompositeVideoClip([clips])
            return video
        
        ```
        User Input:
        "Can you trim the clip from the 10th second to the 20th second and increase the volume by 10, also increase the speed by 2x"
        Your goal is to return the function definition and the function with the argument from the user argument.
        Eg: The following text is the only expected output, do not hallucinate and output more than required. Do not write additional code just output the required code without additional context.
        from moviepy.editor import *

        clip=VideoFileClip(r"/home/cyber/Desktop/dev/hackathon/rvitm/windows.mp4")


        def volume(clip,scaledvolume):
            clip=clip.volumex(scaledvolume)
            return clip

        def writeEnd(video,filename="Untitled.mp4"):
            video.write_videofile(filename)

        def trimClip(clip,t1,t2):
            video=clip.subclip(t1,t2)
            return video
            
        def blackAndWhite(video):
            video=video.fx(vfx.blackwhite)
            return video

        def adjustSpeed(clip, speed_factor=1.0):
            return clip.fx(vfx.speedx, speed_factor)

        def addText(text:str, fontsize:int,font:str,color:str,bg_color:str):
            txt=TextClip(text=text,fontsize=fontsize,font=font,color=color,bg_color=bg_color)
            return txt

        def repositionText(txt:TextClip,posstr:str=None,position:tuple[float,float]=(0,0)):
            txt = txt.set_position(posstr if posstr!=None else position)
            return txt

        ~~~ (output 3 tilde for the regex engine to differentiate between code and output, do not hallucinate at any cost as this is super crucial.)
        # choose functions based on user input not all functions are required to be in a file except writeEnd function
        # choose functions carefully and only do what the user tells you to do
        clip=volume(clip,5) # use only if asked
        clip = blackAndWhite(clip) #use only if asked
        clip = trimClip(clip,8,20) #use only if asked
        clip = adjustSpeed(clip,2.0) #use only if asked
        writeEnd(clip) # this should always be there at the end of the script
        Do not do output anything else, do not edit the given code in anyway just do what is told. Do not additional functions just add what is told.
        """
    }])
    return response['message']['content']

def parse_llm_response(response_text: str):
    parts = response_text.strip().split('~~~')
    if len(parts) != 2:
        raise ValueError("Invalid response format: missing ~~~ delimiter")
    function_def = parts[0].strip()
    function_call = parts[1].strip()
    return function_def, function_call

def main():
    max_attempts = 10  # Maximum number of attempts to prevent infinite loops
    attempt = 0
    success = False

    while not success and attempt < max_attempts:
        try:
            x = llmotpt()
            y = parse_llm_response(x)
            funcdef = y[0]
            funcout = y[1]
            
            with open('executer.py', 'w') as f:
                f.write(str(funcdef) + '\n' + str(funcout))
            
            result = subprocess.run(["python3", 'executer.py'], 
                                  capture_output=True, 
                                  text=True)
            
            if result.returncode == 0:
                success = True
                
                print(result.stdout)
            else:
                print(f"Attempt {attempt + 1} failed with error: {result.stderr}")
                
        except Exception as e:
            print(f"Attempt {attempt + 1} failed with error: {str(e)}")
        
        if not success:
            attempt += 1
            time.sleep(1)  # Add a small delay between attempts
    
    if not success:
        print(f"Failed after {max_attempts} attempts")

if __name__ == "__main__":
    main()
