class Algorithm:
     def __init__(self):
     # fill your init vars
         self.buffer_size = 0
         self.rebuf_time = [0] * 20
     # Intial 
     def Initial(self):
         self.buffer_size = 0

     #Define your al
     def run(self, S_time_interval, S_send_data_size, S_frame_time_len, S_frame_type, S_buffer_size, S_end_delay, rebuf_time, cdn_has_frame,cdn_flag, buffer_flag):
         self.rebuf_time.append(rebuf_time) 
         self.rebuf_time.pop(0)
         if S_buffer_size[-1] > 1.0:
             bit_rate = 1
         else:
             bit_rate = 0
         if sum(self.rebuf_time) < 0.001 and bit_rate == 0:
             bit_rate = 1
         target_buffer = 1.5
         return bit_rate, target_buffer


