#!/bin/bash

echo "Init Rabbitmq config..."

USER=$RABBITMQ_DEFAULT_USER
VHOSTS=$RABBITMQ_VHOSTS

# Split the vhosts into an array using a comma (,) as the delimiter.
IFS=',' read -ra VHOST_ARRAY <<< "$VHOSTS"

echo ${VHOST_ARRAY}

for vhost in "${VHOST_ARRAY[@]}"
do
    rabbitmqctl add_vhost $vhost
    rabbitmqctl set_permissions -p $vhost $USER ".*" ".*" ".*"
done
