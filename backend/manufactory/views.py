from django.shortcuts import render
from backend.authentication.models import CustomUser
from rest_framework.decorators import permission_classes
import rest_framework.permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from backend.manufactory.views import get_user_from_request
from backend.authentication.permissions import FabricationPermission, SubAssemblyPermission, AssemblyPermission, SuperAssemblyPermission, SuperFabricationPermission, SuperSubAssemblyPermission
from .serializer import AssemblySerializer, FabricationSerializer, SubAssemblySerializer

from authentication.permissions import FabricationPermission, SuperFabricationPermission, AssemblyPermission

## import APIView?

# Create your views here.


def get_user_from_request(request):
    # change this when auth is implemented

    _id = request.GET["id"]

    return CustomUser.objects.get(id=_id or 1)

#Fabiraction view
class FabricationDataView(APIView):
    def get(self, request):
        # Logic to retrieve Fabrication data
        user = get_user_from_request(request)   

        fabrications = Fabrication.objects.filter(end_date_isnull=True)
        serilizer = FabricationSerializer(fabrications, many=True)


        response_msg = {
            "quantity":fabrications.count(),
            "data": serilizer.data
        }

        response_code = status

        return Response(response_msg, response_code)

    def post(self, request):
        # Logic to create a new Fabrication entry
        # Retrieve data from the request data
        item = request.data.get("item")
        raw_material = request.data.get("raw_material")
        quantity = request.data.get("quantity")

        # Create the new Fabrication entry
        new_fabrication = Fabrication.objects.create(
            item=item,
            raw_material=raw_material,
            quantity=quantity,
        )

        # Return a success response
        return Response(
            {"message": "Fabrication entry created successfully"}, status=201
        )



# SubAssenmbly 
class SubAssemblyDataView(APIView):
    def get(self, request):
        # Logic to retrieve SubAssembly data
        user = get_user_from_request(request)   

        subAssemblys = SubAssembly.objects.filter(end_date_isnull=True)
        serilizer = SubAssemblySerializer(subAssemblys, many=True)


        response_msg = {
            "quantity":subAssemblys.count(),
            "data": serilizer.data
        }

        response_code = 200


        return Response(response_msg, response_code)

    def post(self, request):
        # Logic to create a new SubAssembly entry
        # Retrieve data from the request data
        process = request.data.get("process")
        item_id = request.data.get("item_id")
        machine_id = request.data.get("machine_id")

        # Create the new SubAssembly entry
        new_SubAssembly = SubAssembly.objects.create(
            item=item,
            raw_material=raw_material,
            quantity=quantity,
        )

        # Return a success response
        return Response(
            {"message": "SubAssembly entry created successfully"}, status=201
        )


# Assembly
class AssemblyDataView(APIView):
    def get(self, request):
        # Logic to retrieve Assembly data
        user = get_user_from_request(request)   

        assemblys = Assembly.objects.filter(end_date_isnull=True)
        serilizer = AssemblySerializer(Assemblys, many=True)


        response_msg = {
            "quantity":assemblys.count(),
            "data": serilizer.data
        }

        response_code = 200


        return Response(response_msg, response_code)

    def post(self, request):
        # Logic to create a new Assembly entry
        # Retrieve data from the request data
        process = request.data.get("process")
        machine_id = request.data.get("machine_id")

        # Create the new Assembly entry
        new_assembly = Assembly.objects.create(
            process=process,
            machine_id=raw_material,
        )

        # Return a success response
        return Response(
            {"message": "Assembly entry created successfully"}, status=201
        )

    # @permission_classes([SuperAssemblyPermission])
    def patch(self,request):
        # Logic to update Assembly entry
        # Retrieve data from the request data
        id_list = request.data.get("id_;list")


        # Retrieve the Assembly objects based on the specified IDs
        assemblies = Assembly.objects.filter(process_id__in=ids)

        # Update the end_date field to the current datetime
        current_datetime = timezone.now()
        for assembly in assemblies:
            assembly.end_date = current_datetime

        # Prepare the bulk update data
        bulk_update_data = [
            Assembly(id=assembly.id, end_date=F('end_date'))
            for assembly in assemblies
        ]

        # Perform the bulk update
        Assembly.objects.bulk_update(bulk_update_data, ['end_date'])


        Response(
            {"message": "Assembly updated successfully"}, status=201
        )


## implement above in One view
# class UserDataView(APIView):
#     def get(self, request):


#         user = get_user_from_request(request)

#         fabrication_users = CustomUser.objects.filter(user_type="fabrication")
#         serilizer = FabricationSerializer(fabrications, many=True)

#         response_msg = {"data": serilizer.data}

#         response_code = 200
#         return Response(response_msg, response_code)
