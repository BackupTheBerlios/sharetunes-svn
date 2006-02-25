# vim:noet

clean:
	find -name '*~' -or -name '*.pyc' | xargs rm -f
	rm -f config tracks_table musicpath

dist: clean
	cd .. && rm -f sharetunes.zip && zip -r sharetunes.zip sharetunes
	ls -l ../sharetunes.zip

publish:
	#@@ obsolete
	scp ../sharetunes.zip brendano@elaine.stanford.edu:~/WWW
