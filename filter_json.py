import json

from scipy import signal


class FilterJson:

    temp_data = None

    def __init__(self, origin_data, filter_list_json, frequency):
        self.temp_data = origin_data
        self.filter_list = json.loads(filter_list_json)
        self.frequency = frequency

    def run(self):
        for filter_json in self.filter_list:
            for key in filter_json.keys():
                filter_info = filter_json[key]
                if key == 'notch':
                    filter_frequency = filter_info['filter_frequency']
                    self.temp_data = self.exg_notch_filter(self.temp_data, filter_frequency)
                elif key == 'bandpass':
                    filter_min_frequency = filter_info['filter_min_frequency']
                    filter_max_frequency = filter_info['filter_max_frequency']
                    self.temp_data = self.exg_bandpass_filter(self.temp_data, filter_min_frequency, filter_max_frequency)
        return self.temp_data

    def exg_notch_filter(self, exg_data, removed_notch_hz):
        fs = self.frequency  # Sample frequency (Hz)
        f0 = removed_notch_hz  # Frequency to be removed from signal (Hz)
        q_notch = 30  # Quality factor
        w0 = f0 / (fs / 2)  # Normalized Frequency
        c, d = signal.iirnotch(w0, q_notch)
        eeg_notch_filtered = signal.filtfilt(c, d, exg_data)  # the eeg data we want
        return eeg_notch_filtered

    def exg_bandpass_filter(self, exg_data, low, high):
        # bandpass filter
        # 这里假设采样频率为1000hz,信号本身最大的频率为500hz，要滤除10hz以下和400hz以上频率成分
        # 即截至频率为10hz和400hz,则wn1=2*10/1000=0.02,wn2=2*400/1000=0.8。Wn=[0.02,0.8]
        # 采样频率：250
        w_min = 2.0 * low / self.frequency
        w_max = 2.0 * high / self.frequency
        b, a = signal.butter(4, [w_min, w_max], 'bandpass')  # 250Hz sample, 125Hz EEG.
        eeg_bp_filtered = signal.filtfilt(b, a, exg_data)
        return eeg_bp_filtered
