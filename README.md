## 📶오픈소스를 활용한 CSI 기반 행동 탐지 시스템 프로젝트📶</br>


### CSI(Channel State Information)
 * 서브캐리어의 부반송파에서 null부반송파, Pilot부반송파, 직교성분을 제거하는 코드부분</br>
 * 64개의 부반송파에서 실질적인 Data를 담당하는 52개의 부반송파 성분이 추출되어야 성공적으로 전처리가 완료된 것

### Nexmon 기본 셋팅 방법
 * 셋팅 조건
> Raspberry Pi: Raspberry Pi 4B</br>
> Raspberry Pi OS : Raspbian v5.10.92
* Nexmon 오픈소스 및 설치 가이드
> https://github.com/nexmonster/nexmon_csi.git</br>

### Nexcsi 기본 셋팅 설치
``` bash
pip install nexcsi
```

### 오픈소스 사용 코드

``` python
from nexcsi import decoder
import numpy as np

device = "raspberrypi"  # nexus5, nexus6p, rtac86u

# PCAP 파일 읽기
samples = decoder(device).read_pcap('C:/pcap파일 경로 지정')

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
output_file_path = 'C:/csv파일 저장 경로 지정'
with open(output_file_path, 'w') as f:
    for db_amplitudes in db_amplitudes_list:
        f.write(','.join(map(str, db_amplitudes)) + '\n')  # 각 행에 dB 값을 저장
```
