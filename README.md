# CloudNest
## Hybrid Cloud Infrastructure Automation and Self-Healing Platform

**Project tagline:** Building a Production-Style Infrastructure using Linux, Docker, Python, Networking and AWS.

## 1. Project Overview

CloudNest is a learning-focused hybrid infrastructure project that combines a local Ubuntu Server home lab with AWS cloud services.

The project demonstrates containerized services, private networking, infrastructure monitoring, basic automatic recovery, scheduled health checks, report generation and cloud storage.

The goal is to understand practical Infrastructure, DevOps and Cloud Engineering workflows.

## 2. Technologies Used

- Ubuntu Server 24.04 LTS
- Docker and Docker Compose
- Python 3
- Nginx
- MySQL 8
- WireGuard VPN
- Linux cron
- AWS EC2
- Amazon S3
- Amazon EBS snapshots
- AWS IAM
- AWS CLI

## 3. Architecture

### Local Home Lab

Client
  |
  | HTTP :8081
  v
Nginx container :80
  |
  | Reverse proxy
  v
Python application :5000
  |
  | MySQL service configured
  v
MySQL container :3306

Python health monitor checks the required containers.
Cron schedules the monitor every five minutes.
The report generator creates a health report from the log.

### AWS Integration

AWS EC2 runs the CloudNest containerized project.
An EC2 IAM role grants scoped access to the CloudNest S3 bucket.
S3 stores backup/test objects.
EBS snapshots provide a point-in-time volume backup.

WireGuard provides a private VPN path between configured peers.

## 4. Docker Services

The Docker Compose project contains three services:

### Python Application
- Built from the local Dockerfile.
- Runs a Python HTTP server on port 5000.
- Displays a CloudNest welcome message and configured database details.
- Runs as a non-root user.
- Uses a read-only container filesystem and drops Linux capabilities.

### Nginx
- Uses the nginx:alpine image.
- Publishes host port 8081 to container port 80.
- Acts as a reverse proxy to the Python app.

### MySQL
- Uses the mysql:8 image.
- Stores database files in the persistent Docker volume
  `cloudnest-db-data`.

The Compose services communicate over the Docker Compose network.

## 5. Python Automation

### Health Monitor

File: `cloudnest-automation/health_monitor.py`

The script:
1. Retrieves running container names using Docker.
2. Checks the required Python, Nginx and MySQL containers.
3. Attempts to start `cloudnest-python` if it is stopped.
4. Checks container status again.
5. Reports the infrastructure as HEALTHY or UNHEALTHY.

The script currently attempts automatic recovery only for the Python container.

### Scheduled Monitoring

A cron job runs the health monitor every five minutes.
Output and errors are appended to `health_monitor.log`.

### Health Report Generator

File: `cloudnest-automation/report_generator.py`

The report generator reads the health-monitor log and writes
`health_report.txt` with a timestamp and the latest health-monitor result.

## 6. WireGuard Networking

WireGuard was configured for private communication between peers.

- VPN server address: `10.8.0.1`
- Windows peer address: `10.8.0.2`
- WireGuard UDP port: `51820`

The server configuration uses a specific peer address rather than
allowing all IPv4 addresses.

The final live client handshake test remains pending because the
second laptop was unavailable during final testing.

## 7. AWS Integration
### EC2
CloudNest was deployed on an Ubuntu EC2 instance in the Mumbai region
(ap-south-1).

### S3
The project uses the bucket `cloudnest-yukti-2026-backup`.
Public access is blocked, and server-side encryption with SSE-S3 is enabled.

### IAM
The EC2 instance uses an attached IAM role instead of storing
long-term AWS access keys on the instance.
The custom policy provides scoped access to the project bucket.

### EBS
An EBS snapshot was created as part of the cloud backup exercises.

AWS resources can incur charges even when the EC2 instance is stopped.
Resource usage and billing should be checked regularly.

## 8. Testing and Results

| Test | Result |
|---|---|
| Docker Compose services listed | PASS |
| Python, Nginx and MySQL containers running | PASS |
| Python container health check | PASS |
| CloudNest page through Nginx | PASS — HTTP 200 OK |
| Health monitor reports containers | PASS |
| Python container recovery test | PASS |
| Cron job configured every five minutes | PASS |
| Health-monitor output logged | PASS |
| Health report generated | PASS |
| MySQL TCP connectivity test | PASS |
| Application executes a MySQL query | NOT IMPLEMENTED |
| Final live WireGuard client handshake | PENDING |

The successful HTTP test returned the CloudNest welcome page.
The health report showed all three required containers as RUNNING.

The MySQL TCP test verified network connectivity only.
The current Python application does not establish a database
connection or execute SQL queries.

## 9. Security Measures

- The Python application runs as a non-root user.
- The Python container drops Linux capabilities.
- The Python container uses a read-only root filesystem.
- MySQL data is stored in a Docker volume.
- Environment variables are used for configuration and credentials.
- The `.env` file is excluded from version control.
- AWS access uses an EC2 IAM role with scoped permissions.
- S3 public access is blocked.
- SSH access should be restricted to a trusted source IP.
- Private keys, passwords and secret values must not be committed.

## 10. Known Limitations
- The Python app displays database configuration but does not query MySQL.
- Automatic recovery currently targets only the Python container.
- The health monitor checks whether containers are running; it does
  not fully validate every application's internal functionality.
- The final WireGuard client handshake test is pending.
- The project is a learning home lab, not a production-certified platform.

## 11. Future Scope

- Add real MySQL connection and database queries.
- Extend recovery to additional services.
- Add alerting through email or messaging.
- Improve monitoring and failure-recovery metrics.
- Integrate Kubernetes as a future orchestration layer.
- Add more detailed AWS monitoring and cost evaluation.

## 12. Conclusion

CloudNest demonstrates practical experience with Linux administration,
Docker containerization, reverse proxying, private networking,
Python automation and AWS infrastructure.

The project provides a foundation for further learning in DevOps,
Cloud Engineering, infrastructure monitoring and orchestration.
