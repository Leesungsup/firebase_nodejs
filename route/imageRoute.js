// requiring dependencies
const express = require('express');

// express router app
const router = express.Router();

// multer to upload image
const multer = require('multer');


// configuring multer file limits and destination
var upload = multer(
    {
        limits: {
            fieldNameSize: 999999999,
            fieldSize: 999999999
        },
        dest: 'uploads/'
    }
);

// requiring imageController for router
const imageController = require('../controller/imageController');

// defining routes
router.post('/image', upload.any(), imageController.uploadImage);

//console.log(`지름이 4인 원의 둘레: ${imageController.resultstring}`);

module.exports = router;