import os
import argparse
from ts3ekkoutil.envconsts import EkkoPropertyNames as epn


def add_env_option(parser, name, env_name, env_default=None, **kwargs):
    parser.add_argument(name, default=os.environ.get(env_name, env_default), dest=env_name, **kwargs)


def create_ekko_parser():
    parser = argparse.ArgumentParser()
    add_env_option(parser, '--ts3-server-host', epn.TS3_SERVER_HOST, 'localhost',
                   help='Hostname/ip of ts3 server')
    add_env_option(parser, '--ts3-server-port', epn.TS3_SERVER_PORT, '9987',
                   help='Port of the ts3 server')

    add_env_option(parser, '--ts3-username', epn.TS3_USERNAME, 'EkkoBot',
                   help='Username of the bot')

    add_env_option(parser, '--ts3-identity', epn.TS3_IDENTITY,
                   help='Identity to be used for the bot')
    add_env_option(parser, '--ts3-unique-id', epn.TS3_UNIQUE_ID,
                   help='Unique ID, used to identify the bots own actions')
    add_env_option(parser, '--ts3-client-apikey', epn.TS3_CLIENT_APIKEY,
                   help='ClientQuery apikey, configured in the ts3 client docker image')

    add_env_option(parser, '--ts3-channel-name', epn.TS3_CHANNEL_NAME,
                   help='Channel name to which the bot should connect')
    add_env_option(parser, '--ts3-channel-id', epn.TS3_CHANNEL_ID,
                   help='Channel ID to which the bot should connect')
    add_env_option(parser, '--ts3-channel-password', epn.TS3_CHANNEL_PASSWORD,
                   help='Channel password for the channel the bot is connecting to')
    add_env_option(parser, '--ts3-server-password', epn.TS3_SERVER_PASSWORD,
                   help='Password to the ts3 server')
    add_env_option(parser, '--ts3-server-permission-token', epn.TS3_SERVER_PERMISSION_TOKEN,
                   help='Permission token to claim rights on the ts3 server.')

    add_env_option(parser, '--ts3-identity-database-preconf', epn.TS3_IDENTITY_DATABASE_PRECONF,
                   help='Identity string which is pre-configured in the ProtobufItems table'
                        ' in the settings.db inside of the deployed client instance.')
    add_env_option(parser, '--ts3-identity-database-key', epn.TS3_IDENTITY_DATABASE_KEY,
                   help='Identitfier key of the record in the ProtobufItems table in the settings.db configuration '
                        'database, which should be used for the identity modification')
    add_env_option(parser, '--ekko-node-id', epn.EKKO_NODE_ID,
                   help='Identifier for each ekko client node')

    add_env_option(parser, '--ts3-clientquery-host', epn.TS3_CLIENTQUERY_HOST, 'localhost',
                   help='Host used by the TS3 Client to provide the ClientQuery endpoint')
    add_env_option(parser, '--ts3-clientquery-port', epn.TS3_CLIENTQUERY_PORT, '25639',
                   help='Port used by the TS3 Client to provide the ClientQuery endpoint')

    add_env_option(parser, '--ts3-config-directory', epn.TS3_CONFIG_DIRECTORY, '/root/.ts3client/',
                   help='Directory in which the TS3 configuration files are (.ts3client, files are e.g. settings.db)')
    add_env_option(parser, '--ekko-media-directory-source', epn.EKKO_MEDIA_DIRECTORY_SOURCE, '/var/media/',
                   help='Directory in which files for playback from filesystem are stored on the docker host. '
                        'This directory will be mounted to the directory defined by `--ekko-media-directory`.')
    add_env_option(parser, '--ekko-media-directory', epn.EKKO_MEDIA_DIRECTORY, '/mnt/media/',
                   help='Directory in which files for playback from filesystem are stored')
    add_env_option(parser, '--teamspeak-directory', epn.TS3_DIRECTORY, '/opt/TeamSpeak3-Client-linux_amd64/',
                   help='Directory in which teamspeak was installed')
    add_env_option(parser, '--teamspeak-runscript', epn.TS3_RUNSCRIPT, 'ts3client_runscript.sh',
                   help='Filename of the runscript in the teamspeak directory (see --teamspeak-directory)')
    add_env_option(parser, '--docker-ekkoclient-build', epn.DOCKER_EKKO_CLIENT_BUILD, action='store_true',
                   help='Build the ekkoclient image instead of downloading the built one', env_default=False)
    add_env_option(parser, '--docker-ekkoclient-directory', epn.DOCKER_EKKO_CLIENT_DIRECTORY,
                   help='Source directory for building the ekkoclient image')
    add_env_option(parser, '--docker-network-name', epn.DOCKER_NETWORK_NAME,
                   help='Name of the docker network for the ekko ensamble.')
    add_env_option(parser, '--docker-debug-diable-autoremove', epn.DOCKER_DISABLE_AUTOREMOVE, action='store_true',
                   help='Do not remove the containers of exited ekko clients (only for debug purposes, '
                        'results in errors in case manager tries to create existing containers)')
    add_env_option(parser, '--docker-ekkoclient-image-name', epn.DOCKER_EKKO_CLIENT_IMAGE_NAME, 'ekkoclient',
                   help='Name of the ekko client image')
    add_env_option(parser, '--docker-ekkoclient-image-tag', epn.DOCKER_EKKO_CLIENT_IMAGE_TAG, 'latest',
                   help='Tag of the ekko client image')
    add_env_option(parser, '--docker-network-dblink', epn.DOCKER_NETWORK_DBLINK, 'db:dbhost',
                   help='Link descriptor for database<->ekkoclient link')
    add_env_option(parser, '--ekko-client-control-port', epn.EKKO_CLIENT_CONTROL_PORT, '8080',
                   help='Port on which the ekkoclients offer the control service.')

    add_env_option(parser, '--fixtures-path', epn.EKKO_FIXTURES_PATH,
                   help='Path of the directory which includes seed/fixture files for database initialization')
    add_env_option(parser, '--permission-path', epn.EKKO_PERMISSION_PATH,
                   help='Path to the yaml permission file (for ts3ekkosingle)')

    add_env_option(parser, '--db-username', epn.DB_USERNAME,
                   help='application database username')
    add_env_option(parser, '--db-password', epn.DB_PASSWORD,
                   help='application database password')
    add_env_option(parser, '--db-host', epn.DB_HOST,
                   help='application database host')
    add_env_option(parser, '--db-dbname', epn.DB_DBNAME,
                   help='application database name')



    add_env_option(parser, '--ekko-manage-server', epn.EKKO_MANAGE_SERVER, 'ts3ekkomanage',
                   help='Hostname/ip of the server on which the ts3ekko management instance runs')
    add_env_option(parser, '--ekko-manage-port', epn.EKKO_MANAGE_PORT, '8180',
                   help='Port on which the ts3ekko manage api can be reached')

    add_env_option(parser, '--log-level', epn.LOG_LEVEL, 0,
                   help='Log level for all ekko applications')
    add_env_option(parser, '--log-format', epn.LOG_FORMAT, '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                   help='Format in which the log messages are written')

    add_env_option(parser, '--cog-media-volume-modifier', epn.COG_MEDIA_VOLUME_MODIFIER, 0.2, type=float,
                   help='(MediaCog) Ratio by which the volume gets recalculated for the media player.')
    add_env_option(parser, '--cog-media-volume-max', epn.COG_MEDIA_VOLUME_MAX, 500, type=int,
                   help='(MediaCog) Maximum allowed volume.')
    add_env_option(parser, '--cog-media-alias-prefix', epn.COG_MEDIA_ALIAS_PREFIX, '\$',
                   help='(MediaCog) Prefix used to a mark media alias.')

    return parser
