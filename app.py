from flask import Flask, request, jsonify
import configparser

# Load the configuration file
config = configparser.RawConfigParser()
config.read('conf.ini')

app = Flask(__name__)


@app.route('/', methods=['GET'])
def start():
    return "started"


@app.route('/cam1Config', methods=['POST'])
def cam1_config():
    """
    Configure cam1
    :param: url, port, username, password
    :return: json(status, message)
    """
    url = request.json['url']
    port = request.json['port']
    username = request.json['username']
    password = request.json['password']

    try:
        config.set('CountCam1', 'url', str(url))
        config.set('CountCam1', 'port', str(port))
        config.set('CountCam1', 'username', str(username))
        config.set('CountCam1', 'password', str(password))

        with open('conf.ini', 'w') as configfile:
            config.write(configfile)

    except (FileNotFoundError, configparser.NoSectionError, configparser.NoOptionError,
            configparser.DuplicateOptionError, configparser.DuplicateSectionError) as er:
        return jsonify({'status': 'fail',
                        'message': ' Fail to configure cam1'})

    else:
        return jsonify({'status': 'success',
                        'message': 'Successfully configure cam1'})


@app.route('/cam2Config', methods=['POST'])
def cam2_config():
    """
    Configure cam2
    :param: url, port, username, password
    :return: json(status, message)
    """
    url = request.json['url']
    port = request.json['port']
    username = request.json['username']
    password = request.json['password']

    try:
        config.set('CountCam2', 'url', str(url))
        config.set('CountCam2', 'port', str(port))
        config.set('CountCam2', 'username', str(username))
        config.set('CountCam2', 'password', str(password))

        with open('conf.ini', 'w') as configfile:
            config.write(configfile)

    except (FileNotFoundError, configparser.NoSectionError, configparser.NoOptionError,
            configparser.DuplicateOptionError, configparser.DuplicateSectionError) as er:
        return jsonify({'status': 'fail'})

    else:
        return jsonify({'status': 'success'})


@app.route('/cam3Config', methods=['POST'])
def cam3_config():
    """
    Configure cam3
    :param:url, port , username, password
    :return: json(status, message)
    """
    url = request.json['url']
    port = request.json['port']
    username = request.json['username']
    password = request.json['password']

    try:
        config.set('CountCam3', 'url', str(url))
        config.set('CountCam3', 'port', str(port))
        config.set('CountCam3', 'username', str(username))
        config.set('CountCam3', 'password', str(password))

        with open('conf.ini', 'w') as configfile:
            config.write(configfile)

    except (FileNotFoundError, configparser.NoOptionError, configparser.NoSectionError,
            configparser.DuplicateOptionError, configparser.DuplicateSectionError) as er:
        return jsonify({'status': 'fail'})

    else:
        return jsonify({'status': 'success'})


if __name__ == '__main__':
    app.run(debug=True, host="localhost", port=7788)
