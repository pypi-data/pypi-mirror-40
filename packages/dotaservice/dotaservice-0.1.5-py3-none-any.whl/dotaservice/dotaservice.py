from pprint import pprint, pformat
from struct import unpack
from sys import platform
import asyncio
import glob
import json
import logging
import math
import os
import pkg_resources
import re
import shutil
import signal
import time
import traceback
import uuid

from google.protobuf.message import DecodeError
from google.protobuf.json_format import MessageToDict
from grpclib.server import Server

from dotaservice import __version__
from dotaservice.protos.dota_gcmessages_common_bot_script_pb2 import CMsgBotWorldState
from dotaservice.protos.dota_shared_enums_pb2 import DOTA_GAMERULES_STATE_GAME_IN_PROGRESS
from dotaservice.protos.dota_shared_enums_pb2 import DOTA_GAMERULES_STATE_PRE_GAME
from dotaservice.protos.DotaService_grpc import DotaServiceBase
from dotaservice.protos.DotaService_pb2 import Empty
from dotaservice.protos.DotaService_pb2 import HostMode
from dotaservice.protos.DotaService_pb2 import Observation
from dotaservice.protos.DotaService_pb2 import Status

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

LUA_FILES_GLOB = pkg_resources.resource_filename('dotaservice', 'lua/*.lua')


def verify_game_path(game_path):
    if not os.path.exists(game_path):
        raise ValueError("Game path '{}' does not exist.".format(game_path))
    if not os.path.isdir(game_path):
        raise ValueError("Game path '{}' is not a directory.".format(game_path))
    dota_script = os.path.join(game_path, DotaGame.DOTA_SCRIPT_FILENAME)
    if not os.path.isfile(dota_script):
        raise ValueError("Dota executable '{}' is not a file.".format(dota_script))
    if not os.access(dota_script, os.X_OK):
        raise ValueError("Dota executable '{}' is not executable.".format(dota_script))


class DotaGame(object):

    ACTION_FILENAME = 'action'
    ACTIONABLE_GAME_STATES = [DOTA_GAMERULES_STATE_PRE_GAME, DOTA_GAMERULES_STATE_GAME_IN_PROGRESS]
    BOTS_FOLDER_NAME = 'bots'
    CONFIG_FILENAME = 'config_auto'
    CONSOLE_LOG_FILENAME = 'console.log'
    CONSOLE_LOGS_GLOB = 'console*.log'
    DOTA_SCRIPT_FILENAME = 'dota.sh'
    LIVE_CONFIG_FILENAME = 'live_config_auto'
    PORT_WORLDSTATE_DIRE = 12121
    PORT_WORLDSTATE_RADIANT = 12120
    RE_DEMO =  re.compile(r'playdemo[ \t](.*dem)')
    RE_LUARDY = re.compile(r'LUARDY[ \t](\{.*\})')
    WORLDSTATE_PAYLOAD_BYTES = 4

    def __init__(self,
                 dota_path,
                 action_folder,
                 host_timescale,
                 ticks_per_observation,
                 game_mode,
                 host_mode,
                 game_id=None):
        self.dota_path = dota_path
        self.action_folder = action_folder
        self.host_timescale = host_timescale
        self.ticks_per_observation = ticks_per_observation
        self.game_mode = game_mode
        self.host_mode = host_mode
        self.game_id = game_id
        if not self.game_id:
            self.game_id = str(uuid.uuid1())
        self.dota_bot_path = os.path.join(self.dota_path, 'dota', 'scripts', 'vscripts',
                                          self.BOTS_FOLDER_NAME)
        self.bot_path = self._create_bot_path()
        self.worldstate_queue_radiant = asyncio.Queue(loop=asyncio.get_event_loop())
        # self.worldstate_queue_dire = asyncio.Queue(loop=asyncio.get_event_loop())
        self.lua_config_future = asyncio.get_event_loop().create_future()
        self._write_config()
        self.process = None
        self.demo_path_rel = None

        has_display = 'DISPLAY' in os.environ
        if not has_display and HostMode.Value('DEDICATED'):
            raise ValueError('GUI requested but no display detected.')
            exit(-1)
        super().__init__()

    def _write_config(self):
        # Write out the game configuration.
        config = {
            'game_id': self.game_id,
            'ticks_per_observation': self.ticks_per_observation,
        }
        self.write_static_config(data=config)

    def write_static_config(self, data):
        self._write_bot_data_file(filename_stem=self.CONFIG_FILENAME, data=data)

    def write_live_config(self, data):
        self._write_bot_data_file(filename_stem=self.LIVE_CONFIG_FILENAME, data=data)
        
    def write_action(self, data):
        self._write_bot_data_file(filename_stem=self.ACTION_FILENAME, data=data)

    def _write_bot_data_file(self, filename_stem, data):
        """Write a file to lua to that the bot can read it.

        Although writing atomicly would prevent bad reads, we just catch the bad reads in the
        dota bot client.
        """
        filename = os.path.join(self.bot_path, '{}.lua'.format(filename_stem))
        data = """
        -- THIS FILE IS AUTO GENERATED
        return '{data}'
        """.format(data=json.dumps(data, separators=(',', ':')))
        with open(filename, 'w') as f:
            f.write(data)

    def _create_bot_path(self):
        """Remove DOTA's bots subdirectory or symlink and update it with our own."""
        if os.path.exists(self.dota_bot_path) or os.path.islink(self.dota_bot_path):
            if os.path.isdir(self.dota_bot_path) and not os.path.islink(self.dota_bot_path):
                raise ValueError(
                    'There is already a bots directory ({})! Please remove manually.'.format(
                        self.dota_bot_path))
            os.remove(self.dota_bot_path)
        session_folder = os.path.join(self.action_folder, str(self.game_id))
        os.mkdir(session_folder)
        bot_path = os.path.join(session_folder, self.BOTS_FOLDER_NAME)
        os.mkdir(bot_path)

        # Copy all the bot files into the action folder.
        lua_files = glob.glob(LUA_FILES_GLOB)
        for filename in lua_files:
            shutil.copy(filename, bot_path)

        # shutil.copy('/Users/tzaman/dev/dotaservice/botcpp/botcpp_radiant.so', bot_path)

        # Finally, symlink DOTA to this folder.
        os.symlink(src=bot_path, dst=self.dota_bot_path)
        return bot_path

    async def monitor_log(self):
        abs_glob = os.path.join(self.bot_path, self.CONSOLE_LOGS_GLOB)
        while True:
            # Console logs can get split from `$stem.log` into `$stem.$number.log`.
            for filename in glob.glob(abs_glob):
                with open(filename) as f:
                    for line in f:
                        # Demo line always comes before the LUADRY signal.
                        if self.demo_path_rel is None:
                            m_demo = self.RE_DEMO.search(line)
                            if m_demo:
                                self.demo_path_rel = m_demo.group(1)
                                logger.debug("demo_path_rel={}".format(self.demo_path_rel))
                        m_luadry = self.RE_LUARDY.search(line)
                        if m_luadry:
                            config_json = m_luadry.group(1)
                            lua_config = json.loads(config_json)
                            logger.debug('lua_config={}'.format(lua_config))
                            self.lua_config_future.set_result(lua_config)
                            return
            await asyncio.sleep(0.2)

    async def run(self):
        # Start the worldstate listener(s).
        asyncio.create_task(self._run_dota())
        asyncio.create_task(self._worldstate_listener(
            port=self.PORT_WORLDSTATE_RADIANT, queue=self.worldstate_queue_radiant))
        # asyncio.create_task(self._worldstate_listener(
        #     port=self.PORT_WORLDSTATE_DIRE, queue=self.worldstate_queue_radiant))

    async def _run_dota(self):
        script_path = os.path.join(self.dota_path, self.DOTA_SCRIPT_FILENAME)

        # TODO(tzaman): all these options should be put in a proto and parsed with gRPC Config.
        args = [
            script_path,
            '-botworldstatesocket_threaded',
            '-botworldstatetosocket_dire {}'.format(self.PORT_WORLDSTATE_DIRE),
            '-botworldstatetosocket_frames {}'.format(self.ticks_per_observation),
            '-botworldstatetosocket_radiant {}'.format(self.PORT_WORLDSTATE_RADIANT),
            '-con_logfile scripts/vscripts/bots/{}'.format(self.CONSOLE_LOG_FILENAME),
            '-con_timestamp',
            '-console',
            '-insecure',
            '-noip',
            '-nowatchdog',  # WatchDog will quit the game if e.g. the lua api takes a few seconds.
            '+clientport 27006',  # Relates to steam client.
            '+dota_1v1_skip_strategy 1',
            '+dota_surrender_on_disconnect 0',
            '+host_timescale {}'.format(self.host_timescale),
            '+hostname dotaservice',
            '+sv_cheats 1',
            '+sv_hibernate_when_empty 0',
            '+tv_delay 0 ',
            '+tv_enable 1',
            '+tv_title {}'.format(self.game_id),
            '+tv_autorecord 1',
            '+tv_transmitall 1',  # TODO(tzaman): what does this do exactly?
        ]

        if self.host_mode == HostMode.Value('DEDICATED'):
            args.append('-dedicated')
        if self.host_mode == HostMode.Value('DEDICATED') or \
            self.host_mode == HostMode.Value('GUI'):
            args.append('-fill_with_bots')
            args.extend(['+map', 'start gamemode {}'.format(self.game_mode)])
            args.append('+sv_lan 1')
        if self.host_mode == HostMode.Value('GUI_MENU'):
            args.append('+sv_lan 0')

        create = asyncio.create_subprocess_exec(
            *args,
            stdin=asyncio.subprocess.PIPE,
        )
        self.process = await create

        task_monitor_log = asyncio.create_task(self.monitor_log())

        try:
            await self.process.wait()
        except asyncio.CancelledError:
            kill_processes_and_children(pid=self.process.pid)
            raise

    async def close(self):
        # TODO(tzaman): close async stuff?

        # Make the bot flush.
        self.write_action(data='FLUSH')

        # Stop the recording
        self.process.stdin.write(b"tv_stoprecord\n")
        self.process.stdin.write(b"quit\n")
        await self.process.stdin.drain()
        await asyncio.sleep(1)

        # Move the recording.
        if self.demo_path_rel is not None:
            demo_path_abs = os.path.join(self.dota_path, 'dota', self.demo_path_rel)
            try:
                shutil.move(demo_path_abs, self.bot_path)
            except Exception as e:  # Fail silently.
                logger.error(e)

    @classmethod
    async def _world_state_from_reader(cls, reader):
        # Receive the package length.
        data = await reader.read(cls.WORLDSTATE_PAYLOAD_BYTES)
        if len(data) != cls.WORLDSTATE_PAYLOAD_BYTES:
            raise ValueError('Invalid worldstate payload')
        n_bytes = unpack("@I", data)[0]
        # Receive the payload given the length.
        data = await asyncio.wait_for(reader.read(n_bytes), timeout=1)
        # Decode the payload.
        world_state = CMsgBotWorldState()
        world_state.ParseFromString(data)
        logger.debug('Received world_state: dotatime={}, gamestate={}'.format(
            world_state.dota_time, world_state.game_state))
        return world_state

    @classmethod
    async def _worldstate_listener(self, port, queue):
        while True:  # TODO(tzaman): finite retries.
            try:
                await asyncio.sleep(0.5)
                reader, writer = await asyncio.open_connection('127.0.0.1', port)
            except ConnectionRefusedError:
                pass
            else:
                break
        try:
            while True:
                # This reader is always going to need to keep going to keep the buffers flushed.
                try:
                    world_state = await self._world_state_from_reader(reader)
                    is_in_game = world_state.game_state in self.ACTIONABLE_GAME_STATES
                    has_units = len(world_state.units) > 0
                    if is_in_game and has_units:
                        # Only regard worldstates that are actionable (in-game + has units).
                        queue.put_nowait(world_state)
                except DecodeError as e:
                    pass
        except asyncio.CancelledError:
            raise


class DotaService(DotaServiceBase):

    WATCHDOG_TIMER = 10

    def __init__(self, dota_path, action_folder, session_expiration_time):
        self.dota_path = dota_path
        self.action_folder = action_folder
        self.session_expiration_time = session_expiration_time

        # Initial assertions.
        verify_game_path(self.dota_path)

        if not os.path.exists(self.action_folder):
            if platform == "linux" or platform == "linux2":
                raise ValueError(
                    "Action folder '{}' not found.\nYou can create a 2GB ramdisk by executing:"
                    "`mkdir /tmpfs; mount -t tmpfs -o size=2048M tmpfs /tmpfs`\n"
                    "With Docker, you can add a tmpfs adding `--mount type=tmpfs,destination=/tmpfs`"
                    " to its run command.".format(self.action_folder))
            elif platform == "darwin":
                if not os.path.exists(self.action_folder):
                    raise ValueError(
                        "Action folder '{}' not found.\nYou can create a 2GB ramdisk by executing:"
                        " `diskutil erasevolume HFS+ 'ramdisk' `hdiutil attach -nomount ram://4194304``"
                        .format(self.action_folder))

        self.dota_game = None
        self._ready = True
        self._time_last_call = time.time()
        super().__init__()

    
    async def watchdog(self):
        """The watchdog checks for timeouts, then cleans resources."""
        while True:
            await asyncio.sleep(self.WATCHDOG_TIMER)
            if self._ready == False and self.session_expired:
                self._ready = True
                await self.clean_resources()

    @property
    def ready(self):
        """Check if we are ready to play.

        The session will also be checked for expiration.
        """
        if not self._ready:
            if self.session_expired:
                self._ready = True
        return self._ready

    def set_call_timer(self):
        self._time_last_call = time.time()

    @property
    def session_expired(self):
        """Sessions expire after time sime, after which the current resource is available."""
        if self._ready:
            # Not applicable: when it's ready, there's no session, so not expired.
            return False
        dt = time.time() - self._time_last_call
        if dt > self.session_expiration_time:
            logger.info("Session expired.")
            return True
        return False

    @staticmethod
    def stop_dota_pids():
        """Stop all dota processes.
        
        Stopping dota is nessecary because only one client can be active at a time. So we clean
        up anything that already existed earlier, or a (hanging) mess we might have created.
        """
        dota_pids = str.split(os.popen("ps -e | grep dota2 | awk '{print $1}'").read())
        for pid in dota_pids:
            try:
                os.kill(int(pid), signal.SIGKILL)
            except ProcessLookupError:
                pass

    async def clean_resources(self):
        """Clean resoruces.
        
        Kill any previously running dota processes, and therefore set our status to ready.
        """
        # TODO(tzaman): Currently semi-gracefully. Can be cleaner.
        if self.dota_game is not None:
            # await self.dota_game.close()
            self.dota_game = None
        self.stop_dota_pids()

    async def clear(self, stream):
        """Cleans resources.

        Should be called when a user is done with a game, or when you want to nuke resources.
        """
        logger.debug('DotaService::clear()')
        await self.clean_resources()
        self._ready = True
        await stream.send_message(Empty())

    async def reset(self, stream):
        """reset method.

        This method should start up the dota game and the other required services.
        """
        logger.debug('DotaService::reset()')
        if not self.ready:
            logger.info('Resource currently exhausted: returning response.')
            await stream.send_message(Observation(status=Status.Value('RESOURCE_EXHAUSTED')))
            return
        logger.info('Starting new game.')
        self._ready = False
        self.set_call_timer()
        config = await stream.recv_message()
        logger.debug('config=\n{}'.format(config))

        await self.clean_resources()

        # Create a new dota game instance.
        self.dota_game = DotaGame(
            dota_path=self.dota_path,
            action_folder=self.action_folder,
            host_timescale=config.host_timescale,
            ticks_per_observation=config.ticks_per_observation,
            game_mode=config.game_mode,
            host_mode=config.host_mode,
            game_id=config.game_id,
        )

        # Start dota.
        asyncio.create_task(self.dota_game.run())

        # We first wait for the lua config. TODO(tzaman): do this in DotaGame?
        logger.debug('::reset is awaiting lua config..')
        lua_config = await self.dota_game.lua_config_future
        logger.debug('lua config received={}'.format(lua_config))

        # Cycle through the queue until its empty, then only using the latest worldstate.
        data = None
        try:
            while True:
                data = await asyncio.wait_for(
                    self.dota_game.worldstate_queue_radiant.get(), timeout=0.2)
        except asyncio.TimeoutError:
            pass

        if data is None:
            await stream.send_message(Observation(status=Status.Value('FAILED_PRECONDITION')))
            raise ValueError('Worldstate queue empty while lua bot is ready!')

        # Now write the calibration file.
        config = {
            'calibration_dota_time': data.dota_time,
        }
        logger.debug('Writing live_config={}'.format(config))
        self.dota_game.write_live_config(data=config)

        # Return the reponse
        await stream.send_message(Observation(status=Status.Value('OK'), world_state=data))

    async def step(self, stream):
        logger.debug('DotaService::step()')
        self.set_call_timer()
        request = await stream.recv_message()
        actions = MessageToDict(request.actions)

        logger.debug('actions=\n{}'.format(pformat(actions)))

        self.dota_game.write_action(data=actions)

        # We've started to assume our queue will only have 1 item.
        data = await self.dota_game.worldstate_queue_radiant.get()

        # Make sure indeed the queue is empty and we're entirely in sync.
        assert self.dota_game.worldstate_queue_radiant.qsize() == 0

        # Return the reponse.
        await stream.send_message(Observation(status=Status.Value('OK'), world_state=data))


async def serve(server, *, host, port):
    await server.start(host, port)
    logger.info('DotaService {} serving on {}:{}'.format(__version__, host, port))
    try:
        await server.wait_closed()
    except asyncio.CancelledError:
        server.close()
        await server.wait_closed()


async def grpc_main(loop, handler, host, port):
    server = Server([handler], loop=loop)
    asyncio.create_task(handler.watchdog())
    await serve(server, host=host, port=port)


def main(grpc_host, grpc_port, dota_path, action_folder, session_expiration_time):
    dota_service = DotaService(
        dota_path=dota_path,
        action_folder=action_folder,
        session_expiration_time=session_expiration_time,
        )
    loop = asyncio.get_event_loop()
    tasks = grpc_main(
        loop=loop,
        handler=dota_service,
        host=grpc_host,
        port=grpc_port,
    )

    loop.run_until_complete(tasks)
