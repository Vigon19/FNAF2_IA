class AnimPaths:
    def __init__(self):
        self.anim_location={
         "toy_freddy":[9,10,0],
         "toy_chica":[9,7,4,1,5,0],
         "toy_bonnie":[9,3,4,2,6,0],
         "withered_bonnie":[8,7,1,5,0],
         "withered_chica":[8,4,2,6,0],
         "withered_foxy":[8,0],
         "withered_freddy":[8,7,3,0],
         "balloon_boy":[10,5,0],
         "mangle":[12,11,10,7,6,1,2,0],
         "puppet":[11,0],
        }
    def check_location(self, anim,num_camera):
        if num_camera in self.anim_location[anim]:
            return True
        else: return False