#! /usr/bin/env python3

import argparse
import asyncio
import logging
import os

import traceback
import sys

from fuocore import __version__ as fuocore_version
from fuocore.pubsub import run as run_pubsub

from feeluown import logger_config, __version__ as feeluown_version
from feeluown.config import config
from feeluown.consts import (
    HOME_DIR, USER_PLUGINS_DIR, PLUGINS_DIR, DATA_DIR,
    CACHE_DIR, USER_THEMES_DIR, SONG_DIR, COLLECTIONS_DIR
)
from feeluown.rcfile import load_rcfile, bind_signals
from feeluown.utils import is_port_used


logger = logging.getLogger(__name__)


def ensure_dirs():
    for d in (HOME_DIR, DATA_DIR,
              USER_THEMES_DIR, USER_PLUGINS_DIR,
              CACHE_DIR, SONG_DIR, COLLECTIONS_DIR):
        if not os.path.exists(d):
            os.mkdir(d)


def excepthook(exc_type, exc_value, tb):
    """Exception hook"""
    src_tb = tb
    while src_tb.tb_next:
        src_tb = src_tb.tb_next
    logger.error('Exception occured: print locals varibales')
    logger.error(src_tb.tb_frame.f_locals)
    traceback.print_exception(exc_type, exc_value, tb)


ensure_dirs()
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.append(PLUGINS_DIR)
sys.path.append(USER_PLUGINS_DIR)


def setup_argparse():
    parser = argparse.ArgumentParser(description='运行 FeelUOwn 播放器')
    parser.add_argument('-nw', '--no-window', action='store_true', default=False,
                        help='以 CLI 模式运行')

    parser.add_argument('-d', '--debug', action='store_true', default=False,
                        help='开启调试模式')
    parser.add_argument('-v', '--version', action='store_true',
                        help='显示当前 feeluown 和 fuocore 版本')
    parser.add_argument('--log-to-file', action='store_true', default=False,
                        help='将日志打到文件中')
    # XXX: 不知道能否加一个基于 regex 的 option？比如加一个
    # `--mpv-*` 的 option，否则每个 mpv 配置我都需要写一个 option？

    # TODO: 需要在文档中给出如何查看有哪些播放设备的方法
    parser.add_argument(
        '--mpv-audio-device',
        default='auto',
        help='（高级选项）给 mpv 播放器指定播放设备'
    )
    return parser


def main():
    parser = setup_argparse()
    args = parser.parse_args()

    if args.version:
        print('feeluown {}, fuocore {}'.format(feeluown_version, fuocore_version))
        return

    if is_port_used(23333) or is_port_used(23334):
        print('\033[0;31m', end='')
        print('Port(23333 or 23334) is used, maybe another feeluown is running?')
        print('\033[0m', end='')
        sys.exit(1)

    debug = args.debug
    mpv_audio_device = args.mpv_audio_device
    cli_only = args.no_window
    logger_config(debug, to_file=args.log_to_file)

    load_rcfile()

    player_kwargs = dict(
        audio_device=bytes(mpv_audio_device, 'utf-8'))

    # 设置 exception hook
    sys.excepthook = excepthook

    if not cli_only:
        try:
            import PyQt5  # noqa
        except ImportError:
            logger.warning('PyQt5 is not installed，can only use CLI mode.')
            cli_only = True

    if not cli_only:
        from PyQt5.QtWidgets import QApplication
        from quamash import QEventLoop
        from feeluown.guiapp import GuiApp

        q_app = QApplication(sys.argv)
        q_app.setQuitOnLastWindowClosed(True)
        q_app.setApplicationName('FeelUOwn')

        app_event_loop = QEventLoop(q_app)
        asyncio.set_event_loop(app_event_loop)
        pubsub_gateway, pubsub_server = run_pubsub()

        app = GuiApp(pubsub_gateway, player_kwargs=player_kwargs)
        app.config = config
        # 初始化 UI 和组件间信号绑定
        app.initialize()
        # TODO: 调用 show 时，会弹出主界面，但这时界面还没开始绘制
        # 为了让提升启动速度，一些非必须的初始化操作可以在 show 之后进行
        app.show()
    else:
        from feeluown.app import CliApp

        pubsub_gateway, pubsub_server = run_pubsub()
        app = CliApp(pubsub_gateway, player_kwargs=player_kwargs)
        app.config = config
        app.initialize()

    bind_signals(app)

    event_loop = asyncio.get_event_loop()
    app.protocol.run_server()
    try:
        event_loop.run_forever()
        logger.info('Event loop stopped.')
    except KeyboardInterrupt:
        # NOTE: gracefully shutdown?
        pass
    finally:
        pubsub_server.close()
        event_loop.close()


if __name__ == '__main__':
    main()
