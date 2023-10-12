import asyncio
import matplotlib.pyplot as plt
from equia.models import CalculationComposition, ApiOutputUnflashedPropertyResult, ExceptionInfo, ProblemDetails
from equia.equia_client import EquiaClient
from equia.demofluids.demofluid1_nHexane_Ethylene_HDPE7 import demofluid1_nHexane_Ethylene_HDPE7
from shared_settings import sharedsettings

def create_client():
    return EquiaClient(sharedsettings.url, sharedsettings.access_key)


def create_input(client: EquiaClient):
    input = client.get_unflashed_property_input()
    input.fluid = demofluid1_nHexane_Ethylene_HDPE7() #1 Use predefined demo fluid
    input.fluidid = None #No needed since we supply fluid in line above
    input.temperature = 500 # Temperature used in units 'Kelvin' as defined in units below
    input.pressure = 25 # Pressure used in units 'Bar' as defined in units below
    input.pointtype = "Fixed Temperature/Pressure"
    input.volumetype = "Auto"
    input.components = [
      CalculationComposition(mass=0.78), 
      CalculationComposition(mass=0.02), 
      CalculationComposition(mass=0.2)]
    input.units = "C(In,Massfraction);C(Out,Massfraction);T(In,Kelvin);T(Out,Kelvin);P(In,Bar);P(Out,Bar);H(In,kJ/Kg);H(Out,kJ/Kg);S(In,kJ/(Kg Kelvin));S(Out,kJ/(Kg Kelvin));Cp(In,kJ/(Kg Kelvin));Cp(Out,kJ/(Kg Kelvin));Viscosity(In,centiPoise);Viscosity(Out,centiPoise);Surfacetension(In,N/m);Surfacetension(Out,N/m)"
    return input


def print_exception_info(exception_info: ExceptionInfo):
    print(f"Date: {exception_info.date}")
    print(f"Message Type: {exception_info.message_type}")
    print(f"Message: {exception_info.message}")
    print("")
    print(f"Stack Trace: {exception_info.stack_trace}")


def print_problem_details(details: ProblemDetails):
    print("------ A problem occured --------")
    print(f"Title: {details.title}")
    print(f"Type: {details.type}")
    print(f"Status: {details.status}")
    print(f"Detail: {details.detail}")
    print(f"Instance: {details.instance}")
    print(f"Additional properties: {details.additional_properties}")


def print_value(input):
    print(input.ljust(25), end="", flush=True)


def print_calculation_result(result: ApiOutputUnflashedPropertyResult):
    print("")

    print_value(f"Temperature [{result.temperature.units}]")
    print_value(str(result.temperature.value))
    print("")
    print_value(f"Pressure [{result.pressure.units}]")
    print_value(str(result.pressure.value))
    print("")
    print_value(f"Volume [{result.volume.units}]")
    print_value(str(result.volume.value))
    print("")



async def call_slepoint():
    client = create_client()

    input = create_input(client)

    result = await client.call_unflashed_properties_async(input)
    # Always do the cleanup
    await client.cleanup()

    if (isinstance(result, ProblemDetails)):
        print_problem_details(result)
    elif (result.success == True):
        print_calculation_result(result.point)
    else:
        print_exception_info(result.exception_info)

loop = asyncio.get_event_loop()
loop.run_until_complete(call_slepoint())
