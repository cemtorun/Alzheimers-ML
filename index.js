var AWS = require('aws-sdk')
var s3 = new AWS.S3();

var params = {
    Bucket: 'princetonhackbob',
    Key: 'AlexaTest3.json'
};

var fileLoaded = false;
var fileData = null;

exports.handler = (event, context, callback) => {

    if(!fileLoaded){
        s3.getObject(params, function (err, data) {
            if (err) console.log(err, err.stack);
            else {
                fileLoaded = true;
                fileData = data;
                parseJSON(event, context, callback)
            }
        });
    } else {
        parseJSON(event, context, callback)
    }
};

function parseJSON(event, context, callback){
    //Do the actual work here
    // console.log(fileData.Body.toString())
    const spawnSync = require("child_process").spawnSync;
    const pythonProcess = spawnSync('python',["./main.py", fileData.Body.toString()]);
    var checkValue;
    // pythonProcess.stdout.on('data', function(data) {
    //     // res.send(data.toString());
    //     console.log(data.toString())
    // } )
    // pythonProcess.stdout.on('data', (data) => {
    //     console.log("hrloooo")
    //     checkValue = data.toString();
    //     console.log(checkValue)
    //     callback(null, {
    //         'statusCode': 200,
    //         'headers': {'Content-Type': 'application/json'},
    //         // 'body': fileData.Body.toString()
    //         'body': checkValue
    //     }) //Then end

    // });
    console.log(pythonProcess)
    console.log(pythonProcess.stderr.toString())
    console.log(pythonProcess.stdout.toString())
    return callback(null,  {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        // 'body': fileData.Body.toString()
        'body': true
    })

}
