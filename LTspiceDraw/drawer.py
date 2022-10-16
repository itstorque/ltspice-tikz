class Drawer:
    
    def __init__(self, asc_path) -> None:
        self.asc_file_path = asc_path
        
        self.read_asc()
        
    def read_asc(self):
        self.asc_file_path