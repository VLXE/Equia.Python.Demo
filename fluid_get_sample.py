import asyncio
from equia.models import FluidGetResult, ExceptionInfo, ApiFluid, ProblemDetails
from equia.equia_client import EquiaClient
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


def print_fluid(fluid: ApiFluid):
    print(f"Fluid: {fluid.name}")
    print(f"Comment: {fluid.comment}")
    print(f"EoS: {fluid.eos}")
    print(f"Solvent Cp: {fluid.solvent_cp}")
    print(f"Polymer Cp: {fluid.polymer_cp}")
    print(f"Property reference point: {fluid.property_reference_point}")

    print(f"No standard components: {len(fluid.standards)}")
    print(f"No polymers: {len(fluid.polymers)}")


async def request_fluid():
    client = create_client()

    argument = client.get_fluid_get_input()
    argument.fluidid = "Fluid id here" # Replace value with your fluid id

    result: FluidGetResult = await client.call_fluid_get_async(argument)
    # Always do the cleanup
    await client.cleanup()

    if (isinstance(result, ProblemDetails)):
        print_problem_details(result)
    elif (result.success == True):
        print_fluid(result.fluid)
    else:
        print_exception_info(result.exception_info)

loop = asyncio.get_event_loop()
loop.run_until_complete(request_fluid())
