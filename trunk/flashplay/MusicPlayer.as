class MusicPlayer extends MovieClip
{
    
    //interface
    var onMusicLoaded:Function;
    var onMusicEnd:Function;
    
    private var _main_sound:Sound;
    private var _sound_container_mc:MovieClip;//0;

    //constructor
    function MusicPlayer()
    {
        trace("###MusicPlayer##")
    }

    //public methods
    
    //loads a mp3 sound, call onMusicLoaded(success) when finish the download or when an error occurs
    function loadMusic(p_music_url:String,p_buffer:Boolean)
    {
        _main_sound.onLoad = function(success:Boolean) {
          if (success) {
            //download finished
            this["owner"].onMusicLoaded(true);
          } else {
            if(this.getBytesLoaded()>4){
                //part of the mp3 is cached, do nothing
                /*
                if(this.getBytesLoaded()==this.getBytesTotal()){
                    this["owner"].onMusicLoaded(true);
                }else{
                    //doesnt call onMusicLoaded cause the downloading is in progress
                }
                */
            }else{
                //ERROR download failed
                this["owner"].onMusicLoaded(false);
            }
          }
        };
        this.createEmptyMovieClip("_sound_container_mc",0)
        _main_sound = new Sound(_sound_container_mc)
        _main_sound["owner"] = this;
        _main_sound.onSoundComplete = function(success:Boolean) {
            //sound complete
            //[Flash Player BUG] - <workaround> manually resets the position to 0
            this.start(0)
            this.stop()
            //</workaround>
            this["owner"].onMusicEnd()
        }
        _main_sound.loadSound(p_music_url,p_buffer);        
    }

    //start playing the music, calls onMusicEnd when the music reaches the end
    function playMusic()
    {
        _main_sound.start()
    }

    //stop the music and return to position 0
    function stopMusic()
    {
        //[Flash Player BUG] - <workaround> manually resets the position to 0
        _main_sound.stop()
        _main_sound.start(0)
        _main_sound.stop()
        //</workaround>
        delete _main_sound
        _sound_container_mc.removeMovieClip();
    }

    //pause the music
    function pauseMusic()
    {
        //TODO
    }

    //volume 0-100
    function setMusicVolume(p_volume)
    {
        trace("setMusicVolume "+p_volume)
        _main_sound.setVolume(p_volume)
    }
    function get bytes_loaded()
    {
        return _main_sound.getBytesLoaded()
    }
    function get bytes_total(){
        return _main_sound.getBytesTotal()
    }
    function get music_position()
    {
        return _main_sound.position;
    }
    function get music_duration()
    {
        return _main_sound.duration;
    }
    
    function alert(p_msg){
        trace(p_msg)    
    }
    
}
