
class RobotController:
    
    def __init__(self):
        self.pos = 0
        
    def go_to_home_pos(self):
        print("home")
        
    def go_to_capture_left_pos(self):
        print("left capture")
        
    def go_to_capture_right_pos(self):
        print("right capture")
        
    def go_to_bin_pos(self, bin_num):
        print("going to ", bin_num)
        