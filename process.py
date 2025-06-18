# process.py

class Process:
    def __init__(self, pid, arrival_time, service_time, priority, time_slice):
        self.pid = pid
        self.arrival_time = arrival_time
        self.service_time = service_time
        self.priority = priority
        self.time_slice = time_slice
        
        self.default_time_slice = time_slice


        self.start_time = None              # 시작 시간
        self.finish_time = None             # 종료 시간
        self.waiting_time = None            # 대기 시간
        self.response_time = None           # 응답 시간
        self.return_time = None             # 반환 시간
        self.remaining_time = service_time  # 남은 작업 시간