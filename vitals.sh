#! usr/bin/bash

# Seeding Random Generator
RANDOM=$$$(date +%s)


# List of Device id's
#declare -a all_Connected_devices=(dev_001 dev_002 dev_003 dev_004 dev_005)
declare -a all_Connected_devices=(1 2 3 4 5)
num_Connect_devices=${#all_Connected_devices[@]} 
num_Connect_devices=$((num_Connect_devices-1))
echo $num_Connect_devices

# Initializing counter
counter=0
ctr=0
# infinite while loop
while true
do 
	echo $counter
	device_id=${all_Connected_devices[$counter]}
	
	#Generating Health Vitals
	#HR=$(gshuf -i 60-100 -n 1)
	HR=$(python -S -c "import random; print random.randint(60,100)")
	echo "HeartRate="$HR
	#Blood_oxygen=$(shuf -i 90-99 -n 0.01)
	#echo "Blood oxygen=",$Blood_oxygen

	Blood_oxygen=$(python -S -c "import random; print random.uniform(90,99)")
	echo "Blood oxygen="$Blood_oxygen

	body_temp=$(python -S -c "import random; print random.uniform(95,103)")
	echo "Body temperature="$body_temp

	env_temp=$(python -S -c "import random; print random.uniform(55,85)")
	echo "Environment Temperature="$env_temp

	#Generating position (altitude) of fireman
	position=$(python -S -c "import random; print random.uniform(50,5000)")
	echo "Position="$position

	if [ "$counter" -eq $num_Connect_devices ];
	then 
		echo "Reset counter to zero"
		counter=0
	else
		echo "Increment counter"
		counter=$((counter+1))
	fi

#       if [$counter -eq num_Connect_devices-1]
#	then 
#		echo "Counter has reached max"
#		counter=0
#	else
#		echo "Ïncrement counter"
#	fi

	echo "All values to be passed to API=" $HR, $Blood_oxygen, $body_temp, $env_temp, $position

	#API CAll (Dummy)
	#curl --request GET echo.jsontest.com/heartrate/$HR/Blood_O2/$Blood_oxygen
	curl -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/api/$device_id/vitals -d '{"HR": "'"$HR"'", "Blood Oxygen": "'"$Blood_oxygen"'", "Body_Temp":"'"$body_temp"'", "Env_temp": "'"$env_temp"'", "Barometer_read":"'"$position"'"}'
	
	ctr=$((ctr+1))
	echo $ctr
	if [ $((ctr%11)) -eq 0 ]; then
		echo "SOS warning"
		curl -H "Content-Type: text/plain" -X POST http://127.0.0.1:5000/api/$device_id/SOS -d '{I am in danger}'
		exit 0
	fi


done
