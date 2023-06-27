from pathlib import Path

import whisper
import zlib
from typing import Iterator, TextIO

from whisper.utils import write_srt

# load the best model
model = whisper.load_model("large")

def transcription_translated(audio_file_path):

    result = model.transcribe(audio_file_path)
    # returns english translation text
    return result["text"]


print(transcription_translated(	" سنخوذ معاركنا معهم وسنمض جموعا نردعهم ونعيد الحق المغتصب وبكل القوة ندفعهم سنخوذ معاركنا معهم وسنمض جموعا نردعهم ونعيد الحق المغتصب وبكل القوة ندفعهم بسلاح الحق البتاري سنحرر أرض الأحرار ونعيد الطهر إلى القدس من بعد الظل وبنار بسلاح الحق البتاري سنحرر أرض الأحرار ونعيد الطهر إلى القدس من بعد الظل وبنار سنخوذ معاركنا معهم وسنمض جموعا نردعهم ونعيد الحق المغتصب وبكل القوة ندفعهم وسنمض ندفك معاقلهم بدوي دام يقلقهم وسنمح العار بأيدينا وبكل القوة نردعهم وسنمض ندفك معاقلهم بدوي دام يقلقهم وسنمح العار بأيدينا وبكل القوة نردعهم سنخوذ معاركنا معهم وسنمض جموعا نردعهم ونعيد الحق المغتصب وبكل القوة ندفعهم لن نرضى بجزء محتل لن نترك شبرا للذل ستمور الأرض وتحرقهم في الأرض براكين تغني لن نرضى بجزء محتل لن نترك شبرا للذل ستمور الأرض وتحرقهم في الأرض براكين تغني سنخوذ معاركنا معهم وسنمض جموعا نردعهم ونعيد الحق المغتصب وبكل القوة ندفعهم لن نرضى بجزء محتل لن نترك شبرا للذل ستمور الأرض وتحرقهم في الأرض براكين تغني لن نرضى بجزء محتل لن نترك شبرا للذل ستمور الأرض وتحرقهم في الأرض براكين تغني سنخوذ معاركنا معهم وسنمض جموعا نردعهم ونعيد الحق المغتصب وبكل القوة ندفعهم سنخوذ معاركنا معهم وسنمض جموعا نردعهم ونعيد الحق المغتصب وبكل القوة ندفعهم"))



def transcription_srt(audio_file_path):

    result = model.transcribe(audio_file_path, task='translate')
    # save SRT
    audio_basename = Path(audio_file_path).stem
    with open(Path("srtdir") / (audio_basename + ".srt"), "w", encoding="utf-8") as srt:
        write_srt(result["segments"], file=srt)
#generate srt file for translation
#transcription_srt("audio/foot.mp4")

#_, probs = model.detect_language("audio/foot.mp4")
#print(f"Detected language: {max(probs, key=probs.get)}")

#for the audio file ffmpeg it accept mp3 or mp4 so no need to convert the video to mp3
#print(transcription_translated("audio/foot.mp4"))

