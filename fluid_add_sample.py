from ast import Str
import asyncio
from equia.models import FluidAddResult, ExceptionInfo, ProblemDetails
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


def print_fluid(fluidid: Str):
    print(f"Fluid id: {fluidid}")


async def request_fluid():
    client = create_client()

    argument = client.get_fluid_add_input()
    argument.fluid = demofluid1_nHexane_Ethylene_HDPE7()

    result: FluidAddResult = await client.call_fluid_add_async(argument)
    # Always do the cleanup
    await client.cleanup()

    if (isinstance(result, ProblemDetails)):
        print_problem_details(result)
    elif (result.success == True):
        print_fluid(result.fluidid)
    else:
        print_exception_info(result.exception_info)

loop = asyncio.get_event_loop()
loop.run_until_complete(request_fluid())
