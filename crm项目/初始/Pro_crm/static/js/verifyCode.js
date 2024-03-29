var show_num = [];
var timeout_flag = false;
var cache = {};
$(function () {
    draw(show_num);
    $("#login-verify-code-canvas").on('click', function () {
        draw(show_num);
    });
});

function draw(show_num) {
    var canvas_width = $('#login-verify-code-canvas').width(), canvas_height = $('#login-verify-code-canvas').height(),
        canvas = document.getElementById("login-verify-code-canvas"), context = canvas.getContext("2d"),
        sCode = "A,B,C,E,F,G,H,J,K,L,M,N,P,Q,R,S,T,W,X,Y,Z,1,2,3,4,5,6,7,8,9,0", aCode = sCode.split(","),
        aLength = aCode.length;
    canvas.width = canvas_width;
    canvas.height = canvas_height;
    for (var i = 0; i <= 3; i++) {
        var j = Math.floor(Math.random() * aLength), deg = Math.random() * 30 * Math.PI / 180,
            txt = Math.floor(Math.random() * 2) == 1 ? aCode[j] : aCode[j].toLowerCase(), x = 10 + i * 20,
            y = 20 + Math.random() * 8;
        show_num[i] = txt.toLowerCase();
        context.font = "bold 23px 微软雅黑";
        context.translate(x, y);
        context.rotate(deg);
        context.fillStyle = randomColor();
        context.fillText(txt, 0, 0);
        context.rotate(-deg);
        context.translate(-x, -y);
    }
    for (var i = 0; i <= 5; i++) {
        context.strokeStyle = randomColor();
        context.beginPath();
        context.moveTo(Math.random() * canvas_width, Math.random() * canvas_height);
        context.lineTo(Math.random() * canvas_width, Math.random() * canvas_height);
        context.stroke();
    }
    for (var i = 0; i <= 30; i++) {
        context.strokeStyle = randomColor();
        context.beginPath();
        var x = Math.random() * canvas_width;
        var y = Math.random() * canvas_height;
        context.moveTo(x, y);
        context.lineTo(x + 1, y + 1);
        context.stroke();
    }
    timeout_flag = false;
    clearTimeout(cache["Timeout"]);
    var t = setTimeout(function () {
        timeout_flag = true;
    }, 60000);
    cache["Timeout"] = t;
}

function randomColor() {
    var r = Math.floor(Math.random() * 256);
    var g = Math.floor(Math.random() * 256);
    var b = Math.floor(Math.random() * 256);
    return "rgb(" + r + "," + g + "," + b + ")";
}