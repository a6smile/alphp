export APACHE_CONF_CUSTOM=/etc/apache2/conf.d/custom.conf
export APACHE_LOG_DIR=/var/log/apache2
export APACHE_LOG_ACCESS="$APACHE_LOG_DIR/access.log"
export APACHE_LOG_ERROR="$APACHE_LOG_DIR/error.log"
export APACHE_PID_FILE=/run/apache2/httpd.pid

printf "Memulai Apache HTTP Server"
echo "# Jangan mengedit file ini, dibuat oleh .profile" > $APACHE_CONF_CUSTOM
cat <<EOL >> $APACHE_CONF_CUSTOM
DocumentRoot $DOCUMENT_ROOT
Listen $APACHE_PORT
ServerName $HOST:$APACHE_PORT
EOL

pid=$( pgrep -o httpd )
if [ -n "$pid" ]; then
    echo "$pid" > $APACHE_PID_FILE
    echo "httpd (pid $pid) sudah berjalan" > $APACHE_LOG_ERROR
else
    ( httpd -k start > $APACHE_LOG_ERROR 2>&1 & )
fi

while [ "$( stat -c %s $APACHE_LOG_ERROR )" -eq 0 ]; do
    printf "."
    sleep .1
done

trap '. $HOME/.logout; exit' 0

if pidof -s httpd > /dev/null 2>&1; then
    if [ -n "$pid" ]; then
        info="Jika terjadi konflik, coba: kill $pid"
    else
        info=$( echo -e "[\e[1;32mOK\e[0m] Server $HOST telah berhasil dimulai di Port $APACHE_PORT" )
    fi
else
    info=$( echo -e "[\e[1;31mError\e[0m] Terjadi kesalahan!" )
fi

cat <<EOL

         _         _              _____     __  
        | |       | |            | ____|   / /  
   __ _ | | _ __  | |__   _ __   | |__    / /_  
  / _\` || || '_ \ | '_ \ | '_ \  |___ \  | '_ \ 
 | (_| || || |_) || | | || |_) |  ___) |_| (_) |
  \__,_||_|| .__/ |_| |_|| .__/  |____/(_)\___/ 
           | |           | |                    
           |_|           |_|                    
Selamat datang di alphp!
https://github.com/gnulinuxid/alphp
---------------------------------------------------------
$( tail -n5 $APACHE_LOG_ERROR )
$info
---------------------------------------------------------
Ketik "exit" lalu Enter untuk logout.
EOL
