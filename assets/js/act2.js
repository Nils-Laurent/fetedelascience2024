var video = document.getElementById('spectro');
var video_src = document.getElementById('spectro_src');
var titre_spec = document.getElementById('spectro_title');

function play_fn (key) {
    video.pause();
    video.currentTime = 0;
    video.load();
    video.play();
}

var data = {
    'wolf': {"file": 'wolf.mp4', 'cat': 'animals', 'text': 'Loup'},
    'dolphin': {"file": 'dolphin.mp4', 'cat': 'animals', 'text': 'Dauphin (x0.5)'},
    'bell': {"file": 'bell.mp4', 'cat': 'music', 'text': 'Cloche'},
    'guitar': {"file": 'guitar.mp4', 'cat': 'music', 'text': 'Guitare'},
};

for (var key in data) {
    el_a = document.createElement("a");
    el_a.className = "dropdown-item";
    el_a.href = "#";
    el_a.id = key;
    el_a.innerText = data[key]['text']
    el_a.onclick = click_fn;

    el_li = document.createElement("li");
    el_li.appendChild(el_a);
    cat = data[key]['cat'];
    cat_ul = document.getElementById(cat);
    cat_ul.appendChild(el_li);
}

function select_spectro(key) {
    console.log(key);
    video_src.src = "./assets/video/" + data[key]['file'];
    titre_spec.innerText = data[key]['text'];
}

function click_fn() {
    select_spectro(this.id);
    play_fn();
}

document.getElementById('play_btn').onclick = play_fn;
select_spectro('wolf');
video.load();
