from django.shortcuts import render


import os
import logging
from datetime import datetime, timezone
from django.conf import settings

import requests
from requests.exceptions import RequestException, Timeout

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# Create your views here.


logger = logging.getLogger(__name__)


class ProfileView(APIView):
    
    
    def get(self, request):
        
        now_iso = datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace("+00:00", "Z")
    
        fact_fallback = "Please, we could not retrieve a cat fact at the moment. try a again later"
    
        
        try:
            rsp = requests.get(settings.CATFACT_API_URL, timeout=settings.CATFACT_TIMEOUT)
            rsp.raise_for_status()
            data = rsp.json()
            
            fact = data.get('fact') or fact_fallback
        
        except (Timeout,) as e:
            logger.warning("Cat facts request timed out %s", e)
            return Response(
                {
                    "status": "error",
                    "message": "failed to fetch cat fact. Please try again later."
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
                content_type="application/json"
            )
            
        except RequestException as e:
            logger.error("Error whilw fetching cat fact: %s", e)
            return Response(
                {
                    "status": "error",
                    "message": "failed to fetch cat fact. Please try again later."
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
                content_type="application/json"
            )
        
        except ValueError as e:  # invalid JSON
            logger.error("Invalid JSON from cat fact provider: %s", e)
            return Response(
                {
                    "status": "error",
                    "message": "Failed to fetch cat fact. Please try again later."
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
                content_type="application/json"
            )
            
        payload = {
            "status": "success",
            "user": {
                "email": settings.USER_EMAIL,
                "name": settings.USER_NAME,
                "stack": settings.USER_STACK,
            },
            "timestamp": now_iso,
            "fact": fact
        }
            
        return Response(payload, status=status.HTTP_200_OK)
            
            
        