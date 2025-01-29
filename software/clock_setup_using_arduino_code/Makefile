PRJ_DIR = $(realpath .)

# ============================================================================= ARGS
PATH_SKETCH	:= $(PRJ_DIR)/clock_setup/clock_setup.ino

PORT		:= /dev/ttyACM0

FILE_CONFIG	:= arduino-cli.yaml
BOARD_CORE	:= WCH:ch32v
BOARD_LIST	:= WCH
FQBN		:= WCH:ch32v:CH32V00x_EVT

# ============================================================================= TARGETS

# setup and install arduino CLI
setup-arduino-cli:
	@ echo " "
	[ -d ~/arduino_cli ] || mkdir -p ~/arduino_cli; \
		cd ~/arduino_cli; \
		curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh; \
		echo "========== Verifying installation..."; \
		source $(HOME)/.bashrc; \
		which arduino-cli; \
		arduino-cli version

# setup board files for CH32V003 on arudino
setup-board-files:
	@ echo " "
	@ echo "==================== Creating board config file"
	arduino-cli config init && \
	@ echo "==================== Copy file to config folder"; \
	[ -d $(HOME)/.arduino15 ] || mkdir -p $(HOME)/.arduino15; \
	cp -rv ./$(FILE_CONFIG) $(HOME)/.arduino15/$(FILE_CONFIG) && \
	@ echo "==================== Update the core index"; \
	arduino-cli core update-index && \
	@ echo "==================== Search for WCH boards"; \
	arduino-cli core search wch && \
	@ echo "==================== Install the core"; \
	arduino-cli core install $(BOARD_CORE) && \
	@ echo "==================== Verify installation"; \
	arduino-cli core list && \
	@ echo "==================== List all WCH boards"; \
	arduino-cli board listall $(BOARD_LIST)

# show all connected boards/chips via USB
list-boards:
	@ echo " "
	@ echo "==================== List connected boards"; \
	arduino-cli board list && \
	@ echo "==================== List Ch32V boards available"; \
	arduino-cli board listall | grep CH32

# compile the arduino sketch for the chip
compile:
	@ echo " "
	@ echo "==================== Compiling sketch"
	arduino-cli compile --fqbn $(FQBN) $(PATH_SKETCH)

# upload the sketch to the board
upload:
	@ echo " "
	@ echo "==================== Uploading sketch"
	arduino-cli upload $(PATH_SKETCH) -p $(PORT) --fqbn $(FQBN)

