#!/bin/bash

set -o xtrace
set -o errexit

# Enable unbuffered output for Ansible in Jenkins.
export PYTHONUNBUFFERED=1


function test_openstack_logged {
    . /etc/kolla/admin-openrc.sh

    openstack --debug compute service list
    openstack --debug network agent list

    echo "TESTING: Server creation"
    openstack server create --wait --image cirros --flavor m1.tiny --key-name mykey --network demo-net kolla_boot_test
    openstack --debug server list
    # If the status is not ACTIVE, print info and exit 1
    if [[ $(openstack server show kolla_boot_test -f value -c status) != "ACTIVE" ]]; then
        echo "FAILED: Instance is not active"
        openstack --debug server show kolla_boot_test
        return 1
    fi
    echo "SUCCESS: Server creation"

    if echo $ACTION | grep -q "ceph"; then
        echo "TESTING: Cinder volume attachment"
        openstack volume create --size 2 test_volume
        openstack server add volume kolla_boot_test test_volume --device /dev/vdb
        openstack server remove volume kolla_boot_test test_volume
        echo "SUCCESS: Cinder volume attachment"
    fi

    echo "TESTING: Server deletion"
    openstack server delete --wait kolla_boot_test
    echo "SUCCESS: Server deletion"

    if echo $ACTION | grep -q "zun"; then
        echo "TESTING: Zun"
        openstack appcontainer service list
        openstack appcontainer host list
        openstack subnet set --no-dhcp demo-subnet
        sudo docker pull alpine
        sudo docker save alpine | openstack image create alpine --public --container-format docker --disk-format raw
        openstack appcontainer run --name test alpine sleep 1000
        attempt=1
        while [[ $(openstack appcontainer show test -f value -c status) != "Running" ]]; do
            echo "Container not running yet"
            attempt=$((attempt+1))
            if [[ $attempt -eq 10 ]]; then
                echo "Container failed to start"
                openstack appcontainer show test
                return 1
            fi
            sleep 10
        done
        openstack appcontainer list
        openstack appcontainer delete --force --stop test
        echo "SUCCESS: Zun"
    fi
}

function test_openstack {
    echo "Testing OpenStack"
    test_openstack_logged > /tmp/logs/ansible/test-openstack 2>&1
    result=$?
    if [[ $result != 0 ]]; then
        echo "Testing OpenStack failed. See ansible/test-openstack for details"
    else
        echo "Successfully tested OpenStack. See ansible/test-openstack for details"
    fi
    return $result
}

test_openstack
