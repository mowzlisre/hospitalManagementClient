from rest_framework.views import APIView
from django.http import JsonResponse
from .models import *
from datetime import datetime

class AnalyticsAPI(APIView):
    def get(self, request, id):
        records = Record.objects.filter(profile__id=id)
        timeStamp = []
        hbpm = []
        spo2 = []
        temp = []
        for record in records:
            stamp = datetime.strftime(record.timeStamp, "%Y-%m-%d %H:%M:%S")
            timeStamp.append(stamp)

            hbpm.append(record.hbpm)
            spo2.append(record.spo2)
            temp.append(record.temperature)
        
        return JsonResponse({
            "timeStamp" : timeStamp,
            "hbpm" : hbpm,
            "spo2" : spo2,
            "temp" : temp
        }, safe=False)

class UpdateDataAPI(APIView):
    def post(self, request):
        try:
            profile = Profile.objects.get(patientName=request.POST.get('username'))
            record = Record()
            record.profile = profile
            record.temperature = request.POST.get('temp')
            record.spo2 = request.POST.get('spo2')
            record.hbpm = request.POST.get('hb')
            record.save()
            return JsonResponse({
                "response" : "Data added"
            })
        except:
            return JsonResponse({
                "response" : "There was an unexpected error!"
            })