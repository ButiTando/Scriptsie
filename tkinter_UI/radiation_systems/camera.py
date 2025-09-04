import cv2
import threading
import time


class Test_Camera:
    CAM_TAG = {
        "stream_load_error": "CAM_NO_CONN",
        "rtsp_connection_successful": "CAM_OK",
        "rtsp_connection_closed": "CAM_CLOSE",

    }

    def __init__(self, rtsp_url):
        self.rtsp_url = rtsp_url
        self.cap = None
        self.latest_frame = None
        self.lock = threading.Lock()
        self.runing = False
        self.thread = None

    def caputure(self):
        """
        Initiating OpenCV capture and starting capture thread in daemon mode.
        """

        self.cap = cv2.VideoCapture(self.rtsp_url)
        
        # Check if stream connection successful
        if not self.cap.isOpened():
            # raise Exception(self.CAM_TAG["steam_load_error"])
            return f'{self.CAM_TAG["stream_load_error"]}: Failed to connect to {self.rtsp_url}'     
        
        self.runing = True
        self.thread = threading.Thread(target=self._grab_frames, daemon=True)
        self.thread.start()
        return f'{self.CAM_TAG["rtsp_connection_successful"]}: Successful connection to {self.rtsp_url}'
    
    def _grab_frames(self):
        # Continously grab frames
        while self.running:
            ret, frame = self.cap.read()

            if ret:
                with self.lock:
                    self.latest_frame = frame

            else:
                print("Failed to grab frame")
            # Limit requests to 30fps
            time.sleep(0.033)

    #Public: Function to get the latest frame
    def get_latest_frame(self):
        with self.lock:            
            if self.latest_frame != None:
                return self.latest_frame.copy()
            else:
                return None
            
    # Stopping feed and killing thread.
    def stop(self):
        self.running = False

        if self.thread:
            self.thread.join()

        if self.cap:
            self.cap.release()

        return f'{self.CAM_TAG["rtsp_connection_closed"]}: Camera feed closed.'
            


