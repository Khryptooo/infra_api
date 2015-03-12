from django.http import HttpResponse
from django.conf import settings
from stem.control import Controller
from hurry.filesize import size
import json
import PyNUT

# Assumes "emerson" monitoring on ::1
def ups_status(request):
	nut  = PyNUT.PyNUTClient()
	vars = nut.GetUPSVars("emerson")
	# All is fine by default
	ret  = {"status": "charged", "charge": 100}

	# Electricity is gone and we're running on reserve power
	if vars["ups.status"] == "OB":
		ret["status"] = "blackout"
		ret["charge"] = vars["battery.charge"]
	# Recovering from blackout
	else:
		if vars["battery.charge"] != "100":
			ret["status"] = "charging"
			ret["charge"] = vars["battery.charge"]

	return HttpResponse(json.dumps(ret))

def tor_status(request):
	TOR_CTRL_PASS = getattr(settings, "TOR_CTRL_PASS")
	TOR_CTRL_PORT = getattr(settings, "TOR_CTRL_PORT")

	with Controller.from_port(port = TOR_CTRL_PORT) as controller:
		controller.authenticate(TOR_CTRL_PASS)
		alive         = controller.is_alive()
		net_in        = size(int(controller.get_info("traffic/read")))
		net_out       = size(int(controller.get_info("traffic/written")))
		net_status    = controller.get_network_status()
		flags         = json.dumps(net_status.flags)
		published     = str(net_status.published)
		bandwidth     = net_status.bandwidth

		ret = {"running": alive, "net_in": net_in, "net_out": net_out, "flags": flags, "published": published, "bandwidth": bandwidth}
		return HttpResponse(json.dumps(ret))
