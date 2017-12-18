# MARATHON_RAW_BACKUP

This tool has been developed by @rfiestas [github](https://github.com/rfiestas) afford for to do [Marathon](https://github.com/mesosphere/marathon) tasks backup using the Marathon API, testing with [1.4.8](https://github.com/mesosphere/marathon/releases/tag/v1.4.8).

It will create a diferents json for each groups and tasks.

NAME

     marathon_raw_backup -- dump or restore Marathon Tasks

COMMANDS

## Backup

### Using sccript

- ```bash marathon_groups_backup.py --environment lab --url http://marathonur:8080```

### Using docker

- ```bash docker  run -e ENVIRONMENT=lab -e URL=http://marathonurl:8080 -e HOME_PATH=/mnt maauso/marathon-raw-backup```

## Restore backup

### Launch each group one by one.

```bash

curl -s -X POST $MARATHON/v2/groups -H "Content-type: application/json" --data "@groups/services.json"
curl -s -X POST $MARATHON/v2/groups -H "Content-type: application/json" --data "@groups/apps.json"

```

### Real exemple to recover groups

```bash

curl -X PUT -H "Content-Type: application/json"  --data @group.json 'http://marathon:8080/v2/groups?force=true'

```

### Real exemple to recover each app

```bash
for i in `find . -type f -name "*.json"` ; do curl -X POST -H "Content-Type: application/json"  --data @$i 'http://marathon8080/v2/apps/' ; done
```