#!/bin/bash
# Start the level 16/19 gatekeepers, the level 17 process, then sshd.
python3 /opt/mineshaft/services.py &
(exec -a "gem-keeper --guarding-the-gems --secret=$(cat /etc/mineshaft/keeper-secret)" sleep infinity) &
exec /usr/sbin/sshd -D -e
