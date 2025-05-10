# AlmaLinux Flask App Deployment & Management Guide

This guide provides instructions for deploying, running, and managing the Flask application on an AlmaLinux server.

## Project Setup

*   **Project Directory:** `/home/almalinux/pharma-admin/`
*   **Virtual Environment Name:** `venv` (located at `/home/almalinux/pharma-admin/venv/`)
*   **Systemd Service Name:** `pharma_admin.service`

## Initial Deployment / Setup

1.  **SSH into your VPS:**
    ```bash
    ssh your_username@your_vps_ip
    ```

2.  **Install System Packages (if not already done):**
    ```bash
    sudo dnf update -y
    sudo dnf install -y git python3 python3-pip python3-devel
    ```

3.  **Clone the Project:**
    ```bash
    cd /home/almalinux # or your preferred base directory
    git clone <your_repository_url> pharma-admin
    cd pharma-admin
    ```

4.  **Create and Activate Virtual Environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
    *(Your prompt should now show `(venv)`)*

5.  **Install Python Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

6.  **Configure Environment Variables:**
    Create or edit the `.env` file in the project root (`/home/almalinux/pharma-admin/.env`):
    ```env
    FLASK_APP=app.py
    FLASK_ENV=production
    SECRET_KEY=your_very_strong_and_unique_secret_key 
    DATABASE_URL=sqlite:///app.db 
    # Add any other necessary environment variables
    ```
    *(Generate a strong `SECRET_KEY`)*

7.  **Initialize the Database (Create Tables & Seed Data):**
    ```bash
    python scripts/init_db.py
    ```

8.  **Import Pharmaceutical Data (if applicable):**
    *(Ensure `json_data` directory and files are present)*
    ```bash
    python scripts/import_data.py
    ```

9.  **Set up Firewall (Port 5000 for Gunicorn):**
    ```bash
    sudo firewall-cmd --permanent --add-port=5000/tcp
    sudo firewall-cmd --reload
    ```
    *(Adjust port if Gunicorn uses a different one. Also check cloud provider firewalls.)*

10. **Create and Configure Systemd Service (`pharma_admin.service`):**
    Create `/etc/systemd/system/pharma_admin.service` with `sudo nano`:
    ```ini
    [Unit]
    Description=Gunicorn instance for Pharma App
    After=network.target

    [Service]
    User=almalinux
    Group=almalinux
    WorkingDirectory=/home/almalinux/pharma-admin
    EnvironmentFile=/home/almalinux/pharma-admin/.env
    Environment="PATH=/home/almalinux/pharma-admin/venv/bin"
    # The following ExecStart line is the one we need to finalize for Gunicorn
    ExecStart=/home/almalinux/pharma-admin/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:5000 wsgi:app 
    Restart=always # Or on-failure

    [Install]
    WantedBy=multi-user.target
    ```
    *(We are still troubleshooting this `ExecStart` for Gunicorn. The simple test worked, now we revert to the Gunicorn command.)*

11. **Enable and Start the Service:**
    ```bash
    sudo systemctl daemon-reload
    sudo systemctl enable pharma_admin.service
    sudo systemctl start pharma_admin.service 
    ```

## Managing the Application

### Check Service Status
```bash
sudo systemctl status pharma_admin.service
```

### Start the Service
```bash
sudo systemctl start pharma_admin.service
```

### Stop the Service
```bash
sudo systemctl stop pharma_admin.service
```

### Restart the Service
(e.g., after code changes or configuration updates)
```bash
sudo systemctl restart pharma_admin.service
```

### View Service Logs
```bash
sudo journalctl -u pharma_admin.service 
# For more details or live logs:
sudo journalctl -f -u pharma_admin.service
sudo journalctl -xeu pharma_admin.service # For extended error details
```

### Updating the Application (Pulling Changes from Git)

1.  **SSH into your VPS and navigate to the project directory:**
    ```bash
    ssh your_username@your_vps_ip
    cd /home/almalinux/pharma-admin
    ```

2.  **Activate the virtual environment:**
    ```bash
    source venv/bin/activate
    ```

3.  **Pull the latest changes from your Git repository:**
    ```bash
    git pull origin main # Or your primary branch name
    ```

4.  **Install/Update Dependencies (if `requirements.txt` changed):**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Apply Database Migrations (if any):**
    *(Your `scripts/init_db.py` might handle this via its `upgrade()` call, or you might run `flask db upgrade` directly if that's your process)*
    ```bash
    # Option 1: If init_db.py handles migrations
    python scripts/init_db.py 
    # Option 2: If you manage migrations separately
    # flask db upgrade 
    ```

6.  **Restart the Application Service:**
    ```bash
    sudo systemctl restart pharma_admin.service
    ```

## Troubleshooting Systemd Service

*   If the service fails to start, always check `sudo systemctl status pharma_admin.service` and `sudo journalctl -xeu pharma_admin.service` first.
*   The `217/USER` error often relates to user permissions, paths in the service file, or environment variables.
*   The `resources` error can be tricky, often related to systemd's inability to set up the execution context.
*   Ensure all paths in the `.service` file (WorkingDirectory, EnvironmentFile, ExecStart, PATH in Environment) are absolute and correct.
*   Verify the `User` and `Group` directives are correct.

---
This file should serve as a good quick reference. We still need to fix the Gunicorn `ExecStart` in your systemd service. 