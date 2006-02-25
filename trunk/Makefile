# vim:noet

clean:
	find -name '*~' -or -name '*.pyc' | xargs rm -f
	rm -f config tracks_table musicpath

dist: clean
	source admin.sh && makezip

publish:
	source admin.sh && publish
	echo "next step is http://developer.berlios.de/project/admin/qrs.php?package_id=&group_id=6194"
