# Display STFT of an audio recording
import os

import matplotlib
import numpy as np
import matplotlib.pyplot as plt

import librosa   # read audio files
import sounddevice as sd  # play audio

import scipy.signal as scisig  # stft

from matplotlib.animation import FuncAnimation
ffmpeg_path = "path/to/ffmpeg"
matplotlib.rcParams['animation.ffmpeg_path'] = ffmpeg_path


def gen_spectrogram(params):
    """
    slowrate : if necessary, slow the audio recording
    """
    def_name = params['name']
    audio_file = 'assets/sons_spectro/' + params['file']
    plt.close('all')

    # Load audio signal
    signal, fs = librosa.load(audio_file, sr=None)

    # default parameters
    contrast = 100
    slowrate = 1
    freqmax = 3000
    sig_start = 0
    sig_end = len(signal) / fs

    if 'range' in params.keys():
        sig_start = params['range'][0]
        sig_end_ = params['range'][1]
        if sig_end_ < sig_end:
            sig_end = sig_end_

    if 'slowrate' in params.keys():
        slowrate = params['slowrate']
    if 'contrast' in params.keys():
        contrast = params['contrast']
    if 'max_freq' in params.keys() and params['max_freq'] is True:
        freqmax = fs / 2

    signal = signal[int(sig_start * fs):int(sig_end * fs)]
    winlength = 2048
    nfft = 2*winlength

    # STFT
    overlap = np.round(.9*winlength)
    f_tf, t_tf, stft = scisig.stft(signal, fs=fs, nperseg=winlength, nfft=nfft, noverlap=overlap)
    dt_tf = t_tf[1]-t_tf[0]

    # Figure
    #spectro_tr = np.log1p(contrast*np.abs(stft))  # log1p scaling
    spectro_tr = 20 * np.log10(np.abs(stft))  # spectrogram in dB
    s_min = np.min(spectro_tr)
    s_max = np.max(spectro_tr)
    #return s_min, s_max

    # Create figure and add axes
    fig_shape = (14, 8)
    fig = plt.figure(figsize=fig_shape)
    ax = fig.add_subplot(111, ylim=(0, freqmax/slowrate))
    ax.set_xlabel('Temps (s)')
    ax.set_ylabel('Fréquence (Hz)')

    # Create variable reference to plot
    #spectro_1pc = ax.pcolormesh(slowrate*t_tf, f_tf/slowrate, spectro_1pc, cmap='Reds')
    vmin = -100
    vmax = 0
    spectro_tr = ax.pcolormesh(slowrate*t_tf, f_tf/slowrate, spectro_tr, cmap='viridis', vmin=vmin, vmax=vmax)
    color_vlin = '#FFDDCCFF'
    trace = ax.axvline(0, color=color_vlin, lw=2)

    # Animation function
    def_fps = 25
    len_sig = len(t_tf)
    print("len_sig: ", len_sig)
    step_fps_float = ((1.0/slowrate * 1.0/dt_tf) / def_fps)
    print("step_fps_float: ", step_fps_float)

    def animate(i):
        index_t = int(round(i * step_fps_float))
        xt = slowrate*t_tf[index_t]
        trace.set_xdata([xt, xt])
        return [trace]

    # Create animation
    inter_frame_ms = int(1000/def_fps)
    nb_frames = int(len_sig/step_fps_float)
    print("nb_frames: ", nb_frames)
    ani = FuncAnimation(fig=fig, func=animate, frames=nb_frames, interval=inter_frame_ms, repeat=False, blit=True)
    video_file_mute = "tmp.mp4"
    ani.save(filename=video_file_mute, writer='ffmpeg', fps=def_fps)

    audio_cut = "tmp.mp3"
    cmd = f"{ffmpeg_path} -y -i {audio_file} -ss {sig_start} -to {sig_end} {audio_cut}"
    print(cmd)
    os.system(cmd)

    audio_out = audio_cut
    if slowrate != 1:
        audio_out = "tmp_slow.mp3"
        cmd = f"{ffmpeg_path} -y -i {audio_cut} -filter:a \"atempo={1.0/slowrate}\" {audio_out}"
        os.system(cmd)

    video_file = "assets/video/" + def_name + ".mp4"
    cmd = f"{ffmpeg_path} -y -i {video_file_mute} -i {audio_out} -map 0:v -map 1:a -c:v copy -shortest {video_file}"
    print(cmd)
    os.system(cmd)

    return s_min, s_max


def gen_set():
    data_vec = [
        {'name': 'wolf', 'file': 'wolf_howl.mp3', 'range': [4, 6]},
        {'name': 'dolphin', 'file': 'dolphin.wav', 'slowrate': 2, 'max_freq': True},
        {'name': 'bell', 'file': 'bell.wav', 'range': [0, 3]},
        {'name': 'guitar', 'file': 'guitar.wav', 'range': [0, 5.5]},
        {'name': 'output', 'file': 'output.wav', 'range': [0, 4]},
    ]

    data_vec = []

    for i in range(1, 71):
        name = str(i)
        if i < 10:
            name = "0" + str(i)
        d = {'name': name, 'file': "SQAM_FLAC_00s9l4/" + name + ".flac", 'range': [0, 4]}
        data_vec.append(d)

    for data in data_vec:
        r = gen_spectrogram(data)


if __name__ == '__main__':
    gen_set()
