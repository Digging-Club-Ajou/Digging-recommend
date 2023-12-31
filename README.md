# Digging_recommend
디킹클럽 추천시스템 개발을 위한 소스코드 관리용입니다.
본 서비스의 ML process는 다음과 같습니다.

## 개발 프로세스
### 1. 데이터 수집
1만 곡에 가까운 데이터셋을 구축하였으며, 국내곡부터 해외가수까지 데이터셋을 구축하였음.
데이터셋의 정보로는 아티스트에 관한 데이터셋과 곡에 관한 데이터셋이 존재하며, 아티스트는 장르, 활동년대, 성별, 그룹, 국가 등의 정보가 저장되어 있으며, 곡 정보 데이터셋은 아티스트 데이터셋 기반 아티스트명, 앨범명, 곡명, 좋아요 수가 존재한다. 

#### 1-1. 데이터셋 구성도
* 1104artist.csv - 아티스트에 관한 데이터셋
* 1105_song.csv - 곡 정보에 관한 데이터셋

### 2. 데이터 전처리
데이터의 결측치나 정규화 작업, 데이터의 패턴 파악을 위해 세그먼트화나 클러스터링이 가능함
### 3. 모델링 및 학습/적용
* 협업 핕터링: 사용자와 아이템 간의 상호 작용 기반으로 추천합니다. 사용자 기반(User-based)과 아이템 기반(Item-based) 방식이 있음
* 콘텐츠 기반 필터링: 음악 아이템의 특징과 사용자의 프로필을 기반으로 추천하는 방식이 있음

위 두 방식을 사용하여 딥러닝이나 ML 모델을 활용하여 패턴을 학습할 수 있음
### 4. 모델 평가 및 최적화
개발팀 내 A/B 테스트를 통해 실제 사용자 환경에서의 추천 성능을 비교 및 평가할 수 있음
### 5. 서비스 내 탑재
개발팀 내 피드백 과정을 통해 어플리케이션과 추천 시스템을 연결하여 서비스를 탑재할 수 있음
