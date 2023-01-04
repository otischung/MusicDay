"""
Provides some librosa functions
"""
import sys

import librosa
import numpy as np


def ref_pitch(src: str, fmin: int | str = "G2", fmax: int | str = "C6", noise_gate: bool = True, sr: int = 44100, frame_len: int = 8000, num_cont_frame: int = 5) -> list:
    """
    Get the five reference pitch of given source audio file.

    You can specify the minimum and maximum frequencies by MIDI integer value
    or note name string, e.g. "C#3", "Ab4".

    Parameters
    ----------
    src: str
        Input audio file path.

    fmin: int|str
        The minimum frequency. The default value is G2 (43)

    fmax: int|str
        The maximum frequency. The default value is C6 (84)

    noise_gate: bool
        The default value is True. It will detect blanks and delete the blank parts.

    sr: int
        Sample rate. The default value is 44.1kHz, which is the standard of CD quality.

    frame_len: int
        This value determines that how many frames will be used in FFT. The default value is 8000.
        This value also determines the segment length. Take our default values for example,
        the segment length is 8000 / 44100 * 1000 = 181.4059 ms.

    num_cont_frame: int
        This value sets the numbers of continuous frame that are all same pitch.
        The default value is 5 frames.
        For example, [69, 69, 69, 69, 69, 70, ...], then 69 (A4) will be accepted.
        On the contrary, [69, 70, 71, 72, 73, ...], then all pitches will be rejected.

    Returns
    -------
    out: list
        The list containing five reference pitch. The order is [low, avg. low, avg., avg high, high].

    Raises
    ------
    FileNotFoundError
        If the given source audio file doesn't exist.

    ParameterError
        If the input frequencies are not in valid note format.
    """
    y0, sr = librosa.load(src, sr=sr)  # y0 is the time domain of the music read in RAM; sr is the sample rate.
    # ------ Perform Noise Gate -----
    if noise_gate:
        n_fft = frame_len
        S = librosa.stft(y0, n_fft=n_fft, hop_length=n_fft // 2)
        D = librosa.amplitude_to_db(np.abs(S), ref=np.max)
        np.max(abs(D))

        nonMuteSections = librosa.effects.split(y0, top_db=20)
        # y will be the voice without blank.
        y = []

        for sliced in nonMuteSections:
            y.extend(y0[sliced[0]:sliced[1]])
    else:
        y = y0
    # -------------------------------

    # Transfer to numpy array.
    y = np.array(y)

    if type(fmin) == str:
        fmin = librosa.note_to_midi(fmin)
    if type(fmax) == str:
        fmax = librosa.note_to_midi(fmax)
    # This will take few times.
    # f0 is the detected fundamental frequencies based on time sequence.
    f0, voiced_flag, voiced_probabilities = librosa.pyin(
        y, sr=sr, frame_length=frame_len,
        fmin=librosa.midi_to_hz(fmin), fmax=librosa.midi_to_hz(fmax))

    appear = []
    midi_note = np.around(librosa.hz_to_midi(f0))
    i = len(midi_note) - 1

    histogram = [0] * 128
    while i >= 0:
        if midi_note[i] != 'nan':
            is_a_note = True
            for t in range(num_cont_frame):
                if midi_note[i - t - 1] != midi_note[i]:
                    is_a_note = False
                    break
            if is_a_note:
                appear.append(midi_note[i])
                histogram[int(midi_note[i])] += 1
                i -= num_cont_frame
            else:
                i -= 1

    if len(appear) == 0:
        print(f"Error, the music {src} has zero note.", file=sys.stderr)
        return [0, 0, 0, 0, 0]

    # This will take few times.
    # appear.sort()

    # Unstable counting sort
    appear_sort = []
    for i in range(128):
        for j in range(histogram[i]):
            appear_sort.append(i)

    # 5 index
    # print("average", librosa.midi_to_note(appear[(int)(len(appear) / 2)]))
    # print("average high", librosa.midi_to_note(appear[(int)(3 * len(appear) / 4)]))
    # print("average low", librosa.midi_to_note(appear[(int)(len(appear) / 4)]))
    # print("low", librosa.midi_to_note(appear[(int)(len(appear) / 100)]))
    # print("high", librosa.midi_to_note(appear[(int)(98 * len(appear) / 100)]))
    low = int(appear_sort[int(len(appear_sort) / 100)])
    avg_low = int(appear_sort[int(len(appear_sort) / 4)])
    avg = int(appear_sort[int(len(appear_sort) / 2)])
    avg_high = int(appear_sort[int(3 * len(appear_sort) / 4)])
    high = int(appear_sort[int(98 * len(appear_sort) / 100)])
    # high = int(appear[int(len(appear) - 2)])
    return [low, avg_low, avg, avg_high, high]