ps_data_1 = """CONTAINER ID        IMAGE                                      COMMAND                  CREATED             STATUS              PORTS                                      NAMES
1a31fcaccf59        badactorservices_bad-actor-services        "/bin/sh -c 'gunicor…"   4 days ago          Up 4 days           80/tcp                                     badactorservices_bad-actor-services_1
d55ab151ce26        badactorservices_bad-actor-services-data   "tail -f /dev/null"      4 days ago          Up 4 days                                                      badactorservices_bad-actor-services-data_1
d4129f2a0d3b        jwilder/nginx-proxy                        "/app/docker-entrypo…"   4 days ago          Up 4 days           0.0.0.0:80->80/tcp, 0.0.0.0:443->443/tcp   nginx-proxy
42df45bdc8b3        postgres:alpine                            "docker-entrypoint.s…"   5 months ago        Up 3 weeks          10.138.44.203:5432->5432/tcp               some-postgres
23a8d9762781        danielguerra/alpine-sshd                   "docker-entrypoint.s…"   6 months ago        Up 4 months         0.0.0.0:4848->22/tcp                       alpine-sshd"""
