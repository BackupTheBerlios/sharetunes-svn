# vim:noet

clean:
	find -name '*~' -or -name '*.pyc' | xargs rm -f
	rm -f config tracks_table musicpath

dist: clean
	cd .. && rm -f sharetunes.zip && zip -r sharetunes.zip sharetunes -x '*.svn*'
	ls -l ../sharetunes.zip

publish:
	#@@ upload to berlios somehow
	scp ../sharetunes.zip brendano@elaine.stanford.edu:~/WWW
