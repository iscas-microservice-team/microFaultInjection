from app import app
from flask import jsonify
from flask import request
from func_pack import fault_injection


# API-test GET Method
@app.route('/test-api', methods=['GET'])
def test_get():
    data = [
        {'test-api': 'API Test Success.'}
    ]
    return jsonify(data)


# Fault-Injection Method
@app.route('/fault-inject', methods=['POST'])
def inject_fault():
    fault_type = request.form.get('fault_type')
    thread_num = request.form.get('thread_num')
    duration = request.form.get('duration')
    mem_size = request.form.get('mem_size')
    io_times = request.form.get('io_times')
    net_port = request.form.get('net_port')
    net_flag = request.form.get('net_flag')
    # deliver all the args from POST into fault_injection
    result = fault_injection(fault_type, thread_num=thread_num, duration=duration, mem_size=mem_size,
                             io_times=io_times, net_port=net_port, net_flag=net_flag)
    if result is not None:
        return jsonify(result)
    else:
        info = [
            {'Info': 'Your faults are injecting. Please wait.'}
        ]
        return jsonify(info)
