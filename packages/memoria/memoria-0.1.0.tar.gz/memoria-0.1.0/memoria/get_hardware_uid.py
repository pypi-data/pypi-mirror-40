import uuid

# creates an identifier that is unique per hardware
def get_hardware_uid():
	"""
	:rtype: str
	"""
	return str(uuid.uuid1(uuid.getnode(),0))[24:]