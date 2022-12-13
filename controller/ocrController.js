// multer to upload image
const multer = require('multer');
const fs = require('fs');
const spawn = require('child_process').spawn;
const database = require('../config');
const firebase = require("firebase-admin");
const { PythonShell } = require("python-shell");
const ocrkey = require("../ocrkey");
var resultstring;
var ocrImage1 = (req,res)=>{
    let tmp_path = req.files[0].path;
        console.log('req path'+req.files[0].originalname);
        let target_path = 'uploads/' + req.files[0].originalname;
        console.log('req originalname'+req.files[0].originalname);
        var src = fs.createReadStream(tmp_path);
        var dest = fs.createWriteStream(target_path);
        src.pipe(dest);
        console.log(ocrkey.ocrkey);
        console.log('pythonshell');
        var options = {
            mode: "json", // 파이썬 응답을 어떤 형식으로 받을 것인가
            pythonPath: "",
            pythonOptions: ["-u"],
            scriptPath: "",
            args: ["./uploads/"+req.files[0].originalname,ocrkey.ocrkey]
            // args: [req.files[0].originalname],
            // args: ['카레유', '20',req.files[0].originalname], // 파이썬 코드로 전달할 arguments
        };
        console.log(options); 
        PythonShell.run("./OCR.py", options, function (err, results) {
            if (err) throw err;
            // 전달 받은 결과값을 찍어봄
            console.log("dga"); 
            // res.send(results);
            console.log(typeof(results));
            console.log(Object.keys(results))
            console.log(results[0]);
            console.log(results[0].toString);
            // console.log(results[1]);
            //let name = req.files[0].originalname;
            let str= req.files[0].originalname.replace('/','');
            str=req.files[0].originalname.replace('.','');
            database.ref("OCR/").child(str).update({name : results[0]}, function(error) {
                if(error)
                    console.error(error)
                else
                    console.log("success save !!");
            });
        });

        src.on('end', function() { 
            res.sendStatus(200); 
        });
        src.on('error', function(err) { 
            res.sendStatus(500); 
        });
}
module.exports.ocrImage=ocrImage1;
