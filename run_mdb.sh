#!/bin/bash
echo "mongodb starting"
export PATH="/mongodb/mongodb-5.0.8/bin:$PATH"
echo "mongodb bin add path"
/mongodb/mongodb-5.0.8/bin/mongod --dbpath=/mongodb/data --logpath=/mongodb/logs --logappend --port=27017