# vim:noet

clean:
	find -name '*~' -or -name '*.pyc' | xargs rm -f
	rm -f config tracks_table musicpath

dist: clean
	source admin.sh && makezip

publish:
	source admin.sh && publish
