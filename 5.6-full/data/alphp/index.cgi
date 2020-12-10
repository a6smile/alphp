#!/bin/sh
# Control Panel v0.0 - alphp 5.6 web-based user interface.
#
MYSQL_DATA_DIR=/root/data
MYSQL_USER=root
MYSQL_PASSWORD=root

log_read() {
    while IFS= read -r; do
        REPLY=${REPLY/*[/[}
        REPLY=${REPLY//&/&amp;}
        REPLY=${REPLY//</&lt;}
        REPLY=${REPLY//>/&gt;}
        printf '%s' "$REPLY<br />"
    done < "$ALPHP_LOG_FILE"
}

mysql_start() {
    log_size=$( stat -c %s "$ALPHP_LOG_FILE" )
    ( mysqld --user="$MYSQL_USER" --datadir="$MYSQL_DATA_DIR" >> "$ALPHP_LOG_FILE" 2>&1 & )
    while [ "$( stat -c %s "$ALPHP_LOG_FILE" )" -eq "$log_size" ]; do
        sleep 1
    done
}

mysql_started() {
    pidof -s mysqld > /dev/null 2>&1
}

if mysql_started; then
    mysql_status='<span class="success">Berjalan</span>'
    qs=mysql-stop
    bs=Hentikan
    pma='<a href="/phpmyadmin">phpMyAdmin &raquo;</a>'
else
    mysql_status='<span class="error">Berhenti</span>'
    qs=mysql-start
    bs=Mulai
    pma='<span class="disabled">phpMyAdmin &raquo;</span>'
fi

echo "Content-Type: text/html; charset=ISO-8859-1"
echo "Cache-Control: no-cache, must-revalidate"
echo "Expires: Thu, 01 Jan 1970 00:00:00 GMT"
echo

case $QUERY_STRING in
    mysql-start*)
        if [ ! -d "$MYSQL_DATA_DIR/mysql" ]; then
            mysql_install_db --datadir="$MYSQL_DATA_DIR" > /dev/null 2>&1
            mysql_start
            if mysql_started; then
                echo "Database \"mysql\" berhasil dibuat di $MYSQL_DATA_DIR" >> "$ALPHP_LOG_FILE"
                mysqladmin --user="$MYSQL_USER" password "$MYSQL_PASSWORD"
                [ -f "$MYSQL_DATA_DIR/create_tables.sql" ] && mysql --user="$MYSQL_USER" --password="$MYSQL_PASSWORD" < "$MYSQL_DATA_DIR/create_tables.sql"
            fi
        fi
        mysql_started || mysql_start
        printf '%s\n%s\n%s\n%s\n%s' '<span class="success">Berjalan</span>' "mysql-stop" "Hentikan" "$( pgrep -o ^mysqld$ )" "$( log_read )"
        exit
        ;;
    mysql-stop*)
        killall mysqld
        while mysql_started; do
            sleep 1
        done
        printf '%s\n%s\n%s\n%s\n%s' '<span class="error">Berhenti</span>' "mysql-start" "Mulai" "" "$( log_read )"
        exit
        ;;
    log-clear*)
        : > "$ALPHP_LOG_FILE"
        printf "1"
        exit
        ;;
esac

cat <<EOL
<!DOCTYPE html>
<html lang="id">
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>alphp 5.6 Control Panel</title>
        <style>
        body { background-color: #dcf2f1; font-family: sans-serif; font-size: 16px; color: #222; max-width: 600px; margin: 0 auto; }

        table { background-color: #fff; width: 100%; }
        table, table tr, table td { margin: 0; padding: 6px; padding-left: 12px; padding-right: 12px; border: 0; border-spacing: 0; border-collapse: collapse; }

        #header td { margin: 0; padding: 0; background-color: #43b3ae; color: #fff; }
        #header h1 { margin: 0; padding: 12px; font-size: 1.5em; }
        #header pre { margin: 0; padding: 12px; font-family: monospace; font-size: .875em; }
        #header a { color: #fff; }
        #title td { padding-top: 12px; font-size: .9375em; }
        .content td, button, .success, .error { font-size: .9375em; }
        .content #log { background: #fff; color: #343a40; border: 1px solid #ccc; width: 100%; height: 240px; overflow: scroll; }
        #footer td { padding-bottom: 12px; font-size: .875em; color: #767676; }

        button { background-color: #43b3ae; color: #fff; border: 0; border-radius: .25rem; width: 100%; height: 32px; margin: 0; padding: 0; }
        button:hover { background-color: #208d88; }
        button.disabled { background-color: #b1e2e0; }
        #pma .disabled, #copyright a { color: #767676; }

        .text_right { text-align: right; }
        a { text-decoration: none; color: #43b3ae; }

        .success { background-color: #5cdb95; color: #fff; }
        .error { background-color: #f86f7d; color: #fff; }
        .success, .error { padding: 2px; padding-left: 4px; padding-right: 4px; }
        </style>
    </head>
    <body>
        <table>
            <tr id="header">
                <td colspan="2"><a href="/alphp/"><pre>
  _ | _ |_  _    
 (_|||_)| ||_)   
     |     |  5.6
</pre></a></td><td colspan="3"><h1>Control Panel v0.0</h1></td>
            </tr>
            <tr id="title">
                <td><b>Service</b></td><td><b>PID</b></td><td><b>Status</b></td><td><b>Aksi</b></td><td></td>
            </tr>
            <tr class="content">
                <td>Apache</td><td>$( pgrep -o ^httpd$ )</td><td><span class="success">Berjalan</span></td><td><button class="disabled" disabled="disabled">Hentikan</button></td><td class="text_right"><a href="/server-status">Server Status &raquo;</a></td>
            </tr>
            <tr class="content">
                <td>MySQL</td><td id="mysql_pid">$( pgrep -o ^mysqld$ )</td><td id="mysql_status">$mysql_status</td><td><button id="bs">$bs</button></td><td class="text_right" id="pma">$pma</td>
            </tr>
            <tr class="content">
                <td colspan="5"><div id="log">$( log_read )</div></td>
            </tr>
            <tr id="footer">
                <td colspan="2"><a href="#" id="log_clear">Bersihkan Log</a></td><td class="text_right" id="copyright" colspan="3">&copy; <a href="https://github.com/gnulinuxid/">GNULinuxID</a> 2020</td>
            </tr>
        </table>
        <div id="qs" style="display: none;">$qs</div>
        <script>
        function doRequest(source) {
            var mysql_status = document.getElementById("mysql_status"),
            qs               = document.getElementById("qs"),
            mysql_pid        = document.getElementById("mysql_pid"),
            log              = document.getElementById("log"),
            pma              = document.getElementById("pma");
            source.innerHTML = "Memuat";
            xhr = new XMLHttpRequest();
            xhr.open("GET", "/alphp/?" + qs.innerHTML, true);
            xhr.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 200 && this.responseText) {
                    var rs = xhr.responseText.split(/\\r?\\n/);
                    mysql_status.innerHTML = rs[0];
                    qs.innerHTML           = rs[1];
                    source.innerHTML       = rs[2];
                    mysql_pid.innerHTML    = rs[3];
                    log.innerHTML          = rs[4];
                    log.scrollTop          = log.scrollHeight - log.clientHeight;
                    if (rs[3]) {
                        pma.innerHTML = '<a href="/phpmyadmin">phpMyAdmin &raquo;</a>';
                    } else {
                        pma.innerHTML = '<span class="disabled">phpMyAdmin &raquo;</span>';
                    }
                }
            }
            xhr.send();
        }
        var bs = document.getElementById("bs");
        bs.onclick = function() {
            doRequest(this);
        }
        var log_clear = document.getElementById("log_clear");
        log_clear.onclick = function() {
            if (confirm("Log akan dibersihkan. Yakin?")) {
                xhr = new XMLHttpRequest();
                xhr.open("GET", "/alphp/?log-clear", true);
                xhr.onreadystatechange = function() {
                    if (this.readyState == 4 && this.status == 200 && this.responseText && this.responseText == 1) {
                        document.getElementById("log").innerHTML = "";
                    }
                }
                xhr.send();
            }
        }
        </script>
    </body>
</html>
EOL
