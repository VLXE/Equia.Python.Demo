import asyncio
import matplotlib.pyplot as plt
from equia.models import CalculationComposition, ApiOutputCalculationResultPoint, ExceptionInfo, ProblemDetails
from equia.equia_client import EquiaClient
from equia.demofluids.demofluid1_nHexane_Ethylene_HDPE7 import demofluid1_nHexane_Ethylene_HDPE7
from shared_settings import sharedsettings

def create_client():
    return EquiaClient(sharedsettings.url, sharedsettings.access_key)


def create_input(client: EquiaClient):
    input = client.get_sle_point_input()
    input.fluid = demofluid1_nHexane_Ethylene_HDPE7() #1 Use predefined demo fluid
    input.fluidid = None # No needed since we supply fluid in line above
    input.pressure = 25 # Pressure used in units 'Bar' as defined in units below
    input.pointtype = "FixedPressure"
    input.components = [
      CalculationComposition(amount=0.78), 
      CalculationComposition(amount=0.02), 
      CalculationComposition(amount=0.2)]
    input.units = "C(In,Massfraction);C(Out,Massfraction);T(In,Kelvin);T(Out,Kelvin);P(In,Bar);P(Out,Bar);H(In,kJ/Kg);H(Out,kJ/Kg);S(In,kJ/(Kg Kelvin));S(Out,kJ/(Kg Kelvin));Cp(In,kJ/(Kg Kelvin));Cp(Out,kJ/(Kg Kelvin));Viscosity(In,centiPoise);Viscosity(Out,centiPoise);Surfacetension(In,N/m);Surfacetension(Out,N/m)"
    return input


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


def print_value(input):
    print(input.ljust(25), end="", flush=True)


def print_calculation_result(result: ApiOutputCalculationResultPoint):
    print("")
    print_value("Property")
    for phase in result.phases:
        print_value(phase.phase_label)
    print("")

    print_value(f"Temperature [{result.temperature.units}]")
    print_value(str(result.temperature.value))
    print("")
    print_value(f"Pressure [{result.pressure.units}]")
    print_value(str(result.pressure.value))
    print("")

    print_composition(result)
    print_properties(result)
    print_polymer_moments(result)
    print_polymer_distributions(result)


def print_composition(result: ApiOutputCalculationResultPoint):
    print("")
    print("Components")
    firstPhase = result.phases[0]
    for i in range(len(firstPhase.composition.components)):
        print_value(
            f"{firstPhase.composition.components[i].name} [{firstPhase.composition.composition_units}]")
        for phase in result.phases:
            print_value(str(phase.composition.components[i].value))
        print("")


def print_properties(result: ApiOutputCalculationResultPoint):
    firstPhase = result.phases[0]
    print("")
    print_value(f"Phase Fraction [Mole]")
    for phase in result.phases:
        print_value(str(phase.mole_percent.value))
    print("")
    print_value(f"Phase Fraction [Weight]")
    for phase in result.phases:
        print_value(str(phase.weight_percent.value))
    print("")
    print_value(f"Compressibility [-]")
    for phase in result.phases:
        print_value(str(phase.compressibility.value))
    print("")
    print_value(f"Density [{firstPhase.density.units}]")
    for phase in result.phases:
        print_value(str(phase.density.value))
    print("")
    print_value(f"Molar Volumne [{firstPhase.volume.units}]")
    for phase in result.phases:
        print_value(str(phase.volume.value))
    print("")
    print_value(f"Enthalpy [{firstPhase.enthalpy.units}]")
    for phase in result.phases:
        print_value(str(phase.enthalpy.value))
    print("")
    print_value(f"Entropy [{firstPhase.entropy.units}]")
    for phase in result.phases:
        print_value(str(phase.entropy.value))
    print("")
    print_value(f"Cp [{firstPhase.cp.units}]")
    for phase in result.phases:
        print_value(str(phase.cp.value))
    print("")
    print_value(f"Cv [{firstPhase.cv.units}]")
    for phase in result.phases:
        print_value(str(phase.cv.value))
    print("")
    print_value(f"JTCoefficient [{firstPhase.jt_coefficient.units}]")
    for phase in result.phases:
        print_value(str(phase.jt_coefficient.value))
    print("")
    print_value(f"Velocity of sound [{firstPhase.speed_of_sound.units}]")
    for phase in result.phases:
        print_value(str(phase.speed_of_sound.value))
    print("")
    print_value(f"Solubility parameter [{firstPhase.solubility_parameter.units}]")
    for phase in result.phases:
        print_value(str(phase.solubility_parameter.value))
    print("")
    print_value(f"Molecular Weight [{firstPhase.molecular_weight.units}]")
    for phase in result.phases:
        print_value(str(phase.molecular_weight.value))
    print("")


def print_polymer_moments(result: ApiOutputCalculationResultPoint):
    first_phase_moments = result.phases[0].polymer_moments
    for i in range(len(first_phase_moments.polymers)):
        print_value(
            f"Mn ({first_phase_moments.polymers[i].polymer_name}) [{first_phase_moments.moment_units}]")
        for phase in result.phases:
            print_value(str(phase.polymer_moments.polymers[i].mn))
        print("")

        print_value(
            f"Mw ({first_phase_moments.polymers[i].polymer_name}) [{first_phase_moments.moment_units}]")
        for phase in result.phases:
            print_value(str(phase.polymer_moments.polymers[i].mw))
        print("")

        print_value(
            f"Mz ({first_phase_moments.polymers[i].polymer_name}) [{first_phase_moments.moment_units}]")
        for phase in result.phases:
            print_value(str(phase.polymer_moments.polymers[i].mz))
        print("")


def print_polymer_distributions(result: ApiOutputCalculationResultPoint):
    firstPhase = result.phases[0]
    # find components with distribution (polymers)
    for compIndex in range(len(firstPhase.composition.components)):
        component = firstPhase.composition.components[compIndex]
        if (len(component.distribution) <= 0):
            continue

        # just print the name of the polymer on top of each phase column
        print_value("")
        for phaseIndex in range(len(result.phases)):
            print_value(component.name)

        # now print the actual distribution values for each phase
        for distIndex in range(len(component.distribution)):
            print("")
            print_value("")
            for phaseIndex in range(len(result.phases)):
                distribution = result.phases[phaseIndex].composition.components[compIndex].distribution[distIndex]
                print_value(str(distribution.value))


def draw_polymer_distributions(result: ApiOutputCalculationResultPoint):
    plt.title("Distribution")
    plt.xlabel("Ln(Molar mass)")
    plt.xscale("log")
    plt.ylabel("Mass fraction")
    for i in range(len(result.phases)):
        phase = result.phases[i]
        for j in range(len(phase.composition.components)):
            component = phase.composition.components[j]
            if (len(component.distribution) > 0):
                plt.plot(list(map(lambda point: point.value, component.distribution)), list(
                    map(lambda point: point.molar_mass, component.distribution)), label=f"{component.name}: {phase.phase_label}")

    plt.legend()
    plt.show()


async def call_slepoint():
    client = create_client()

    input = create_input(client)

    result = await client.call_sle_point_async(input)
    # Always do the cleanup
    await client.cleanup()

    if (isinstance(result, ProblemDetails)):
        print_problem_details(result)
    elif (result.success == True):
        print_calculation_result(result.point)
        draw_polymer_distributions(result.point)
    else:
        print_exception_info(result.exception_info)

loop = asyncio.get_event_loop()
loop.run_until_complete(call_slepoint())
