import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
import scipy.signal as signal

# Tạo nhiều tín hiệu đầu vào
fs = 1000  # Tần số lấy mẫu
t = np.linspace(0, 1, fs, endpoint=False)  # Thời gian từ 0 đến 1 giây
frequencies = [5, 10, 20]  # Danh sách tần số của các tín hiệu đầu vào
signals = [np.sin(2 * np.pi * f * t) for f in frequencies]

# Biến đổi Fourier và hiển thị
plt.figure(figsize=(10, 6))
for i, x in enumerate(signals, 1):
    X = fft(x)
    freqs = fftfreq(len(x), 1/fs)

    plt.subplot(len(signals), 2, 2*i-1)
    plt.plot(t, x)
    plt.title(f'Tín hiệu {i}')

    plt.subplot(len(signals), 2, 2*i)
    plt.plot(freqs, np.abs(X))
    plt.title(f'Biến đổi Fourier - Tín hiệu {i}')
    plt.xlabel('Tần số (Hz)')

plt.tight_layout()
plt.show()

# Biến đổi Z cho mỗi tín hiệu
plt.figure(figsize=(10, 6))
for i, x in enumerate(signals, 1):
    system = signal.TransferFunction([1], [1, -0.5])  # Ví dụ: Hệ số của hàm truyền của bạn
    time, response, _ = signal.lsim(system, x, t)

    plt.subplot(len(signals), 2, 2*i-1)
    plt.plot(t, x)
    plt.title(f'Tín hiệu {i}')

    plt.subplot(len(signals), 2, 2*i)
    plt.plot(time, response)
    plt.title(f'Biến đổi Z - Tín hiệu {i}')
    plt.xlabel('Thời gian')

plt.tight_layout()
plt.show()
