var video, ctx;
var canvas;

var src, dst, gray, cap, faces, classifier


function start() {
    video = document.createElement("video", { autoPlay: true }); // create a video element
    video.setAttribute("playsinline", null);
    video.setAttribute("autoPlay", true);
    video.controls = true;
    video.muted = true;

    canvas = document.getElementById('canvas');
    ctx = canvas.getContext('2d');

    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    ctx.canvas.width = window.innerWidth;
    ctx.canvas.height = window.innerHeight;

    // resize the canvas to fill browser window dynamically
    window.addEventListener('resize', resizeCanvas, false);

    console.log('Requesting local stream');

    // startButton.disabled = true;
    navigator.mediaDevices
        .getUserMedia({
            audio: false,
            video: {
                "width": {
                    "min": "300",
                    "max": "640"
                },
                "height": {
                    "min": "200",
                    "max": "480"
                }
            }
        })
        .then(gotStream)
        .catch(function (e) {
            console.log(e);
            alert('getUserMedia() error: ', e);
        });

}

function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    ctx.canvas.width = window.innerWidth;
    ctx.canvas.height = window.innerHeight;

    console.log('Assigned New Heights');

    /**
     * Your drawings need to be inside this function otherwise they will be reset when 
     * you resize the browser window and the canvas goes will be cleared.
     */
    drawStuff();
}

function gotStream(stream) {
    video.srcObject = stream;
    setTimeout(function () {
        video.play();
    }, 50);
    video.addEventListener('play', function () {
        var $this = this; //cache
        (function loop() {
            drawStuff();

            setTimeout(loop, 1000 / 30); // drawing at 30fps
        })();
    }, 0);


    doImageRecognition();

}

const FPS = 30;

async function processVideo() {
    try {

        let begin = Date.now();
        // start processing.
        cap.read(src);

        let dsize = new cv.Size(src.cols / 2, src.rows / 2);
        cv.resize(src, dst, dsize, fx = 0, fy = 0, interpolation = cv.INTER_LINEAR)

        cv.cvtColor(dst, gray, cv.COLOR_RGBA2GRAY, 0);
        // detect faces.
        await classifier.detectMultiScale(gray, faces, 1.1, 3, 0);


        
        // draw faces.
        // for (let i = 0; i < faces.size(); ++i) {
        //     // let face = faces.get(i);
        //     // faces.get(i).x = face.x * 2;
        //     // faces.get(i).y = face.y * 2;
        //     // faces.get(i).width = face.width * 2;
        //     // faces.get(i).height = face.height * 2;
        // }
        // schedule the next one.
        let delay = 1000 / FPS - (Date.now() - begin);

        setTimeout(processVideo, delay);
    } catch (err) {
        console.log(err);
    }
};

function drawStuff() {
    console.log('draw')
    if (canvas == null)
        return;
    ctx.save();

    ctx.beginPath();
    ctx.rect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = "black";
    ctx.fill();

    var scale = Math.min(
        canvas.width / video.videoWidth,
        canvas.height / video.videoHeight);
    var vidH = video.videoHeight;
    var vidW = video.videoWidth;
    var top = canvas.height / 2 - (vidH / 2) * scale;
    var left = canvas.width / 2 - (vidW / 2) * scale;
    // ctx.drawImage($this, 0, 0);
    ctx.drawImage(video, left, top, vidW * scale, vidH * scale);


    try {
        if (faces != undefined) {

            for (let i = 0; i < faces.size(); ++i) {
                let face = faces.get(i);

                //2 used as downscaled value given in src resize
                face.width = face.width * 2;
                face.height = face.height * 2;
                face.y = face.y * 2;
                face.x = face.x * 2;

                face.width = face.width * scale;
                face.height = face.height * scale;
                face.y = face.y * scale;
                face.x = face.x * scale;
                face.x = face.x + left;
                face.y = face.y + top;

                // cv.rectangle(dst, point1, point2, [255, 0, 0, 255]);
                ctx.beginPath();
                ctx.lineWidth = 4 * scale;
                ctx.strokeStyle = "green";
                ctx.rect(face.x, face.y, face.width, face.height);
                // {x: 176, y: 387, width: 58, height: 58}
                ctx.stroke();
            }
        }
    } catch (e) {
        console.log(e);
    }

    ctx.restore();


}


function doImageRecognition() {



    let utils = new Utils('errorMessage');

    // utils.loadCode('codeSnippet', 'codeEditor');
    // utils.executeCode('codeEditor');


    utils.loadOpenCv(() => {
        let faceCascadeFile = 'haarcascade_frontalface_default.xml';
        utils.createFileFromUrl(faceCascadeFile, faceCascadeFile, () => {
            // startAndStop.removeAttribute('disabled');
            video.height = video.videoHeight;
            video.width = video.videoWidth;

            src = new cv.Mat(video.height, video.width, cv.CV_8UC4); 
            dst = new cv.Mat();
            gray = new cv.Mat();
            cap = new cv.VideoCapture(video);
            faces = new cv.RectVector();
            classifier = new cv.CascadeClassifier();

            // load pre-trained classifiers
            classifier.load('haarcascade_frontalface_default.xml');

            console.log('Classifier loaded');
            processVideo();
        });
    });


}

window.onbeforeunload = function () {
    // clean and stop.
    src.delete();
    dst.delete();
    gray.delete();
    faces.delete();
    classifier.delete();
    return;
}
