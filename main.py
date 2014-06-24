"""
Usage:

  %(prog)s [opts]

Options:

  -s Run a server
  -c Run a client

  -t Don't run threaded network

  -p [server:][port]
     game server and/or port number to contact

  -l output.log
     optional log filename

If no options are specified, the default is to run a solo client-server."""
# ## Python 3 look ahead imports ###
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import os
import sys

from panda3d.core import loadPrcFileData
from direct.directnotify.DirectNotify import DirectNotify

import spacedrive
#from spacedrive import universals


#loadPrcFileData("", "extended-exceptions 1")

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--client", action="store_true", help="run as a multiplayer client")
parser.add_argument("-s", "--server", action="store_true", help="run as a multiplayer server")
args = parser.parse_args()

'''for opt, arg in opts:
    if opt == '-s':
        universals.runServer = True
        print "Server Flag"
    elif opt == '-c':
        universals.runClient = True
        print "Client Flag"
    elif opt == '-t':
        threadedNet = True
    elif opt == '-p':
        if ':' in arg:
            universals.ServerHost, arg = arg.split(':', 1)
        if arg:
            universals.ServerPort = int(arg)
    elif opt == '-l':
        logFilename = Filename.fromOsSpecific(arg)
    elif opt == '-h':
        usage(0)
    else:
        print 'illegal option: ' + opt
        sys.exit(1)

if logFilename:
    # Set up Panda's notify output to write to the indicated file.
    mstream = MultiplexStream()
    mstream.addFile(logFilename)
    mstream.addStandardOutput()
    Notify.ptr().setOstreamPtr(mstream, False)

    # Also make Python output go to the same place.
    sw = StreamWriter(mstream, False)
    sys.stdout = sw
    sys.stderr = sw

    # Since we're writing to a log file, turn on timestamping.
    loadPrcFileData('', 'notify-timestamp 1')'''

run_server = args.server
run_client = args.client
local_only = False

if not run_client and not run_server:
    run_client = True
    run_server = True
    local_only = True


spacedrive.init(run_server=args.server,
                run_client=args.client,
                local_only=local_only,
                log_level='debug',
                window_title='Apollo')

loadPrcFileData("", "notify-level-Apollo debug")
log = DirectNotify().newCategory("Apollo")

spacedrive.init_physics()
#import shipSystem
#import shipComponents
#import solarSystem
if run_server:
    log.info("Setting up server network")
    from networking.server_net import NetworkSystem
    spacedrive.init_server_net(NetworkSystem)

if run_client:
    import clientNet
    import graphicsComponents
    import guiSystem
    import renderSystem
    log.info("Setting up client network")
    clinet = clientNet.NetworkSystem()
    clinet.serverAddress = '127.0.0.1'
    sandbox.addSystem(clinet)
    log.info("Setting up gui system")
    sandbox.addSystem(guiSystem.GUISystem())
    log.info("Setting up render system")
    sandbox.addSystem(renderSystem.RenderSystem(graphicsComponents.RenderComponent))
    sandbox.base.render.setShaderAuto()

log.info("Setting up Solar System Body Simulator")
sandbox.addSystem(solarSystem.SolarSystemSystem(solarSystem.CelestialComponent))

log.info("Setting up dynamic physics")
sandbox.addSystem(physics.PhysicsSystem(shipComponents.BulletPhysicsComponent))

log.info("Setting up ship interface system")
shipSystem = shipSystem.ShipSystem(shipComponents.PlayerComponent)
sandbox.addSystem(shipSystem)
shipSystem.loadShipClasses()


def planetPositionDebug(task):
    log.debug("===== Day: " + str(universals.day) + " =====")
    for bod in sandbox.getSystem(solarSystem.SolarSystemSystem).bodies:
        log.debug(bod.getName() + ": " + str(bod.getPos()))
    return task.again


def loginDebug(task):
    #sandbox.getSystem(clientNet.NetworkSystem).sendLogin(universals.username, "Hash Password")
    sandbox.send('login', [('127.0.0.1', 1999)])
    #return task.again
    return task.done


def spawnDebug(task):
    shipSystem.spawnShip("The Hype", "Hyperion", universals.spawn, True)
    spawnPoint = LPoint3d(universals.spawn)
    spawnPoint.addX(3)
    shipSystem.spawnShip("Boo boo", "Hyperion", spawnPoint)

#sandbox.base.taskMgr.doMethodLater(10, planetPositionDebug, "Position Debug")
if universals.runClient:
    sandbox.base.taskMgr.doMethodLater(1, loginDebug, "Login Debug")

if universals.runServer:
    sandbox.base.taskMgr.doMethodLater(1, spawnDebug, "Spawn Debug")


log.info("Setup complete.")
sandbox.run()

##TODO: FIX BULLET PHYSICS AND SOLAR SYSTE RENDER TO PROPERLY USE ROOT SOLAR SYSTEM NODE
