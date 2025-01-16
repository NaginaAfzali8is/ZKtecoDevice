from flask import Flask, jsonify
from zk import ZK

app = Flask(__name__)

# Device configuration
zk = ZK('192.168.50.96', port=4370, timeout=5)

@app.route('/users', methods=['GET'])
def get_users_with_attendance():
    try:
        # Connect to the device
        conn = zk.connect()
        print("Connected to the device")

        # Retrieve users
        users = conn.get_users()
        user_data = []
        for user in users:
            user_info = {
                'user_id': user.user_id,
                'name': user.name,
                'privilege': user.privilege,
                'password': user.password,
                'card': user.card,
                'group_id': user.group_id
            }
            user_data.append(user_info)

        # Retrieve attendance records
        attendance_records = conn.get_attendance()
        attendance_data = []
        if attendance_records:
            for record in attendance_records:
                attendance_data.append({
                    'user_id': record.user_id,
                    'timestamp': record.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                    'status': record.status
                })

        conn.disconnect()

        # Return JSON response
        return jsonify({
            'users': user_data,
            'attendance': attendance_data
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
