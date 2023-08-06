from setuptools import setup
from distutils.extension import Extension


# Build & installation process for the JSBSim Python module
setup(
    name="JSBSim",
    version="1.0.0.dev1",
    url="https://github.com/JSBSim-Team/jsbsim",
    author="Jon S. Berndt",
    author_email="jsbsim-users@lists.sourceforge.net",
    license="LGPL 2.1",
    description="An open source flight dynamics & control software library",
    long_description="JSBSim is a multi-platform, general purpose object-oriented Flight Dynamics Model (FDM) written in C++. The FDM is essentially the physics & math model that defines the movement of an aircraft, rocket, etc., under the forces and moments applied to it using the various control mechanisms and from the forces of nature. JSBSim can be run in a standalone batch mode flight simulator (no graphical displays) for testing and study, or integrated with [FlightGear](http://home.flightgear.org/) or other flight simulator.",
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Other Audience",
        "License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)",
        "Operating System :: Microsoft",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: C++",
        "Programming Language :: Python",
        "Topic :: Games/Entertainment :: Simulation",
        "Topic :: Scientific/Engineering"
    ],
    ext_modules=[Extension('jsbsim', ['jsbsim.pyx', 'src/FGFDMExec.cpp','src/FGJSBBase.cpp','src/initialization/FGInitialCondition.cpp','src/initialization/FGTrim.cpp','src/initialization/FGTrimAxis.cpp','src/models/atmosphere/FGMSIS.cpp','src/models/atmosphere/FGMSISData.cpp','src/models/atmosphere/FGMars.cpp','src/models/atmosphere/FGStandardAtmosphere.cpp','src/models/atmosphere/FGWinds.cpp','src/models/flight_control/FGDeadBand.cpp','src/models/flight_control/FGFCSComponent.cpp','src/models/flight_control/FGFilter.cpp','src/models/flight_control/FGGain.cpp','src/models/flight_control/FGKinemat.cpp','src/models/flight_control/FGSummer.cpp','src/models/flight_control/FGSwitch.cpp','src/models/flight_control/FGFCSFunction.cpp','src/models/flight_control/FGSensor.cpp','src/models/flight_control/FGPID.cpp','src/models/flight_control/FGActuator.cpp','src/models/flight_control/FGAccelerometer.cpp','src/models/flight_control/FGGyro.cpp','src/models/flight_control/FGMagnetometer.cpp','src/models/flight_control/FGAngles.cpp','src/models/flight_control/FGWaypoint.cpp','src/models/flight_control/FGDistributor.cpp','src/models/propulsion/FGElectric.cpp','src/models/propulsion/FGEngine.cpp','src/models/propulsion/FGForce.cpp','src/models/propulsion/FGNozzle.cpp','src/models/propulsion/FGPiston.cpp','src/models/propulsion/FGPropeller.cpp','src/models/propulsion/FGRocket.cpp','src/models/propulsion/FGTank.cpp','src/models/propulsion/FGThruster.cpp','src/models/propulsion/FGTurbine.cpp','src/models/propulsion/FGTurboProp.cpp','src/models/propulsion/FGTransmission.cpp','src/models/propulsion/FGRotor.cpp','src/models/FGAerodynamics.cpp','src/models/FGAircraft.cpp','src/models/FGAtmosphere.cpp','src/models/FGAuxiliary.cpp','src/models/FGFCS.cpp','src/models/FGSurface.cpp','src/models/FGGroundReactions.cpp','src/models/FGInertial.cpp','src/models/FGLGear.cpp','src/models/FGMassBalance.cpp','src/models/FGModel.cpp','src/models/FGOutput.cpp','src/models/FGPropagate.cpp','src/models/FGPropulsion.cpp','src/models/FGInput.cpp','src/models/FGExternalReactions.cpp','src/models/FGExternalForce.cpp','src/models/FGBuoyantForces.cpp','src/models/FGGasCell.cpp','src/models/FGAccelerations.cpp','src/math/FGColumnVector3.cpp','src/math/FGFunction.cpp','src/math/FGLocation.cpp','src/math/FGMatrix33.cpp','src/math/FGPropertyValue.cpp','src/math/FGQuaternion.cpp','src/math/FGRealValue.cpp','src/math/FGTable.cpp','src/math/FGCondition.cpp','src/math/FGRungeKutta.cpp','src/math/FGModelFunctions.cpp','src/math/FGTemplateFunc.cpp','src/input_output/FGGroundCallback.cpp','src/input_output/FGPropertyManager.cpp','src/input_output/FGScript.cpp','src/input_output/FGXMLElement.cpp','src/input_output/FGXMLParse.cpp','src/input_output/FGfdmSocket.cpp','src/input_output/FGOutputType.cpp','src/input_output/FGOutputFG.cpp','src/input_output/FGOutputSocket.cpp','src/input_output/FGOutputFile.cpp','src/input_output/FGOutputTextFile.cpp','src/input_output/FGPropertyReader.cpp','src/input_output/FGModelLoader.cpp','src/input_output/FGInputType.cpp','src/input_output/FGInputSocket.cpp','src/input_output/FGUDPInputSocket.cpp','src/simgear/props/props.cxx','src/simgear/props/propertyObject.cxx','src/simgear/xml/easyxml.cxx','src/simgear/xml/xmlparse.c','src/simgear/xml/xmltok.c','src/simgear/xml/xmlrole.c','src/simgear/magvar/coremag.cxx','src/simgear/misc/sg_path.cxx','src/simgear/misc/strutils.cxx','src/simgear/io/iostreams/sgstream.cxx',],
                           include_dirs=['src'],
                           extra_compile_args=["-DJSBSIM_VERSION=\"1.0.0.dev1\"",
                                               "-DHAVE_EXPAT_CONFIG_H",
                                               '-std=c++11'],
                           language='c++')],
    setup_requires=["setuptools>=18.0", "cython>=0.25"])
