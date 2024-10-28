from nexcsi import decoder
import numpy as np

device = "raspberrypi"  # nexus5, nexus6p, rtac86u

# PCAP 파일 읽기
samples = decoder(device).read_pcap('C:/Users/woons/OneDrive/바탕 화면/data/losup1.pcap')

# CSI 데이터를 언팩하기
csi = decoder(device).unpack(samples['csi'], zero_nulls=True, zero_pilots=True)

# dB 진폭을 저장할 리스트 초기화
db_amplitudes_list = []

# CSI 데이터에서 각 csi[0], csi[1], ..., csi[19]에 대해 반복
for index in range(len(csi)):  # csi[0]부터 csi[19]까지 반복
    csi_filtered = csi[index][(csi[index].real != 0) | (csi[index].imag != 0)]  # 0.0 + 0.j를 제외한 나머지 값 선택

    if csi_filtered.size > 0:  # 유효한 데이터가 있는 경우에만 처리
        amplitudes = np.abs(csi_filtered)  # 진폭 계산
        db_values = 20 * np.log10(np.where(amplitudes > 0, amplitudes, np.nan))  # dB로 변환
        db_amplitudes_list.append(db_values)  # dB 값을 리스트에 추가

# 결과를 CSV 파일로 저장
output_file_path = 'C:/Users/woons/OneDrive/바탕 화면/data/test2.csv'
with open(output_file_path, 'w') as f:
    for db_amplitudes in db_amplitudes_list:
        f.write(','.join(map(str, db_amplitudes)) + '\n')  # 각 행에 dB 값을 저장
