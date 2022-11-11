ECHO = /usr/bin/echo

define fancy
	@$(ECHO) -e "\x1b[1m"
	@$(ECHO) "##########################"
	@$(ECHO) "##"
	@$(ECHO) "## $1"
	@$(ECHO) "##"
	@$(ECHO) "##########################"
	@$(ECHO) -e "\x1b[0m"
endef

all: compile upload
	$(call fancy,Done!)

.SILENT:
.PHONY:
compile:
	$(call fancy,Compiling...)
	arduino-cli compile --fqbn arduino:avr:mega . --verbose

.ONESHELL:
.SILENT:
.PHONY:
upload:
	$(call fancy,Uploading...)

	while [ ! -e /dev/ttyACM0 ]; do
		$(ECHO) -e '\x1b[93mPlease plug in your board.\x1b[0m'
		sleep 2
	done

	arduino-cli upload --fqbn arduino:avr:mega . --port /dev/ttyACM0 --verbose
