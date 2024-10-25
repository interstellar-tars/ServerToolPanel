from flask import Flask, render_template, request, redirect, url_for, flash
import os
import psutil

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace this with a secure random key

NGINX_CONFIG_PATH = "/etc/nginx/nginx.conf"  # Nginx config path

# Helper function to get system stats
def get_system_stats():
    return {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage('/').percent,
        "load_avg": os.getloadavg()
    }

# Homepage with server stats and file editor form
@app.route('/')
def index():
    stats = get_system_stats()
    return render_template('index.html', stats=stats)

# Route to view and edit the Nginx configuration file
@app.route('/edit_nginx', methods=['GET', 'POST'])
def edit_nginx():
    if request.method == 'POST':
        # Get the edited content and save it to the Nginx config file
        new_content = request.form.get('file_content')
        try:
            with open(NGINX_CONFIG_PATH, 'w') as f:
                f.write(new_content)
            flash("Nginx configuration updated successfully!", "success")
        except Exception as e:
            flash(f"Failed to save file: {e}", "error")
        return redirect(url_for('edit_nginx'))
    
    # Load the current content of the Nginx config file
    try:
        with open(NGINX_CONFIG_PATH, 'r') as f:
            file_content = f.read()
    except Exception as e:
        flash(f"Could not read Nginx config file: {e}", "error")
        file_content = ""
    
    return render_template('edit_nginx.html', file_content=file_content)

# Route to restart Nginx service (optional)
@app.route('/restart_nginx', methods=['POST'])
def restart_nginx():
    try:
        os.system("sudo systemctl restart nginx")  # Restart command
        flash("Nginx restarted successfully!", "success")
    except Exception as e:
        flash(f"Failed to restart Nginx: {e}", "error")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
