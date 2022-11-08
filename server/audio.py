import librosa, librosa.display
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
from scipy.stats import ttest_ind
import matplotlib.patheffects as path_effects
import acoustid
import chromaprint
import seaborn as sns
from fuzzywuzzy import fuzz
from boto3.session import Session

ACCESS_KEY_ID = 'AKIARXQBP2ZVIIEGC2VH'
SECRET_KEY = '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'

session = Session(aws_access_key_id = ACCESS_KEY_ID, aws_secret_access_key = SECRET_KEY)

s3 = session.resource('s3')

bucket = 'audio-already-upload'

my_bucket = s3.Bucket(bucket)

print("Downloading from S3......")

my_bucket.download_file('audioaccelarate','C:/Users/HarshGupta/Desktop/Audio_user/Accelerating/accelarate.wav')
my_bucket.download_file('audiodeaccelarate','C:/Users/HarshGupta/Desktop/Audio_user/Deaccelerating/deaccelarate.wav')

print("Downloaded successfully from s3....")

text_file = open("C:/Users/HarshGupta/Desktop/Name.txt", "r")
data = text_file.read() 
text_file.close()
 
for filen in os.listdir("C:/Users/HarshGupta/Desktop/Audio_org/Accelerating/"):
    if(data + ".wav" in filen):
      file1 = "C:/Users/HarshGupta/Desktop/Audio_org/Accelerating/"+data+".wav"

# file2 = "C:/Users/HarshGupta/Desktop/Audio_user/Accelerating/" + data + ".wav"
file2 = "C:/Users/HarshGupta/Desktop/Audio_user/Accelerating/accelarate.wav"

signal,sr=librosa.load(file1, sr=22050)

class AudioAnalyzer:
    def __init__(self, filename, fft_size=256, input_sr=41000, analyze=True):
        y, sr = librosa.load(filename, sr=input_sr)
        self.y = y
        self.sr = sr
        self.fft_size = fft_size
        if analyze:
            self.spectrum_analysis()
        
    def change_fft_bin_size(self, size):
        self.fft_size = size
        self.spectrum_analysis()
        
    def spectrum_analysis(self):
        self.df = pd.DataFrame(np.abs(librosa.stft(self.y, n_fft=self.fft_size)))
        bins = librosa.fft_frequencies(sr=self.sr, n_fft=self.fft_size)
        self.df['bins'] = bins / 1000.
        self.df['average_amplitude'] = self.df.mean(axis=1)
        self.df = self.df[['bins', 'average_amplitude']]
        return self.df
    
    def plot_spectrum(self, min_freq=0, max_freq=None, fill=False, title="Spectrogram - Average Frequency"):
        max_freq = max_freq or 20000.
        window = self.df.loc[(self.df.bins * 1000. >= min_freq) & (self.df.bins * 1000. <= max_freq)].copy()
        window['scaled_amplitude'] = np.interp(window.average_amplitude, (0., max(window.average_amplitude)), (0., 1.))
        window.plot(x='bins', y='scaled_amplitude', figsize=(16,4))
        if fill:            
            plt.fill_between(self.df.bins, self.df.average_amplitude)
        legend = plt.legend()
        legend.remove()
        plt.xlabel("Frequency (kHz)", fontsize=20)
        plt.ylabel("Amplitude (scaled)", fontsize=20)
        plt.title(title, fontsize=26)

original_acc = AudioAnalyzer(file1, input_sr=44100, fft_size=44100)
user_acc = AudioAnalyzer(file2, input_sr=44100, fft_size=44100)

class SpectrumCompare():
    
    def __init__(self, original, modified):
        self.original_df = original.df
        self.modified_df = modified.df
        
        self.dfs = [self.original_df, self.modified_df]
        
        self.get_max_average(self)
        self.scale_amplitudes(self)
        self.get_ratio_df(self)
    
    def plot_spectrum_group(self,
                            spec_1=True,
                            spec_2=True,
                            title="Comparison of Frequency Amplitudes",
                            xlabel="Frequency (kHz)",
                            ylabel="Scaled Amplitude",                             
                            frange=None,
                            ratio=False,
                            legend=["Spectrum 1", "Spectrum 2", "Signal Diff.", "Threshold"],
                            threshold=False,
                           ):  
        
        dfs = self.dfs.copy()
        fig = plt.figure(figsize=(16,8))
        
        if frange:
            for i, df in enumerate(dfs):
                dfs[i] = df.loc[(df.bins * 1000. >= frange[0]) & (df.bins * 1000. <= frange[1])]
        else:
            dfs = self.dfs
        
        if spec_1: plt.plot(dfs[0].bins, dfs[0].scaled_amplitude, label=legend[0], c="steelblue")
        if spec_2: plt.plot(dfs[1].bins, dfs[1].scaled_amplitude, label=legend[1], c="coral")

        if ratio:
            if frange:                
                ratio_df = self.ratio_df[(self.ratio_df.bins * 1000. >= frange[0]) & (self.ratio_df.bins * 1000. <= frange[1])]
                plt.plot(ratio_df['bins'], ratio_df['scaled_amplitude'], label=legend[2], c="forestgreen", linestyle="-.")
            else:
                plt.plot(self.ratio_df['bins'], self.ratio_df['scaled_amplitude'], label=legend[2], c="forestgreen")
        
        if threshold and frange:
            plt.plot([frange[0] / 1000, frange[1] / 1000], [0.5, 0.5], linestyle="--", label=legend[3], c="r")
        
        plt.title(title, fontsize=24)
        plt.xlabel(xlabel, fontsize=20)
        plt.ylabel(ylabel, fontsize=20) 
        plt.legend(fontsize=14)
        
    def plot_spectrum_heatmap(self, 
                               plot_spec1=True,
                               frange=[], 
                               title="Audio Comparison", 
                               cmap="plasma",
                               background_color="white",
                               background_alpha=0.5
                              ):
        if plot_spec1:
            df = self.original_df
        else:
            df = self.modified_df            

        df['ratio_amplitude'] = self.ratio_df.scaled_amplitude

        df['attenuated_scaled'] = df.scaled_amplitude
        df['boosted_scaled'] = df.scaled_amplitude
        
        if len(frange):
            plot_df = df.loc[(df.bins >= frange[0] / 1000) & (df.bins <= frange[1] / 1000)]
            ratio_df = self.ratio_df.loc[(self.ratio_df.bins >= frange[0] / 1000) & (self.ratio_df.bins <= frange[1] / 1000)] 
        else:
            plot_df = df
            ratio_df = self.ratio_df

        fig = plt.figure(figsize=(20,10))
        ax1 = fig.add_subplot(211, facecolor="white")
        ax2 = fig.add_subplot(211, facecolor="#00000000")
        cbaxes = plt.subplot2grid((16,1), (10,0)) 
        cbaxes.set_title("Scaled Amplitude Ratio", size=14)
        
        sns.heatmap(data=ratio_df.set_index('bins').transpose(), cbar=True, cbar_ax=cbaxes, cbar_kws={"orientation" : "horizontal"}, cmap=cmap, alpha=0.95, zorder=1, ax=ax1, vmin=0.0, vmax=1.0)
        ax1.set_xlabel("")
        ax1.set_xticks([])
        ax1.set_ylabel("")
        ax1.set_yticks([])

        sns.lineplot(data=plot_df, x="bins", y="scaled_amplitude", color='black', zorder=10, ax=ax2, path_effects=[path_effects.SimpleLineShadow(), path_effects.Normal()])
        ax2.fill_between(x=plot_df.bins, y1=plot_df.scaled_amplitude, color='white', alpha=0.0)
        ax2.fill_between(x=plot_df.bins, y1=plot_df.scaled_amplitude, y2=1.0, color=background_color, alpha=background_alpha)

        ax2.set_xlabel("Frequency (kHz)", size=28)
        ax2.set_ylabel("Scaled Amplitude", size=28)     
        
        ax2.margins(0)
        fig.suptitle(title, size=36, y=0.95)
    
    def plot_amplitude_distributions(self, 
                                    n=10000, 
                                    size=1000,
                                    title="Amplitude Distributions",
                                    xlabel="Average Amplitude (unscaled)",
                                    ylabel="Density"
                                    ):
        amp1 = self.dfs[0].scaled_amplitude
        amp2 = self.dfs[1].scaled_amplitude

        samples_1 = []
        samples_2 = []

        for i in range(size):
            samples_1.append(np.random.choice(amp1, size=size).mean())
            samples_2.append(np.random.choice(amp2, size=size).mean())

        plt.figure(figsize=(8,6))

        sns.distplot(samples_1)
        sns.distplot(samples_2)

        plt.title(title, fontsize=18)
        plt.xlabel(xlabel, fontsize=14)
        plt.ylabel(ylabel, fontsize=14)

        t_stat, p_val = ttest_ind(samples_1, samples_2, equal_var=False)
        return pd.DataFrame([[t_stat, p_val]], columns=["T-Statistic", "P-Value"])


    @staticmethod
    def get_max_average(self):
        max_average = 0
        for df in self.dfs:
            cur_max = df.average_amplitude.max()
            max_average = cur_max if cur_max > max_average else max_average
        
        self.max_average = max_average
    
    @staticmethod
    def scale_amplitudes(self):        
        scaled_dfs = []
        for df in self.dfs:
            averaged = df['average_amplitude']
            df['scaled_amplitude'] = np.interp(averaged, (0., self.max_average), (0., 1.)) 
            scaled_dfs.append(df)            
        self.original_df, self.modified_df = scaled_dfs
        
    @staticmethod
    def get_ratio_df(self):
        
        orig_scaled = self.original_df.scaled_amplitude
        mod_scaled = self.modified_df.scaled_amplitude
        
        self.ratio_df = pd.DataFrame((mod_scaled - orig_scaled) + 0.5)
        self.ratio_df['bins'] = self.original_df.bins
        
        self.ratio_df.loc[self.ratio_df.scaled_amplitude > 1.0, ['scaled_amplitude']] = 1.0
        self.ratio_df.loc[self.ratio_df.scaled_amplitude < 0.0, ['scaled_amplitude']] = 0.0

orig_to_used_acc = SpectrumCompare(original_acc, user_acc)

duration, fp_encoded = acoustid.fingerprint_file(file1)
fingerprint1, version = chromaprint.decode_fingerprint(fp_encoded)
duration, fp_encoded2 = acoustid.fingerprint_file(file2)
fingerprint2, version = chromaprint.decode_fingerprint(fp_encoded2)

similarity = fuzz.ratio(fingerprint1, fingerprint2)

total_score = similarity

for filen in os.listdir("C:/Users/HarshGupta/Desktop/Audio_org/Deaccelerating/"):
    if(data + ".wav" in filen):
      file3 = "C:/Users/HarshGupta/Desktop/Audio_org/Deaccelerating/"+data+".wav"

file4 = "C:/Users/HarshGupta/Desktop/Audio_user/Deaccelerating/deaccelarate.wav"

original_deacc = AudioAnalyzer(file3, input_sr=44100, fft_size=44100)
user_deacc = AudioAnalyzer(file4, input_sr=44100, fft_size=44100)

orig_to_used_deacc = SpectrumCompare(original_deacc, user_deacc)

duration, fp_encoded3 = acoustid.fingerprint_file(file3)
fingerprint3, version = chromaprint.decode_fingerprint(fp_encoded3)
duration, fp_encoded4  = acoustid.fingerprint_file(file4)
fingerprint4, version = chromaprint.decode_fingerprint(fp_encoded4)

similarity2 = fuzz.ratio(fingerprint3, fingerprint4)

total_score2 = similarity2;

final_score = (similarity+similarity2)/2;

with open('C:/Users/HarshGupta/Desktop/Audio_output/Final_out.txt', 'w') as f:
    print("Final Similarity Score : ", final_score, file=f)