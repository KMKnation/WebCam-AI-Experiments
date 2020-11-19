var video, ctx;
var canvas;


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

    var video_config = true;
    if (data.camera == 'front') {
        video_config = {
            facingMode: { exact: "user" }
        }
    } else if (data.camera == 'rear') {
        video_config = {
            facingMode: { exact: "environment" }
        }
    }

    // var appversion = navigator.appVersion;

    var appVersionElem = document.getElementById('app_version');
    appVersionElem.textContent = "DEVICE INFO | " + navigator.appVersion;

    // startButton.disabled = true;
    navigator.mediaDevices
        .getUserMedia({
            audio: {
                mandatory: {
                    echoCancellation: true,
                    googAutoGainControl: true,
                    googHighpassFilter: true,
                    googNoiseSuppression: true
                }
            },
            video: video_config
        })
        .then(gotStream)
        .catch(function (e) {
            console.log(e);
            // alert('getUserMedia() error: ', e);
            alert(data.camera + " <- camera config not working");
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

}

function drawStuff() {
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

    ctx.restore();
}
