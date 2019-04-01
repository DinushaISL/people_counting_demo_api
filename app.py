from flask import Flask, request, jsonify
import configparser
import os
import subprocess
import signal
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
        print(er)
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
        print(er)
        return jsonify({'status': 'fail'})

    else:
        return jsonify({'status': 'success'})


@app.route('/startPeopleCountCam1', methods=['GET'])
def start_process_count_cam1():
    """
    The api implementation to start people counting in cam1. Subprocess has been defined to start people counting
    python script for cam1.
    :return: json(status, message)
    """
    try:
        # print('process started')
        # process = subprocess.Popen(['C:/Python27/python.exe',
        #                             'people_count_cam_one.py'], shell=True, stdout=subprocess.PIPE)
        config.set('CountCam1', 'cond', 0)
        process = subprocess.Popen(['python3 people_count_cam_one.py'], shell=True, stdout=subprocess.PIPE)
        config.set('CountCam1', 'pid', str(process.pid))
        if config.has_option('CountCam1', 'pid'):
            subprocess.Popen(['cp conf.ini conf.ini.back'], shell=True, stdout=subprocess.PIPE)
            # subprocess.Popen(['copy conf.ini conf.ini.back'], shell=True, stdout=subprocess.PIPE)

        with open('conf.ini', 'w') as configfile:
                config.write(configfile)

    except (FileNotFoundError, configparser.NoOptionError, configparser.NoSectionError) as er:
        print(er)
        return jsonify({"status": "fail",
                        'message': 'Fail to start people counting for cam1'})

    else:
        return jsonify({"status": "success",
                        'message': 'Successfully start people counting process from cam1'})


@app.route('/endPeopleCountCam1', methods=['GET'])
def process_count_cam1():
    """
    The people counting process ending for cam1.
    :return: json(status, message)
    """
    try:
        config.set('CountCam1', 'cond', 1)
        with open('conf.ini', 'w') as configfile:
            config.write(configfile)

    except (os.error, configparser.NoSectionError, configparser.NoOptionError) as er:
        return jsonify({"status": "fail",
                        "message": "These is no started process going on. So please start the process first"})

    else:
        return jsonify({"status": "success",
                        'message': "Successfully end people counting process from cam1"})


# @app.route('/statusPeopleCountCam1', methods=['GET'])
# def process_status_cam1():
#     """
#     Keeping status of people counting from cam1.
#     :return: json(status, message)
#     """
#     try:
#         pid = config.get('CountCam1', 'pid')
#         # subprocess.check_output("ps -p " + str(pid) + " " + "-o user", shell=True)
#         # data.decode("utf-8")
#     except (configparser.NoOptionError, configparser.NoSectionError) as er:
#         print(er)
#         pid = config.get('CountCam1', 'pid')
#
#         return jsonify({'status': "No",
#                         'message': 'There is no process please start'})
#
#     else:
#         return jsonify({'status': "Yes",
#                         'message': "People counting process from cam1 is running successfully"})


# @app.route('/restartPeopleCountCam1', methods=['GET'])
# def process_restart_cam1():
#     """
#     Restart people counting process from cam1
#     :return: json(status, message)
#     """
#     try:
#         # with open('process_id.log', 'r') as file:
#         #     pid = file.readline()
#         #     pid = pid.split('\n', 1)[0]
#
#         # pid = config.get('CountCam1', 'pid')
#         # os.kill(int(pid), signal.SIGTERM)
#
#         # time.sleep(1)
#
#         process = subprocess.Popen(['python3 people_count_cam_one.py'], shell=True,
#                                    stdout=subprocess.PIPE)  # Should be change
#
#         # with open('process_id.log', 'w') as file_new:
#         #     file_new.write(str(process.pid) + '\n')
#         #     file_new.close
#         subprocess.Popen(['cp conf.ini conf.ini.back'], shell=True, stdout=subprocess.PIPE)
#         config.set('CountCam1', 'pid', str(process.pid))
#         with open('conf.ini', 'w') as configfile:
#             config.write(configfile)
#
#     except (os.error, FileNotFoundError, subprocess.CalledProcessError, subprocess.SubprocessError,
#             configparser.NoSectionError, configparser.NoOptionError) as er:
#         # app.logger.error("Process restart error:" + " " + str(er))
#         # print(er)
#         logging.error("Process start error in black detection because of:" + " " + str(er))
#         return jsonify({"status": "fail",
#                         'message': 'Fail to restart people counting process from cam1'})
#
#     else:
#         logging.info("People counting process from cam1 has been restarted successfully")
#         return jsonify({"status": "success",
#                         'message': 'Successfully restart people counting from cam1'})


@app.route('/startPeopleCountCam2', methods=['GET'])
def start_process_count_cam2():
    """
    Start people counting process for cam2
    :return: json(status, message)
    """
    try:
        process = subprocess.Popen(['python3 people_count_cam_two.py'], shell=True, stdout=subprocess.PIPE)

        # with open('process_id.log', 'w') as file:
        #     file.write(str(process.pid) + '\n')
        #     file.close()
        if config.has_option('CountCam2', 'pid'):
            subprocess.Popen(['cp conf.ini conf.ini.back'], shell=True, stdout=subprocess.PIPE)
            # subprocess.Popen(['copy conf.ini conf.ini.back'], shell=True, stdout=subprocess.PIPE)
            config.set('CountCam2', 'pid', str(process.pid))
            with open('conf.ini', 'w') as configfile:
                config.write(configfile)

    except (FileNotFoundError, subprocess.CalledProcessError, subprocess.SubprocessError,
            configparser.NoOptionError, configparser.NoSectionError) as er:
        # print(er)
        return jsonify({"status": "fail",
                        'message': 'Fail to start people counting for cam2'})

    else:
        return jsonify({"status": "success",
                        'message': 'Successfully start people counting process from cam2'})


@app.route('/endPeopleCountCam2', methods=['GET'])
def process_count_cam2():
    """
    End people counting process from cam2
    :return: json(status, message)
    """
    # with open('process_id.log', 'r') as file:
    #     pid = file.readline()
    #     pid = pid.split('\n', 1)[0]
    # subprocess.call(['./kill_process_id.sh', pid])
    try:
        pid = config.get('CountCam2', 'pid')
        os.kill(int(pid), signal.SIGTERM)

    except (os.error, configparser.NoSectionError, configparser.NoOptionError) as er:
        # app.logger.error("Process kill error:"+" "+str(er))
        # print(er)

        return jsonify({"status": "fail",
                        "message": "These is no started process going on. So please start the process first"})

    else:
        return jsonify({"status": "success",
                        'message': "Successfully end people counting process from cam2"})


# @app.route('/statusPeopleCountCam2', methods=['GET'])
# def process_status_cam2():
#     """
#     Check ststus of people counting process from cam2
#     :return: json(status, message)
#     """
#     try:
#         pid = config.get('CountCam2', 'pid')
#         subprocess.check_output("ps -p " + str(pid) + " " + "-o user", shell=True)
#         # data.decode("utf-8")
#     except (subprocess.CalledProcessError, configparser.NoOptionError, configparser.NoOptionError) as er:
#         # app.logger.error("Process status checking error:" + " " + str(er))
#         pid = config.get('CountCam2', 'pid')
#
#         # print(er)
#
#         return jsonify({'status': "No",
#                         'message': 'There is no process please start'})
#
#     else:
#         logging.info("People counting process from cam2 already running in background @{0} process id".format(pid))
#         return jsonify({'status': "Yes",
#                         'message': "People counting process from cam2 is running successfully"})


# @app.route('/restartPeopleCountCam2', methods=['GET'])
# def process_restart_cam2():
#     """
#     Restart people counting from cam2
#     :return: json(status, message)
#     """
#     try:
#         # with open('process_id.log', 'r') as file:
#         #     pid = file.readline()
#         #     pid = pid.split('\n', 1)[0]
#
#         pid = config.get('CountCam2', 'pid')
#         os.kill(int(pid), signal.SIGTERM)
#
#         time.sleep(1)
#
#         process = subprocess.Popen(['python3 people_count_cam_two.py'], shell=True,
#                                    stdout=subprocess.PIPE)  # Should be change
#
#         # with open('process_id.log', 'w') as file_new:
#         #     file_new.write(str(process.pid) + '\n')
#         #     file_new.close()
#
#         if config.has_option('CountCam2', 'pid'):
#             subprocess.Popen(['cp conf.ini conf.ini.back'], shell=True, stdout=subprocess.PIPE)
#             config.set('CountCam2', 'pid', str(process.pid))
#             with open('conf.ini', 'w') as configfile:
#                 config.write(configfile)
#
#     except (os.error, FileNotFoundError, subprocess.CalledProcessError, subprocess.SubprocessError,
#             configparser.NoOptionError, configparser.NoSectionError) as er:
#         # app.logger.error("Process restart error:" + " " + str(er))
#         # print(er)
#         logging.error("Process start error in black detection because of:" + " " + str(er))
#         return jsonify({"status": "fail",
#                         'message': 'Fail to restart people counting process from cam2'})
#
#     else:
#         logging.info("People counting process from cam2 has been restarted successfully")
#         return jsonify({"status": "success",
#                         'message': 'Successfully restart people counting from cam2'})


@app.route('/startPeopleCountCam3', methods=['GET'])
def start_process_count_cam3():
    """
    Start of people counting process from cam3
    :return: json(status, message)
    """
    try:
        process = subprocess.Popen(['python3 people_count_cam_three.py'], shell=True, stdout=subprocess.PIPE)

        # with open('process_id.log', 'w') as file:
        #     file.write(str(process.pid) + '\n')
        #     file.close()
        if config.has_option('CountCam3', 'pid'):
            subprocess.Popen(['cp conf.ini conf.ini.back'], shell=True, stdout=subprocess.PIPE)
            # subprocess.Popen(['copy conf.ini conf.ini.back'], shell=True, stdout=subprocess.PIPE)
            config.set('CountCam3', 'pid', str(process.pid))
            with open('conf.ini', 'w') as configfile:
                config.write(configfile)

    except (FileNotFoundError, subprocess.CalledProcessError, subprocess.SubprocessError,
            configparser.NoSectionError, configparser.NoOptionError) as er:

        # print(er)
        return jsonify({"status": "fail",
                        'message': 'Fail to start people counting for cam3'})

    else:
        return jsonify({"status": "success",
                        'message': 'Successfully start people counting process from cam3'})


@app.route('/endPeopleCountCam3', methods=['GET'])
def process_count_cam3():
    """
    End people counting process from cam3
    :return: json(status, message)
    """
    # with open('process_id.log', 'r') as file:
    #     pid = file.readline()
    #     pid = pid.split('\n', 1)[0]
    # subprocess.call(['./kill_process_id.sh', pid])
    try:
        pid = config.get('CountCam3', 'pid')
        os.kill(int(pid), signal.SIGTERM)

    except (os.error, configparser.NoOptionError, configparser.NoSectionError) as er:
        # app.logger.error("Process kill error:"+" "+str(er))
        return jsonify({"status": "fail",
                        "message": "These is no started process going on. So please start the process first"})

    else:
        return jsonify({"status": "success",
                        'message': "Successfully end people counting process from cam3"})


# @app.route('/statusPeopleCountCam3', methods=['GET'])
# def process_status_cam3():
#     """
#     Keeping status of people counting process from cam3
#     :return: json(status, message)
#     """
#     try:
#         pid = config.get('CountCam3', 'pid')
#         subprocess.check_output("ps -p " + str(pid) + " " + "-o user", shell=True)
#         # data.decode("utf-8")
#     except (subprocess.CalledProcessError, configparser.NoSectionError, configparser.NoOptionError) as er:
#         # app.logger.error("Process status checking error:" + " " + str(er))
#         pid = config.get('CountCam3', 'pid')
#         logging.error("Process status checking error @{0} process id because:".format(pid) + " " + str(er))
#
#         # print(er)
#
#         return jsonify({'status': "No",
#                         'message': 'There is no process please start'})
#
#     else:
#         logging.info("People counting process from cam3 already running in background @{0} process id".format(pid))
#         return jsonify({'status': "Yes",
#                         'message': "People counting process from cam3 is running successfully"})


# @app.route('/restartPeopleCountCam3', methods=['GET'])
# def process_restart_cam3():
#     """
#     Restart people counting process from cam3
#     :return: json(status, message)
#     """
#     try:
#         # with open('process_id.log', 'r') as file:
#         #     pid = file.readline()
#         #     pid = pid.split('\n', 1)[0]
#
#         pid = config.get('CountCam3', 'pid')
#         os.kill(int(pid), signal.SIGTERM)
#
#         time.sleep(1)
#
#         process = subprocess.Popen(['python3 people_count_cam_three.py'], shell=True,
#                                    stdout=subprocess.PIPE)  # Should be change
#
#         # with open('process_id.log', 'w') as file_new:
#         #     file_new.write(str(process.pid) + '\n')
#         #     file_new.close()
#
#         if config.has_option('CountCam3', 'pid'):
#             subprocess.Popen(['cp conf.ini conf.ini.back'], shell=True, stdout=subprocess.PIPE)
#             config.set('CountCam3', 'pid', str(process.pid))
#             with open('conf.ini', 'w') as configfile:
#                 config.write(configfile)
#
#     except (os.error, FileNotFoundError, subprocess.CalledProcessError, subprocess.SubprocessError,
#             configparser.NoOptionError, configparser.NoSectionError) as er:
#         # app.logger.error("Process restart error:" + " " + str(er))
#         # print(er)
#         logging.error("Process start error in black detection because of:" + " " + str(er))
#         return jsonify({"status": "fail",
#                         'message': 'Fail to restart people counting process from cam3'})
#
#     else:
#         logging.info("People counting process from cam3 has been restarted successfully")
#         return jsonify({"status": "success",
#                         'message': 'Successfully restart people counting from cam3'})


if __name__ == '__main__':
    app.run(debug=True, host="localhost", port=7788)
