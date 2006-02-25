import com.macromedia.javascript.JavaScriptProxy;
var proxy:JavaScriptProxy = new JavaScriptProxy(_root.lcId, this);

var a = new MusicPlayer()

function play(url) {
    a.loadMusic(url, true)
    a.playMusic()
}

function stop() {
    a.stopMusic()
}
	
trackurl = "http://localhost:8080/musicroot/Arturo%20Sandoval/Hot%20House/01%20Funky%20Cha%20Cha.mp3"

a.stopMusic()
a.setMusicVolume(100)
a.onMusicEnd = function(){ proxy.call('onTrackEnd') }

