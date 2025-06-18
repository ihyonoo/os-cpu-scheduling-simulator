# hrn.py
# HRN 스케줄링 알고리즘

import time
from print_console import print_console_result


def run_hrn(processes):
    ready_queue = sorted(processes, key=lambda p: p.arrival_time)   # 도착 시간 순으로 Ready Queue 정렬
    completed = []          # 완료 상태 저장 공간
    running_process = None  # 실행 프로세스스

    sum_waiting_time = 0
    sum_response_time = 0
    sum_return_time = 0

    print("HRN 시뮬레이션 시작...")

    # 경과 시간 카운트
    elapsed = 0

    # Ready Queue에 프로세스가 남아 있거나, 실행중인 프로세스가 있다면 반복
    while ready_queue or running_process:
        
        print(f"{elapsed}m/s")
        # 실행중인 프로세스가 있다면
        if running_process is not None:

            # 경과 시간 - 프로세스 시작 시간 == 프로세스 작업 시간 이라면 (즉 프로세스가 작업을 완료 하였다면)
            if elapsed - running_process.start_time == running_process.service_time:

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

                # 완료 큐에 추가
                completed.append(running_process)

                # 실행 중인 프로세스를 없앤다.
                running_process = None

        # 실행 중인 프로세스가 없다면면
        if running_process is None:
            # 도착한 프로세스들만 후보로
            candidates = [p for p in ready_queue if p.arrival_time <= elapsed]

            # 도착한 프로세스가 있다면
            if candidates:
                
                # HRN 계산
                for p in candidates:
                    # 현재까지의 대기 시간을 계산
                    waiting_time = elapsed - p.arrival_time
                    # 공식 적용
                    p.response_ratio = (waiting_time + p.service_time) / p.service_time

                # 가장 높은 우선순위를 가진 프로세스 선택
                highest = max(candidates, key=lambda p: p.response_ratio)

                # Dispatch
                ready_queue.remove(highest)
                running_process = highest

                # 시작 시간 기록
                running_process.start_time = elapsed
                # 응답 시간 기록
                running_process.response_time = elapsed - running_process.arrival_time

                # 출력
                print(f"{elapsed}m/s: {running_process.pid} 실행 시작")
        
        # 1초 경과 (루프 당 1초 씩 증가)
        elapsed += 1
        time.sleep(0.001)

    # 결과 출력
    print_console_result(completed, sum_waiting_time, sum_response_time, sum_return_time)

    return completed