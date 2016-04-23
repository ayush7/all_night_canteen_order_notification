#!/bin/bash
uwsgi --static-map /bootstrap=template/bootstrap --ini conf.ini --logto /tmp/serv_log 
