#!/usr/bin/env python3

from parlai.core.params import ParlaiParser
from parlai.chat_service.services.telegram.websocket_manager import TelegramManager
import parlai.chat_service.utils.config as config_utils


SERVICE_NAME = 'websocket'


def setup_args():
    parser = ParlaiParser(False, False)
    parser.add_parlai_data_path()
    parser.add_chatservice_args()
    parser.add_websockets_args()
    return parser.parse_args()


def run(opt):
    opt['service'] = SERVICE_NAME
    manager = TelegramManager(opt)
    try:
        manager.start_task()
    except BaseException:
        raise
    finally:
        manager.shutdown()


if __name__ == '__main__':
    opt = setup_args()
    config_path = opt.get('config_path')
    config = config_utils.parse_configuration_file(config_path)
    opt.update(config['world_opt'])
    opt['config'] = config
    run(opt)
