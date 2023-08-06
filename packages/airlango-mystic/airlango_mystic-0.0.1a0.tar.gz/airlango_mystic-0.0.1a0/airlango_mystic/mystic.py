import sys
import uuid
import time
import grpc
import math
import vims_pb2
import vims_pb2_grpc

import logger
log = logger.Logger('Mystic', logger.LOG_LV_DEBUG)

class Mystic(object):
	'''
	Mystic class provides common controls over Airlango Mystic drone.
	'''
	def __init__(self, server_ip='192.168.1.1'):
		self.session_uuid = uuid.uuid4().bytes
		self.server_addr = server_ip + ':10001'
		self.connected = False
		self.channel = None
		self.control_stub = None
		self.media_stub = None
		self.ready_to_motion = False
		self.running_detector = False
		self.running_human_pose = False
		self.target_is_set = False

	def set_log_level(self, level):
		'''
		Configure the minimum level for logging.
		1 - debug, 2 - info, 3 - warnning, 4 - error
		'''
		log.set_level(level)

	def connect(self):
		if not self.connected:
			self.channel = grpc.insecure_channel(self.server_addr)
			self.control_stub = vims_pb2_grpc.ControlServiceStub(self.channel)
			self.media_stub = vims_pb2_grpc.MediaServiceStub(self.channel)
			# TODO: establish the connection and and verify it works
			self.connected = True
			log.info('Connection to Mystic established')

	def disconnect(self):
		if self.connected:
			self.channel.close()
			self.connected = False
			log.info('Disconnected from Mystic')

	def take_off(self):
		log.info('Request to take off')
		try:
			response = self.control_stub.TakeOff(
				vims_pb2.TakeOffRequest(session_token_uuid=self.session_uuid))
			log.info('Server responsed status: %s'
					% (vims_pb2.VimsStatusCode.Name(response.status)))
			time.sleep(5)
			if response.status == vims_pb2.VIMS_OK:
				log.info('Take off operation succeeds')
		except:
			log.error('Request failed: %s' % (sys.exc_info()[0]))

	def land(self):
		log.info('Request to land')
		try:
			response = self.control_stub.Land(
				vims_pb2.LandRequest(session_token_uuid=self.session_uuid))
			log.info('Server responsed status: %s'
					% (vims_pb2.VimsStatusCode.Name(response.status)))
			time.sleep(10)
			if response.status == vims_pb2.VIMS_OK:
				log.info('Land operation succeeds')
				self.ready_to_motion = False
		except:
			log.error('Request failed: %s' % (sys.exc_info()[0]))

	def prepare_motion(self):
		'''
		After successful taking-off the drone, we need to tell it to
		get ready to accept our subsequent motion commands.
		'''
		log.debug('Request to setup environment for motion')
		try:
			response = self.control_stub.EnterCustomMode(
				vims_pb2.CustomModeRequest(session_token_uuid=self.session_uuid))
			log.debug('Server responsed status: %s'
					% (vims_pb2.VimsStatusCode.Name(response.status)))
			if response.status == vims_pb2.VIMS_OK:
				self.ready_to_motion = True
		except:
			log.error('Request failed: %s' % (sys.exc_info()[0]))


	def hover(self):
		try:
			response = self.control_stub.SendCustomMotion(
				vims_pb2.CustomMotionRequest(session_token_uuid=self.session_uuid,
					roll_rate=0, pitch_rate=0, yaw_rate=0, thrust=0, duration_usec=0, distance=0))
			if response.status == vims_pb2.VIMS_OK:
				print('Executing command ...')
				log.debug('done motion hover')
			else:
				log.error('motion hover not done properly')
		except:
			log.error('Reqeust failed: %s' % (sys.exc_info()[0]))


	def forward(self, velocity=0.2, duration_s=1.0, distance_m=0, wait=False):
		'''
		Move the drone in forward direction with the given distance in meters.
		'''
		if not self.ready_to_motion:
			log.warn('Mystic does not get ready to motion')
			return
		try:
			response = self.control_stub.SendCustomMotion(
				vims_pb2.CustomMotionRequest(session_token_uuid=self.session_uuid,
					roll_rate=0, pitch_rate=velocity, yaw_rate=0, thrust=0, duration_usec=int(duration_s*1e6), distance=distance_m))
			if response.status == vims_pb2.VIMS_OK:
				print('Executing command ...')
				if wait:
					time.sleep(duration_s)
				log.debug('done motion shift forward')
			else:
				log.error('motion shift forward not done properly')
		except:
			log.error('Reqeust failed: %s' % (sys.exc_info()[0]))

	def backward(self, velocity=0.2, duration_s=1.0, distance_m=0, wait=False):
		'''
		Move the drone in backward direction with the given distance in meters.
		'''
		if not self.ready_to_motion:
			log.warn('Mystic does not get ready to motion')
			return
		try:
			response = self.control_stub.SendCustomMotion(
				vims_pb2.CustomMotionRequest(session_token_uuid=self.session_uuid,
					roll_rate=0, pitch_rate=-velocity, yaw_rate=0, thrust=0, duration_usec=int(duration_s*1e6), distance=distance_m))
			if response.status == vims_pb2.VIMS_OK:
				print('Executing command ...')
				if wait:
					time.sleep(duration_s)
				log.debug('done motion shift backward')
			else:
				log.error('motion shift backward not done properly')
		except:
			log.error('Reqeust failed: %s' % (sys.exc_info()[0]))

	def leftward(self, velocity=0.2, duration_s=1.0, distance_m=0, wait=False):
		'''
		shift the drone to left with the given distance in meters.
		'''
		if not self.ready_to_motion:
			log.warn('Mystic does not get ready to motion')
			return
		try:
			response = self.control_stub.SendCustomMotion(
				vims_pb2.CustomMotionRequest(session_token_uuid=self.session_uuid,
					roll_rate=-velocity, pitch_rate=0, yaw_rate=0, thrust=0, duration_usec=int(duration_s*1e6), distance=distance_m))
			if response.status == vims_pb2.VIMS_OK:
				print('Executing command ...')
				if wait:
					time.sleep(duration_s)
				log.debug('done motion shift leftward')
			else:
				log.error('motion shift leftward not done properly')
		except:
			log.error('Reqeust failed: %s' % (sys.exc_info()[0]))

	def rightward(self, velocity=0.2, duration_s=1.0, distance_m=0, wait=False):
		'''
		shift the drone to right with the given distance in meters.
		'''
		if not self.ready_to_motion:
			log.warn('Mystic does not get ready to motion')
			return
		try:
			response = self.control_stub.SendCustomMotion(
				vims_pb2.CustomMotionRequest(session_token_uuid=self.session_uuid,
					roll_rate=velocity, pitch_rate=0, yaw_rate=0, thrust=0, duration_usec=int(duration_s*1e6), distance=distance_m))
			if response.status == vims_pb2.VIMS_OK:
				print('Executing command ...')
				if wait:
					time.sleep(duration_s)
				log.debug('done motion shift rightward')
			else:
				log.error('motion shift rightward not done properly')
		except:
			log.error('Reqeust failed: %s' % (sys.exc_info()[0]))

	def upward(self, velocity=0.2, duration_s=1.0, distance_m=0, wait=False):
		'''
		ascend the drone with the given distance in meters.
		'''
		if not self.ready_to_motion:
			log.warn('Mystic does not get ready to motion')
			return
		try:
			response = self.control_stub.SendCustomMotion(
				vims_pb2.CustomMotionRequest(session_token_uuid=self.session_uuid,
					roll_rate=0, pitch_rate=0, yaw_rate=0, thrust=velocity, duration_usec=int(duration_s*1e6), distance=distance_m))
			if response.status == vims_pb2.VIMS_OK:
				print('Executing command ...')
				if wait:
					time.sleep(duration_s)
				log.debug('done motion upward')
			else:
				log.error('motion upward not done properly')
		except:
			log.error('Reqeust failed: %s' % (sys.exc_info()[0]))

	def downward(self, velocity=0.2, duration_s=1.0, distance_m=0, wait=False):
		'''
		descend the drone with the given distance in meters.
		'''
		if not self.ready_to_motion:
			log.warn('Mystic does not get ready to motion')
			return
		try:
			response = self.control_stub.SendCustomMotion(
				vims_pb2.CustomMotionRequest(session_token_uuid=self.session_uuid,
					roll_rate=0, pitch_rate=0, yaw_rate=0, thrust=-velocity, duration_usec=int(duration_s*1e6), distance=distance_m))
			if response.status == vims_pb2.VIMS_OK:
				print('Executing command ...')
				if wait:
					time.sleep(duration_s)
				log.debug('done motion downward')
			else:
				log.error('motion downward not done properly')
		except:
			log.error('Reqeust failed: %s' % (sys.exc_info()[0]))

	def yaw_left(self, angle=0, duration_s=0.5, wait=False):
		'''
		rotate the drone to left (counter-clockwise)
		'''
		if not self.ready_to_motion:
			log.warn('Mystic does not get ready to motion')
			return
		try:
			response = self.control_stub.SendCustomMotion(
				vims_pb2.CustomMotionRequest(session_token_uuid=self.session_uuid,
					roll_rate=0, pitch_rate=0, yaw_rate=-0.2, thrust=0, duration_usec=int(duration_s*1e6), distance=angle/180.0*math.pi))
			if response.status == vims_pb2.VIMS_OK:
				print('Executing command ...')
				if wait:
					time.sleep(duration_s)
				log.debug('done motion rotate towards left')
			else:
				log.error('motion rotate towards left not done properly')
		except:
			log.error('Reqeust failed: %s' % (sys.exc_info()[0]))

	def yaw_right(self, angle=0, duration_s=0.5, wait=False):
		'''
		rotate the drone to left (clockwise)
		'''
		if not self.ready_to_motion:
			log.warn('Mystic does not get ready to motion')
			return
		try:
			response = self.control_stub.SendCustomMotion(
				vims_pb2.CustomMotionRequest(session_token_uuid=self.session_uuid,
					roll_rate=0, pitch_rate=0, yaw_rate=0.2, thrust=0, duration_usec=int(duration_s*1e6), distance=angle/180.0*math.pi))
			if response.status == vims_pb2.VIMS_OK:
				print('Executing command ...')
				if wait:
					time.sleep(duration_s)
				log.debug('done motion rotate towards right')
			else:
				log.error('motion rotate towards right not done properly')
		except:
			log.error('Reqeust failed: %s' % (sys.exc_info()[0]))

	def start_detector(self):
		if self.running_detector:
			log.info('Detector has already been started.')
			return
		log.info('Request to start detector')
		try:
			response = self.control_stub.EnterGestureMode(
				vims_pb2.GestureModeRequest(session_token_uuid=self.session_uuid))
			log.debug('Server responsed status: %s' % (vims_pb2.VimsStatusCode.Name(response.status)))
			if response.status == vims_pb2.VIMS_OK:
				self.running_detector = True
				log.info('Successfully started detector on drone.')
			else:
				log.error('Fail to start detector.')
		except:
			log.error('Request failed: %s' % (sys.exc_info()[0]))

	def stop_detector(self):
		if not self.running_detector:
			log.info('Detector has already been stopped.')
			return
		log.info('Request to stop detector')
		try:
			response = self.control_stub.LeaveGestureMode(
				vims_pb2.GestureModeRequest(session_token_uuid=self.session_uuid))
			log.debug('Server responsed status: %s' % (vims_pb2.VimsStatusCode.Name(response.status)))
			if response.status == vims_pb2.VIMS_OK:
				self.running_detector = False
				self.target_is_set = False
				log.info('Successfully stopped detector on drone.')
			else:
				log.error('Fail to stop detector.')
		except:
			log.error('Request failed: %s' % (sys.exc_info()[0]))

	def show_human_pose(self, human_id=0):
		if not self.running_detector:
			log.info('Detector must be started first.')
			return
		if self.target_is_set:
			log.info('Target is already set.')
			return
		log.info('Request to set target')
		try:
			response = self.control_stub.SetGestureTarget(
				vims_pb2.SetGestureTargetRequest(session_token_uuid=self.session_uuid, target_id=human_id))
			log.debug('Server responsed status: %s' % (vims_pb2.VimsStatusCode.Name(response.status)))
			if response.status == vims_pb2.VIMS_OK:
				self.target_is_set = True
				log.info('Successfully set target.')
			else:
				log.error('Fail to set target.')
		except:
			log.error('Request failed: %s' % (sys.exc_info()[0]))

	def get_object_info(self):
		try:
			response = self.control_stub.GetCustomObjectInfo(
				vims_pb2.CustomObjectInfoRequest(session_token_uuid=self.session_uuid))
			log.debug('Server responsed status: %s' % (vims_pb2.VimsStatusCode.Name(response.status)))
			if response.status == vims_pb2.VIMS_OK:
				boxes = response.target_rois;
				ret = []
				for box in boxes:
					ret.append([box.name, box.target_id, 
						(box.top_left_pt.x + box.bottom_right_pt.x) / 2, 
						(box.top_left_pt.y + box.bottom_right_pt.y) / 2, box.confidence])
					log.info('Found %s ID=%d at [%f, %f] with confidence %f.' % (box.name, box.target_id, 
						(box.top_left_pt.x + box.bottom_right_pt.x) / 2, 
						(box.top_left_pt.y + box.bottom_right_pt.y) / 2, box.confidence))
				return ret
			else:
				log.error('Fail to get object info.')
		except:
			log.error('Request failed: %s' % (sys.exc_info()[0]))

	def get_marker_info(self):
		try:
			response = self.control_stub.GetCustomArucoInfo(
				vims_pb2.CustomArucoInfoRequest(session_token_uuid=self.session_uuid))
			log.debug('Server responsed status: %s' % (vims_pb2.VimsStatusCode.Name(response.status)))
			if response.status == vims_pb2.VIMS_OK:
				markers = response.markers;
				ret = []
				for marker in markers:
					ret.append([marker.id, marker.center_x, marker.center_y, marker.orientation])
					log.info('Marker ID=%d at [%f, %f] yaw=%f.' % (marker.id, marker.center_x, marker.center_y, marker.orientation))
				return ret
			else:
				log.error('Fail to get marker info.')
		except:
			log.error('Request failed: %s' % (sys.exc_info()[0]))

	def take_picture(self, download=False, download_to='./'):
		'''
		Take a picture and also download it if required.
		Return image file path stored on local machine on success, otherwise, empty string.
		'''
		log.info('Request to take a picture')
		try:
			response = self.control_stub.TakePicture(
				vims_pb2.TakePictureRequest(session_token_uuid=self.session_uuid))
			log.debug('Server responsed status: %s' % (vims_pb2.VimsStatusCode.Name(response.status)))
			if response.status != vims_pb2.VIMS_OK:
				log.error('Fail to take picture')
				return ''
			log.info('Successfully taken a picture on drone: %s' % (response.url))
			if download:
				file_path = self.download_media(response.url, download_to)
				if len(file_path) > 0:
					log.info('Saved the picture to %s' % file_path)
					return file_path
				log.error('Fail to download picture')
		except:
			log.error('Request failed: %s' % (sys.exc_info()[0]))
		return ''

	def start_recording(self):
		'''
		Start video recording
		'''
		log.info('Request to start video recording')
		try:
			response = self.control_stub.StartRecording(
				vims_pb2.StartRecordingRequest(session_token_uuid=self.session_uuid))
			log.debug('Server responsed status: %s' % (vims_pb2.VimsStatusCode.Name(response.status)))
			if response.status == vims_pb2.VIMS_OK:
				log.info('Video recording started')
			else:
				log.error('Fail to start recording')
		except:
			log.error('Request failed: %s' % (sys.exc_info()[0]))

	def stop_recording(self):
		'''
		Stop video recording
		'''
		try:
			response = self.control_stub.StopRecording(
				vims_pb2.StopRecordingRequest(session_token_uuid=self.session_uuid))
			log.debug('Server responsed status: %s' % (vims_pb2.VimsStatusCode.Name(response.status)))
			if response.status == vims_pb2.VIMS_OK:
				log.info('Video recording stopped')
			else:
				log.error('Fail to stop recording')
		except:
			log.error('Request failed: %s' % (sys.exc_info()[0]))

	def download_media(self, media_url, download_to='./'):
		'''
		Download specified media file from Mystic. Applicable for both
		picture or video.
		Return media file path on host machine on success, otherwise, empty string.
		'''
		log.info('Start to download media from Mystic: %s' % (media_url))
		idx = media_url.rfind('/') + 1
		file_path = download_to + media_url[idx:]
		with open(file_path, 'wb') as f:
			try:
				request = vims_pb2.MediaGetRequest(session_token_uuid=self.session_uuid, url=media_url)
				chunks = self.media_stub.GetMedia(request)
				for c in chunks:
					f.write(c.data)
				log.info('Successfully downloaded the media to: %s' % file_path)
				return file_path
			except:
				log.error('Request failed: %s' % (sys.exc_info()[0]))
				log.error('Fail to download/save media file %s to %s' % (media_url, file_path))
		return ''

def run():
	m = Mystic('192.168.1.223') # TODO: just for testing
	m.connect()
	m.take_picture(download=True)
	m.disconnect()

if __name__ == '__main__':
	run()
