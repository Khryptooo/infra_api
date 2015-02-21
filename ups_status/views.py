from django.http import HttpResponse
import json
import PyNUT

# Assumes "emerson" monitoring on ::1
def index(request):
	nut  = PyNUT.PyNUTClient()
	vars = nut.GetUPSVars("emerson")
	# All is fine by default
	ret  = {"status": "charged"}

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
