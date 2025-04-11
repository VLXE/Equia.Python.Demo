import asyncio
from pickle import TRUE
import matplotlib.pyplot as plt
from equia.models import CalculationComposition, ExceptionInfo, ProblemDetails
from equia.equia_client import EquiaClient
from equia.demofluids.demofluid1_nHexane_Ethylene_HDPE7 import demofluid1_nHexane_Ethylene_HDPE7
from shared_settings import sharedsettings

def create_client():
    return EquiaClient(sharedsettings.url, sharedsettings.access_key)


def print_exception_info(exception_info: ExceptionInfo):
    print(f"Date: {exception_info.date}")
    print(f"Message Type: {exception_info.message_type}")
    print(f"Message: {exception_info.message}")
    print("")
    print(f"Stack Trace: {exception_info.stack_trace}")


def print_problem_details(details: ProblemDetails):
    print("------ A problem occurred --------")
    print(f"Title: {details.title}")
    print(f"Type: {details.type}")
    print(f"Status: {details.status}")
    print(f"Detail: {details.detail}")
    print(f"Instance: {details.instance}")
    print(f"Additional properties: {details.additional_properties}")


async def call_phase_diagram():
    client = create_client()

    input = client.get_phasediagam_standard_input()
    input.fluid = demofluid1_nHexane_Ethylene_HDPE7() #1 Use predefined demo fluid
    input.fluidid = None #No needed since we supply fluid in line above
    input.sle = True #Ask to include the SLE part of the phasediagram
    input.slve = True #Ask to include the SLVE part of the phasediagram
    input.vlle = True #Ask to include the VLLE part of the phasediagram
    input.components = [
      CalculationComposition(amount=0.78), 
      CalculationComposition(amount=0.02), 
      CalculationComposition(amount=0.2)]
    input.units = "C(In,Massfraction);C(Out,Massfraction);T(In,Kelvin);T(Out,Kelvin);P(In,Bar);P(Out,Bar);H(In,kJ/Kg);H(Out,kJ/Kg);S(In,kJ/(Kg Kelvin));S(Out,kJ/(Kg Kelvin));Cp(In,kJ/(Kg Kelvin));Cp(Out,kJ/(Kg Kelvin));Viscosity(In,centiPoise);Viscosity(Out,centiPoise);Surfacetension(In,N/m);Surfacetension(Out,N/m)"

    result = await client.call_phasediagram_standard_async(input)
    # Always do the cleanup
    await client.cleanup()

    if (isinstance(result, ProblemDetails)):
        print_problem_details(result)
    elif (result.success == True):
        plt.title("Phase diagram")
        plt.xlabel(f"Temperature [{result.curve.temperature_units}]")
        plt.ylabel(f"Pressure [{result.curve.pressure_units}]")

        if (len(result.curve.phaseenvelope) > 0):
            plt.plot(list(map(lambda point: point.temperature, result.curve.phaseenvelope)), list(
                map(lambda point: point.pressure, result.curve.phaseenvelope)), label=f"Phase Envelope")
        if (len(result.curve.vlle) > 0):
            plt.plot(list(map(lambda point: point.temperature, result.curve.vlle)), list(
                map(lambda point: point.pressure, result.curve.vlle)), label=f"VLLE")
        if (len(result.curve.sle) > 0):
            plt.plot(list(map(lambda point: point.temperature, result.curve.sle)), list(
                map(lambda point: point.pressure, result.curve.sle)), label=f"SLE")
        if (len(result.curve.slve) > 0):
            plt.plot(list(map(lambda point: point.temperature, result.curve.slve)), list(
                map(lambda point: point.pressure, result.curve.slve)), label=f"SLVE")

        plt.legend()
        plt.show()
    else:
        print_exception_info(result.exception_info)


loop = asyncio.get_event_loop()
loop.run_until_complete(call_phase_diagram())
