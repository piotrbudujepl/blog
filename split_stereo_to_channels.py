from pydub import AudioSegment


# Create AudioSegment from clone_from filled with silence
def clone_as_silence(clone_from: AudioSegment):
    data = b"\0" * len(clone_from.raw_data)
    return AudioSegment(data, metadata={"channels": clone_from.channels,
                                        "sample_width": clone_from.sample_width,
                                        "frame_rate": clone_from.frame_rate,
                                        "frame_width": clone_from.frame_width})


# Split stereo channels to 2 AudioSegments.
# "left_channel" will contain left channel from original audio segment in left channel and silence in the right channel.
# "right_channel" will contain opposite.
def split_stereo_channels(audio_to_split: AudioSegment):
    left_channel, right_channel = audio_to_split.split_to_mono()
    left_channel = AudioSegment.from_mono_audiosegments(left_channel, clone_as_silence(left_channel))
    right_channel = AudioSegment.from_mono_audiosegments(clone_as_silence(right_channel), right_channel)
    return left_channel, right_channel


# Do not use!!!
# This method will throw an exception if len(audio_to_split) % 1000 != 0,
# this can be avoided in some files if you will use audio_to_split.duration_in_seconds*1000 instead of length,
# but it still may fail because of frame_rate or other problems
def split_stereo_channels_native(audio_to_split: AudioSegment):
    audio_length = len(audio_to_split)
    left_channel, right_channel = audio_to_split.split_to_mono()
    left_channel = AudioSegment.from_mono_audiosegments(left_channel,
                                                        AudioSegment.silent(
                                                            audio_length,
                                                            audio_to_split.frame_rate))
    right_channel = AudioSegment.from_mono_audiosegments(
        AudioSegment.silent(audio_length, audio_to_split.frame_rate), right_channel)
    return left_channel, right_channel


audio = AudioSegment.from_file("audio.mp3")
left, right = split_stereo_channels(audio)
left.export("left.mp3")
right.export("right.mp3")
