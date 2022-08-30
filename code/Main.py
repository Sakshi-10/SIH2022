import tkinter as tk
import cv2
import numpy
import PIL.Image, PIL.ImageTk
import time
import datetime as dt
import pyaudio
from array import array
import threading
import wave
import AudioS2TWPMAnalysis as aa
import VideoEmotionAnalysis as va
import VoiceSpectroChroma as Voice
import EyeGazeAnalysis as e
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)
import interface
import text2emotion as te 

font = "courier"
fontsize = 15
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
record_on = False
frames = []
p = pyaudio.PyAudio()
stream = None
counter = 0
duration = 0

class App:
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source
        self.ok=False
        self.timer=ElapsedTimeClock(self.window)
        self.vid = VideoCapture(self.video_source)
        self.canvas = tk.Canvas(window, width = self.vid.width, height = self.vid.height)
        self.canvas.pack()
        self.btn_start=tk.Button(window, text='START RECORDING', command=self.open_camera)
        self.btn_start.pack(side=tk.LEFT)
        self.btn_stop=tk.Button(window, text='STOP RECORDING', command=self.close_camera)
        self.btn_stop.pack(side=tk.LEFT)
        self.btn_video=tk.Button(window, text='FACIAL EMOTION ANALYSIS', command=self.video_analysis)
        self.btn_video.pack(side=tk.LEFT)
        self.btn_audio=tk.Button(window, text='VOICE ANALYSIS', command=self.audio_analysis)
        self.btn_audio.pack(side=tk.LEFT)
        self.btn_eye=tk.Button(window, text='EYE GAZE ANALYSIS', command=self.eye_gaze_analysis)
        self.btn_eye.pack(side=tk.LEFT)
        self.btn_eye=tk.Button(window, text='HAND GESTURE ANALYSIS', command=self.hand_gesture)
        self.btn_eye.pack(side=tk.LEFT)
        self.btn_quit=tk.Button(window, text='QUIT', command=quit)
        self.btn_quit.pack(side=tk.LEFT)
        self.delay=10
        self.update()
        self.window.mainloop()
    
    def start_audio_analysis(self):
        global duration

        newwindow=tk.Toplevel()
        newwindow.geometry("640x480")
        newwindow.title("Audio Analysis")

        L = tk.Label(newwindow, text = "AUDIO ANALYSIS",font=("Courier", 20))
        L.pack()

        T = tk.Text(newwindow,font=("Courier", 14),height=18)
        T.pack()

        plot_button = tk.Button(newwindow, text = "Plot Spectrogram", command = Voice.Spectrogramplot, width = '14', height='1')
        plot_button.pack()    

        plot_button = tk.Button(newwindow, text = "Plot Chromagram", command = Voice.Chromagramplot, width = '14', height='1')
        plot_button.pack()      

        detected_text = aa.speech_to_text()
        s1 = "\n\nSpeech Content = "+detected_text
        T.insert(tk.END, s1)
        word_count = aa.No_of_words()
        s2 = "\n\nNumber of Words = "+str(word_count)+" Words"
        T.insert(tk.END, s2)
        s3 = "\n\nDuration of Speech = "+str(duration)+" Seconds"
        T.insert(tk.END, s3)
        wpm=aa.WPM(duration)
        s4="\n\nSpeed of Speech = "+str(wpm)+" Words Per Minute (WPM)"
        T.insert(tk.END, s4)
        tips=aa.get_tips(wpm)
        common_tips=aa.common_tips()
        s5="\n\nTips/Suggestions : \n"+tips+common_tips+"\n\n"
        T.insert(tk.END, s5)
        s6=te.get_emotion(detected_text)
        T.insert(tk.END,s6)


    def plot(self):
        global dct,cnt
        names = dct.values()
        values = cnt.values()

        newwindow2=tk.Toplevel()
        newwindow2.title("Bar Graph - Video Analysis")
        newwindow2.geometry("600x410")
        f = Figure(figsize = (15, 4),dpi = 100)
        canvas = FigureCanvasTkAgg(f,master = newwindow2)
        NavigationToolbar2Tk(canvas, newwindow2)
        ax = f.add_subplot()
        ax.bar(names,values)
        ax.set_xlabel('Emotion')
        canvas.draw()
        canvas.get_tk_widget().pack()

    def start_video_analysis(self):
        global dct,cnt
        newwindow=tk.Toplevel()
        newwindow.geometry("640x480")
        newwindow.title("Video Analysis")

        L = tk.Label(newwindow, text = "VIDEO ANALYSIS",font=("Courier", 20))
        L.pack()
        T = tk.Text(newwindow,font=("Courier", 14),height=18)
        T.pack()
        dct,cnt=va.start()
        plot_button = tk.Button(newwindow, text = "Plot Bar Graph", command = self.plot, width = '12', height='1')
        plot_button.pack()

        s1 = "\nSuggestions Based on Emotion Detected:\n"
        if cnt[0]>0:
            s1+="\nYou look "+str(cnt[0])+"% "+dct[0]+" in the recording.\n"
            if cnt[0]>10:
                s1+="Anger is a natural, and this is not necessarily a bad or inappropriate reaction. But being unreasonable or irrational can lead others around us to feel threatened or resentful and it can be a barrier to effective communication.\n"

        if cnt[1]>0:
            s1+="\nYou look "+str(cnt[1])+"% "+dct[1]+" in the recording.\n"
            if cnt[1]>10:
                s1+="Feeling disgusted may give the listeners a feeling of doubt or confusion. It is advisable to use this emotion the least or as required according to the speech content\n"

        if cnt[2]>0:
            s1+="\nYou look "+str(cnt[2])+"% "+dct[2]+" in the recording.\n"
            if cnt[2]>10:
                s1+="Everyone fears giving presentations & seminars initially, but conquering the fear is very important for an effective presentation. Know your topic, get organized, prepare well, take a deep breath, and you are ready for speaking.\n"

        if cnt[3]>0:
            s1+="\nYou look "+str(cnt[3])+"% "+dct[3]+" in the recording.\n"
            if cnt[3]>10:
                s1+="Being mentally stable and happy is important while speaking. A smile is the best way to start a speech. It relaxes you and the audience. It enhances the words you say, much like the gestures do.\n"

        if cnt[4]>0:
            s1+="\nYou look "+str(cnt[4])+"% "+dct[4]+" in the recording.\n"
            if cnt[4]>10:
                s1+="Along with all other emotions, being neutral during presentation is also required according to the mood of speaker and the speech content. Mix of emotions like happy, sad, anger makes the presentation more effective and easy to grasp for listeners.\n"

        if cnt[5]>0:
            s1+="\nYou look "+str(cnt[5])+"% "+dct[5]+" in the recording.\n"
            if cnt[5]>10:
                s1+="If you are sad, you can't put on a happy face. Your audience will be confused. It's always a good idea to understand the content, mood & age of audience beforehand for a better understanding of using right emotion at right time\n"

        if cnt[6]>0:
            s1+="\nYou look "+str(cnt[6])+"% "+dct[6]+" in the recording.\n"
            if cnt[6]>10:
                s1+="Surprise is usually quite brief and is characterized by a physiological startle response following something unexpected. This type of emotion can be positive, negative, or neutral.\n"
        
        T.insert(tk.END, s1)

    def ploteye(self):
        global right, left, center, noeyes,total
        newwindow2=tk.Toplevel()
        newwindow2.title("Bar Graph - Eye Gaze Analysis")
        newwindow2.geometry("600x410")
        f = Figure(figsize = (15, 4),dpi = 100)
        canvas = FigureCanvasTkAgg(f,master = newwindow2)
        NavigationToolbar2Tk(canvas, newwindow2)
        ax = f.add_subplot()
        names=["Center","Right","Left","Not Visible"]
        values=[center,right,left,noeyes]
        ax.bar(names,values)
        ax.set_ylabel("% of Times")
        ax.set_xlabel("Eye Position")
        canvas.draw()
        canvas.get_tk_widget().pack()

    def start_eyegaze_analysis(self):
        global blinks, right, left, center, noeyes,total
        newwindow=tk.Toplevel()
        newwindow.geometry("640x480")
        newwindow.title("Eye Gaze Analysis")

        L = tk.Label(newwindow, text = "EYE GAZE ANALYSIS",font=("Courier", 20))
        L.pack()
        T = tk.Text(newwindow,font=("Courier", 14),height=18)
        T.pack()
        blinks, right, left, center, noeyes = e.start()
        total=right+left+center+noeyes
        plot_button = tk.Button(newwindow, text = "Plot Bar Graph", command = self.ploteye, width = '12', height='1')
        plot_button.pack()

        center=round((center/total)*100,2)
        right=round((right/total)*100,2)
        left=round((left/total)*100,2)
        noeyes=round((noeyes/total)*100,2)

        s1 = "\nSuggestions Based on Eye Movements:\n"
        if center>0:
            s1+="\nYou have looked "+str(center)+"% times at the center. Looking at center while communicating with someone on a laptop shows confidence and builds trust with the person(s) on the other side.\n"
        if left>0 or right>0:
            s1+="\nYou have looked "+str(left)+"% times at the left and "+str(right)+"% times at the right. Looking left and right while communicating on stage is very important as it builds one-to-one connect with the audience. Whereas looking here and there while communicating in an interview or on the laptop is treated negatively and potray low confidence to the interviewer/audience\n"        
        if noeyes>0:
            s1+="\nYour face was not detected/not visible to the camera for around "+str(noeyes)+"% of times. This could be due to looking up or down. Looking up or down in any scenario, on stage or on laptop is not recommended because the audience or the person(s) on the other side may feel akward due to this behaviour.\n"
        if blinks>0:
            s1+="\nYou have blinked your eyes for "+str(blinks)+" times. Recent studies show that blinking conveys a message that we can subconsciously read and understand. Conditions of stress, anxiety or fatigue can also lead to increased blinking"

        T.insert(tk.END, s1)

    def start_hand_gesture_analysis(self):
        global abs_per,nonabs_per
        newwindow=tk.Toplevel()
        newwindow.geometry("640x480")
        newwindow.title("Hand Gesture Analysis")

        L = tk.Label(newwindow, text = "HAND GESTURE ANALYSIS",font=("Courier", 20))
        L.pack()
        T = tk.Text(newwindow,font=("Courier", 14),height=18)
        T.pack()
        abs,nonabs=interface.start()
        total=abs+nonabs

        if(total==0):
            abs_per=0
        else:
            abs_per=round((abs/total)*100,2)
            

        if abs_per>25 :
            s1="\nYou look "+str(max(abs_per-25,0))+"% abusive in the recording.\n"

        if(max(abs_per-25,0))>15:
            s1+="Hey, we noticed that your behavior is very arrogant and abusive. The actions that you are depicting are against our culture. Repetitive behaviour won't be tolerated. This is not a healthy behaviour. We don't support or nuture such kind of abusive nature.\n"

        else:
            s1="\nYou look "+str(100-abs_per)+"% non abusive in the recording.\n"
            s1+="Awesome! Your behavior was polite and kind. We appreciate these actions."

        T.insert(tk.END, s1)

    def audio_analysis(self):
        t1 = threading.Thread(target = self.start_audio_analysis)
        t1.start()
    
    def eye_gaze_analysis(self):
        t2 = threading.Thread(target = self.start_eyegaze_analysis)
        t2.start()

    def hand_gesture(self):
        t3 = threading.Thread(target = self.start_hand_gesture_analysis)
        t3.start()

    def video_analysis(self):
        t3 = threading.Thread(target = self.start_video_analysis)
        t3.start()

    def start_rec(self):
        global record_on, frames, counter_label, counter
        counter = 0
        while record_on:
            data = stream.read(CHUNK)
            frames.append(data)

    def open_camera(self):
        global record_on,p, stream, counter_label
        self.ok = True
        self.timer.start()
        print("camera opened => Recording")
        frames.clear()
        stream = p.open(format=FORMAT,channels=CHANNELS,rate=RATE,frames_per_buffer=CHUNK,input=True)
        record_on = True
        if len(frames) > 0:
            frames.clear()
        t = threading.Thread(target = self.start_rec)
        t.start()

    def close_camera(self):
        self.ok = False
        self.timer.stop()
        print("camera closed => Not Recording")
        global p, CHANNELS, FORMAT, RATE, frames, record_on, counter_label, record_type, counter, stream
        record_on = False
        stream.stop_stream()
        stream.close()
        stream = None
        filename = 'audio.wav'
        wf = wave.open(filename, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        frames.clear()
        record_on = False
  
    def update(self):
        ret, frame = self.vid.get_frame()
        if self.ok:
            self.vid.out.write(cv2.cvtColor(frame,cv2.COLOR_RGB2BGR))
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tk.NW)
        self.window.after(self.delay,self.update)

class VideoCapture:
    def __init__(self, video_source=0):
        self.vid = cv2.VideoCapture(video_source)
        self.fourcc=cv2.VideoWriter_fourcc(*'XVID')
        self.vid.set(3, 1024)
        self.vid.set(4, 768)
        frame_width = int(self.vid.get(3))
        frame_height = int(self.vid.get(4))
        res=(frame_width,frame_height)
        print(self.fourcc,res)
        self.out = cv2.VideoWriter('video'+'.'+'avi',self.fourcc,10,res)
        self.vid.set(3,res[0])
        self.vid.set(4,res[1])
        self.width,self.height=res

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                return (ret, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
            else:
                return (ret, None)
        else:
            return (ret, None)

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()
            self.out.release()
            cv2.destroyAllWindows()

class ElapsedTimeClock:
    def __init__(self,window):
        self.T=tk.Label(window,text='00:00:00',font=('times', 20, 'bold'), bg='green')
        self.T.pack(fill=tk.BOTH, expand=1)
        self.elapsedTime=dt.datetime(1,1,1)
        self.running=0
        self.lastTime=''
        t = time.localtime()
        self.zeroTime = dt.timedelta(hours=t[3], minutes=t[4], seconds=t[5])

    def tick(self):
        # get the current local time from the PC
        self.now = dt.datetime(1, 1, 1).now()
        self.elapsedTime = self.now - self.zeroTime
        self.time2 = self.elapsedTime.strftime('%H:%M:%S')
        # if time string has changed, update it
        if self.time2 != self.lastTime:
            self.lastTime = self.time2
            self.T.config(text=self.time2)
        # calls itself every 200 milliseconds
        # to update the time display as needed
        # could use >200 ms, but display gets jerky
        self.updwin=self.T.after(100, self.tick)

    def start(self):
            if not self.running:
                self.zeroTime=dt.datetime(1, 1, 1).now()-self.elapsedTime
                self.tick()
                self.running=1

    def stop(self):
            global duration
            if self.running:
                self.T.after_cancel(self.updwin)
                self.elapsedTime=dt.datetime(1, 1, 1).now()-self.zeroTime
                self.time2=self.elapsedTime
                min_to_secs=int(self.elapsedTime.strftime('%M'))*60
                secs=int(self.elapsedTime.strftime('%S'))
                duration=min_to_secs+secs
                #print(duration)
                self.running=0

App(tk.Tk(),'Video Recorder')