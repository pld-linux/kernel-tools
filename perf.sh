#!/bin/sh

if [ -x /usr/bin/perf_gtk -a -n "$DISPLAY" ]; then
	# prefer GTK version under X11
	exec /usr/bin/perf_gtk "$@"
fi
if [ -x /usr/bin/perf_slang ]; then
	# use text version if perf_gtk or $DISPLAY is not available
	exec /usr/bin/perf_slang "$@"
fi
if [ -x /usr/bin/perf_gtk ]; then
	# fall-back to perf_gtk if no perf_slang (it can work in a terminal
	# too)
	exec /usr/bin/perf_gtk "$@"
fi

echo >&2 "You need 'kernel-tools-perf-gtk' or 'kernel-tools-perf-slang' package installed!"
exit 1
