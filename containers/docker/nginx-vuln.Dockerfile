FROM ubuntu:20.04

WORKDIR /tmp

RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y build-essential libpcre3 libpcre3-dev zlib1g zlib1g-dev libssl-dev libgd-dev libxml2 libxml2-dev uuid-dev wget libcap2-bin

RUN wget http://nginx.org/download/nginx-1.25.3.tar.gz -O nginx.tar.gz && \
    mkdir /tmp/nginx && \
    tar -xzvf nginx.tar.gz -C /tmp/nginx --strip-components=1

WORKDIR /tmp/nginx
RUN ./configure \
        --user=nginx \
        --with-debug \
        --group=nginx \
        --prefix=/usr/share/nginx \
        --sbin-path=/usr/sbin/nginx \
        --conf-path=/etc/nginx/nginx.conf \
        --pid-path=/run/nginx.pid \
        --lock-path=/run/lock/subsys/nginx \
        --error-log-path=/var/log/nginx/error.log \
        --http-log-path=/var/log/nginx/access.log \
        --with-http_gzip_static_module \
        --with-http_stub_status_module \
        --with-http_ssl_module \
        --with-pcre \
        --with-http_image_filter_module \
        --with-file-aio \
        --with-http_dav_module \
        --with-http_flv_module \
        --with-http_mp4_module \
        --with-http_gunzip_module && \
    sed -i "$(wc -l < src/core/ngx_config.h)i\\#define SSL_OP_NO_ANTI_REPLAY 1\\" src/core/ngx_config.h && \
    make && \
    make install

WORKDIR /tmp

RUN adduser -c "Nginx user" nginx && \
    setcap cap_net_bind_service=ep /usr/sbin/nginx
RUN touch /run/nginx.pid
RUN chown -R nginx:nginx /etc/nginx /etc/nginx/nginx.conf /var/log/nginx /usr/share/nginx /run/nginx.pid /var
RUN ln -sf /etc/nginx/conf.d/nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
EXPOSE 443

#USER nginx
CMD ["/usr/sbin/nginx", "-g", "daemon off;"]