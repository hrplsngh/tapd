import sounddevice as sd
import numpy as np
import time

sample_rate = 44100
channels = 2
block_size=1024

tap_threshold = 0.08
direction_threshold=0.20
cooldown=0.25

last_tap_time=0

def audio_callback(indata,frames,time_info,status):
    global last_tap_time

    if status:
        print("audio status: ",status)

    left=indata[:,0]
    right=indata[:,1]

    left_rms=np.sqrt(np.mean(left**2))
    right_rms=np.sqrt(np.mean(right**2))

    volume=max(left_rms,right_rms)
    cur_time=time.time()

    if volume<tap_threshold:
        return

    if cur_time-last_tap_time<cooldown:
        return

    last_tap_time=cur_time

    total=left_rms+right_rms
    
    if total==0:
        return

    diff=(left_rms-right_rms)/total

    if diff>direction_threshold:
        print("from left")

    elif diff<-direction_threshold:
        print("from right")

    else:
        print("center")

# checking where the sound is coming from

# def audio_callback(indata, frames, time_info, status):
#     if status:
#         print("Audio status:", status)

#     left = indata[:, 0]
#     right = indata[:, 1]

#     left_rms = np.sqrt(np.mean(left ** 2))
#     right_rms = np.sqrt(np.mean(right ** 2))

#     total = left_rms + right_rms

#     if total == 0:
#         return

#     diff = (left_rms - right_rms) / total

#     print(
#         f"L={left_rms:.4f} | "
#         f"R={right_rms:.4f} | "
#         f"DIFF={diff:.4f}"
#     )

print("starting mic.....")
print("tap left, right or center")

devices=sd.default.device[0]
info=sd.query_devices(devices)

print("device: ",info["name"])
print("input channels: ",info["max_input_channels"])
print("sample_rate: ",info["default_samplerate"])

try:
    with sd.InputStream(samplerate=sample_rate,channels=channels,blocksize=block_size,dtype="float32",callback=audio_callback):
        while True:
            time.sleep(0.1)
except KeyboardInterrupt:
    print("\nstopped.")
except Exception as e:
    print("\n Error: ")
    print(e)

# print(sd.query_devices())
# print(sd.default.device)