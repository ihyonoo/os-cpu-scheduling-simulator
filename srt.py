# srt.py
# SRT 스케줄링 알고리즘

import time
from print_console import print_console_result

def run_srt(processes): 
    ready_queue = sorted(processes, key=lambda p: p.arrival_time)   # 도착 시간 순으로 Ready Queue 정렬
    completed = []          # 완료 상태 저장 공간
    running_process = None  # 실행 프로세스
    gantt_log = []          # Time Out 시에 로그 추가
    current_start = None    # 해당 디스패치의 시작 시간

    sum_waiting_time = 0
    sum_response_time = 0
    sum_return_time = 0
    

    print("SRT 시뮬레이션 시작...")
   
    # 경과 시간 카운트
    elapsed = 0   

    # Ready Queue에 아직 프로세스가 남아 있거나 실행중인 프로세스가 있으면 반복
    while ready_queue or running_process:

        print(f"{elapsed}m/s")  # 출력

        if running_process is not None: # 실행중인 프로세스가 있다면    

            # 실행 중인 프로세스의 Time Slice와 남은 작업 시간을 감소
            running_process.time_slice -= 1
            running_process.remaining_time -= 1

            # 만약 남은 작업시간이 0이라면
            if running_process.remaining_time == 0: 

                # 로그 추가
                gantt_log.append((running_process.pid, current_start, elapsed))

                # 종료 시간 기록
                running_process.finish_time = elapsed
                # 반환 시간 기록
                running_process.return_time = elapsed - running_process.arrival_time
                # 대기 시간 기록
                running_process.waiting_time = running_process.return_time - running_process.service_time

                # 출력
                print(f"{elapsed}m/s: {running_process.pid} 실행 종료")
            

                # 평균 시간 계산을 위한 누적 로직
                sum_response_time += running_process.response_time
                sum_return_time += running_process.return_time
                sum_waiting_time += running_process.waiting_time
                
                # 실행 완료 큐에 추가
                completed.append(running_process)

                # 실행 중인 프로세스를 없앤다.
                running_process = None

            # 타임슬라이스의 시간을 모두 소모하였다면
            elif running_process.time_slice == 0:
                    
                # 로그 추가
                gantt_log.append((running_process.pid, current_start, elapsed))
                        
                # time_slice 초기화
                running_process.time_slice = running_process.default_time_slice

                # 출력
                print(f"{elapsed}m/s: {running_process.pid} Time Out")

                # Ready Queue에 되돌려 보낸다.
                ready_queue.append(running_process)
                    
                # 실행 중인 프로세스를 없앤다.
                running_process = None
            


        # 실행중인 프로세스가 없다면
        if running_process is None:

            # 도착한 프로세스들을 후보로
            candidates = [p for p in ready_queue if p.arrival_time <= elapsed]

            # 후보들이 존재한다면(도착한 프로세스가 있다면)
            if candidates:

                # 남은 작업 시간이 가장 적은 프로세스를 선택
                shortest = min(candidates, key=lambda p: p.remaining_time)

                # Dispatch
                ready_queue.remove(shortest)
                running_process = shortest  

                # 처음 디스패치 된 프로세스라면
                if running_process.start_time is None:
                    # 프로세스 시작 시간 기록  
                    running_process.start_time = elapsed
                    # 프로세스 응답 시간 기록
                    running_process.response_time = elapsed - running_process.arrival_time

                # 현재 디스패치 과정의 시작 시간 기록
                current_start = elapsed

                # 출력
                print(f"{elapsed}m/s: {running_process.pid} 실행 시작")

        # 1초 경과 (루프 당 1초 씩 증가)
        elapsed += 1
        time.sleep(0.001)


    # 결과 출력
    print_console_result(completed, sum_waiting_time, sum_response_time, sum_return_time)

    return completed, gantt_log