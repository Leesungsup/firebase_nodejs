// multer to upload image
const multer = require('multer');
const fs = require('fs');
const spawn = require('child_process').spawn;
const database = require('../config');
const firebase = require("firebase-admin");
const { PythonShell } = require("python-shell");
var resultstring;
var uploadImage1 = (req,res)=>{
    let tmp_path = req.files[0].path;
        console.log('req path'+req.files[0].originalname);
        let target_path = 'uploads/' + req.files[0].originalname;
        console.log('req originalname'+req.files[0].originalname);
        var src = fs.createReadStream(tmp_path);
        var dest = fs.createWriteStream(target_path);
        src.pipe(dest);
        
        // predict.py 파일을 실행 시킴
        // PythonShell.run("model.py", options, function (err, results) {
        //     if (err) throw err;
        //     // 전달 받은 결과값을 찍어봄
        //     console.log("dga"); 
        //     // res.send(results);
        //     console.log(typeof(results));
        //     console.log(Object.keys(results))
        //     console.log(results[0].dd);
        //     // console.log(results[1]);
        //     //let name = req.files[0].originalname;
        //     let str= req.files[0].originalname.replace('/','');
        //     str=req.files[0].originalname.replace('.','');
        //     database.ref("approved_users/").child(str).update({name : results[0].dd.toString()}, function(error) {
        //         if(error)
        //             console.error(error)
        //         else
        //             console.log("success save !!");
        //     });
        // });
        




        // PythonShell.run("model1.py", options, function (err, results) {
        //     if (err) throw err;
        //     // 전달 받은 결과값을 찍어봄
        //     console.log("dga"); 
        //     // res.send(results);
        //     console.log(typeof(results));
        //     console.log(Object.keys(results))
        //     console.log(results[0].dd);
        //     // console.log(results[1]);
        //     //let name = req.files[0].originalname;
        //     let str= req.files[0].originalname.replace('/','');
        //     str=req.files[0].originalname.replace('.','');
        //     database.ref("approved_users/").child(str).update({name : results[0].dd.toString()}, function(error) {
        //         if(error)
        //             console.error(error)
        //         else
        //             console.log("success save !!");
        //     });
        // });
        var exec = require('child_process').exec;
        exec('py -3.10 model1.py --input_images '+req.files[0].originalname, function(error, stdout, stderr) {
            console.log('stdout: ' + stdout);
            if (error !== null) {
                console.log('exec error: ' + error);
            }
            else{
                console.log('pythonshell');
                var options = {
                    mode: "json", // 파이썬 응답을 어떤 형식으로 받을 것인가
                    pythonPath: "",
                    pythonOptions: ["-u"],
                    scriptPath: "",
                    args: ["--input_images", "./uploads/"+req.files[0].originalname,"--depth_model_architecture", "./Food_volume_estimation/depth_architecture.json","--depth_model_weights","./Food_volume_estimation/depth_weights.h5","--segmentation_weights", "./Food_volume_estimation/segmentation_weights.h5","--food",stdout.replace(/\n|\r|\s*/g, "")]
                    // args: [req.files[0].originalname],
                    // args: ['카레유', '20',req.files[0].originalname], // 파이썬 코드로 전달할 arguments
                };
                console.log(options); 
                PythonShell.run("./Food_volume_estimation/volume_estimator.py", options, function (err, results) {
                    if (err) throw err;
                    // 전달 받은 결과값을 찍어봄
                    console.log("dga"); 
                    // res.send(results);
                    console.log(typeof(results));
                    console.log(Object.keys(results))
                    console.log(results[0].dd);
                    // console.log(results[1]);
                    //let name = req.files[0].originalname;
                    let str= req.files[0].originalname.replace('/','');
                    str=req.files[0].originalname.replace('.','');
                    database.ref("calorie/").child(str).update({name : results[0].dd.toString()}, function(error) {
                        if(error)
                            console.error(error)
                        else
                            console.log("success save !!");
                    });
                });
            }
        });

        // PythonShell.run("./Food_volume_estimation/volume_estimator.py", options, function (err, results) {
        //     if (err) throw err;
        //     // 전달 받은 결과값을 찍어봄
        //     console.log("dga"); 
        //     // res.send(results);
        //     console.log(typeof(results));
        //     console.log(Object.keys(results))
        //     console.log(results[0].dd);
        //     // console.log(results[1]);
        //     //let name = req.files[0].originalname;
        //     let str= req.files[0].originalname.replace('/','');
        //     str=req.files[0].originalname.replace('.','');
        //     database.ref("approved_users/").child(str).update({name : results[0].dd.toString()}, function(error) {
        //         if(error)
        //             console.error(error)
        //         else
        //             console.log("success save !!");
        //     });
        // });
        
        //const pyProg = spawn('python', ['./../pypy.py']);
        // const result_02 = spawn('python', ['model.py',req.files[0].originalname]);
        // const result_02 = spawn('python', ['function_argv.py', '카레유', '20',req.files[0].originalname]);
        // result_02.stdout.on('data', (result)=>{
        //     // Object.keys(result).forEach(key=>{
        //     //     console.log(key);
        //     //     console.log(result[key].toString);
        //     // })
        //     //console.log(Array.isArray(result));
        //     console.log(typeof(result));
        //     console.log(result.toString());
        //     //let name = req.files[0].originalname;
        //     let str= req.files[0].originalname.replace('/','');
        //     str=req.files[0].originalname.replace('.','');
        //     database.ref("approved_users/").child(str).update({name : result.toString()}, function(error) {
        //         if(error)
        //             console.error(error)
        //         else
        //             console.log("success save !!");
        //     });
        // });
        src.on('end', function() { 
            res.sendStatus(200); 
        });
        src.on('error', function(err) { 
            res.sendStatus(500); 
        });
}
module.exports.uploadImage=uploadImage1;
// module.exports = {
//     uploadImage: (req, res) => {
//         let tmp_path = req.files[0].path;
//         console.log('req path'+req.files[0].originalname);
//         let target_path = 'uploads/' + req.files[0].originalname;
//         console.log('req originalname'+req.files[0].originalname);
//         var src = fs.createReadStream(tmp_path);
//         var dest = fs.createWriteStream(target_path);
//         src.pipe(dest);
//         const { spawn } = require('child_process');
//         //const pyProg = spawn('python', ['./../pypy.py']);
//         const result_02 = spawn('python', ['function_argv.py', '카레유', '20',req.files[0].originalname]);
//         result_02.stdout.on('data', (result)=>{
//             Object.keys(result).forEach(key=>{
//                 console.log(key);
//                 console.log(result[key].toString);
//             })
//             console.log(Array.isArray(result));
//             console.log(typeof(result));
//             console.log(result.toString());
//         });
//         src.on('end', function() { res.sendStatus(200); });
//         src.on('error', function(err) { res.sendStatus(500); });
//     }
// }