#! /usr/bin/python

from boto import ec2
import boto.utils
import argparse
import time


def parsed_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--instance_id",
                        help="The instance id where the volume is attached. Default: current instance id",
                        default=boto.utils.get_instance_metadata()['instance-id'])
    parser.add_argument("-d", "--destination_instance_id",
                        help="The instance id where you want to attach the snapshot. Default: current instance id",
                        default=boto.utils.get_instance_metadata()['instance-id'])
    parser.add_argument('-v', "--volume",
                        help="The volume you want to snapshot. Default: /dev/sda1",
                        default='/dev/sda1')
    parser.add_argument('-n', "--new_volume",
                        help="The new volume you want to create. Default: /dev/sdz",
                        default='/dev/sdz')
    parser.add_argument('-r', "--region",
                        help="The region you're in. Default: eu-west-1",
                        default='eu-west-1')
    parser.add_argument('-t', "--tag",
                        help="The tag you'd like to apply to the snapshot. Default: copy-volume",
                        default='copy-volume')
    return parser.parse_args()


def main():
    args = parsed_args()
    conn = ec2.connect_to_region(args.region)

    reservations = conn.get_all_instances(instance_ids=[args.destination_instance_id])
    target_instance = reservations[0].instances[0]
    az = target_instance.placement

    vols = conn.get_all_volumes(filters={'attachment.instance-id': args.instance_id})

    matches = [x for x in vols if x.attach_data.device == args.volume]

    if len(matches) == 1:
        code_volume = matches[0]
    else:
        raise Exception('Volume %s was not found!' % args.volume)

    print "Volume %s found! Snapshotting with tag %s..." % (args.volume, args.tag)

    snap = code_volume.create_snapshot(snapshot_description(code_volume, args.instance_id))
    snap.add_tag('Name', args.tag)

    snapshots = conn.get_all_snapshots(owner='self', snapshot_ids=[snap.id])
    if len(snapshots) == 1:
        snapshot = snapshots[0]
    else:
        raise Exception('Snapshot %s not found' % snap.id)

    while snap.status != 'completed':
        snap.update()
        print "Snapshot Status: %s" % snap.status
        time.sleep(5)
        if snap.status == 'completed':
            print "Snapshot %s is completed." % snap.id
            break

    print "Creating volume from snapshot %s" % snap.id

    new_volume = conn.create_volume(snap.volume_size, az, snapshot=snapshot)

    while new_volume.status != 'available':
        new_volume.update()
        print "Volume Status: %s" % new_volume.status
        time.sleep(5)
        if new_volume.status == 'completed':
            print "Volume %s is reay to use." % new_volume.id
            break

    print "Attaching volume %s to %s" % (new_volume.id, args.destination_instance_id)

    new_volume.attach(args.destination_instance_id, args.new_volume)

    print "Removing snapshot %s" % snap.id

    snap.delete()


def snapshot_description(volume, instance_id):
    return "Deployment snapshot of volume %s on instance %s." % (volume.id, instance_id)


if __name__ == '__main__':
    main()
