# Changelog
Here's all notable changes and commits to both the configuration repo and the base ZMK that the config repo builds against. 

Many thanks to all those who have submitted issues and pull requests to make this firmware better!
## Config repo

10/9/2023 - Further documentation refinements, add section on beta testing, document BLE privacy [#241](https://github.com/KinesisCorporation/Adv360-Pro-ZMK/pull/241)

10/9/2023 - Change build actions to fix warnings from shellcheck [#242](https://github.com/KinesisCorporation/Adv360-Pro-ZMK/pull/242)

9/7/2023 - Add a changelog to the documentation, document key positions for combos and improve misc other areas of documentation [#221](https://github.com/KinesisCorporation/Adv360-Pro-ZMK/pull/221) [#222](https://github.com/KinesisCorporation/Adv360-Pro-ZMK/pull/222)

7/28/2023 - Add a section in README explaining how to resolve connectivity issues after updating [#197](https://github.com/KinesisCorporation/Adv360-Pro-ZMK/pull/197)

### 7/6/2023 - V3.0 - Major refactor to board definition to match the upstream PR and comply with ZMK pre-commit requirements, Final changes to key matrix in hope of avoiding any future git conflicts, switch to zephyr Pinctrl API, Update the settings-reset file, switch to the zephyr 3.2 branch of the base ZMK repo, add instructions to resolve the conflicts upon updating (adv360-z3.2)

4/7/2023 - README improvements, adding instructions on flashing, links to the GUI editor and formatting cleanup [#128](https://github.com/KinesisCorporation/Adv360-Pro-ZMK/pull/128)

3/4/2023 - Add extra keys into matrix that point to nowhere, fixes spurious keypress issues when using USB3.1 cables [#114](https://github.com/KinesisCorporation/Adv360-Pro-ZMK/pull/114) [#116](https://github.com/KinesisCorporation/Adv360-Pro-ZMK/pull/116)


2/14/2023 - Disable ZMK logging by default to improve power consumption [#101](https://github.com/KinesisCorporation/Adv360-Pro-ZMK/pull/101)

1/25/2023 - Fix automatic OS detection to build properly when using the local builder on OS-X [#91](https://github.com/KinesisCorporation/Adv360-Pro-ZMK/pull/91)

1/16/2023 - Change formatting of keymap GUI files [#92](https://github.com/KinesisCorporation/Adv360-Pro-ZMK/pull/92)

11/21/2022 - Rewrite README to take into account new makefile structure [#57](https://github.com/KinesisCorporation/Adv360-Pro-ZMK/pull/57)

11/18/2022 - Add SELinux support to the makefile build sequence [#58](https://github.com/KinesisCorporation/Adv360-Pro-ZMK/pull/58)

11/14/2022 - Makefile cleanup to delete docker images on clean and run more seamlessly [#42](https://github.com/KinesisCorporation/Adv360-Pro-ZMK/pull/42)

10/30/2022 - Improve make clean so that it doesn't error when run without build firmware [#36](https://github.com/KinesisCorporation/Adv360-Pro-ZMK/pull/36)

10/26/2022 - Add support for building through podman as opposed to docker [#10](https://github.com/KinesisCorporation/Adv360-Pro-ZMK/pull/10)

10/23/2022 - Update GitHub actions to avoid deprecated actions [#33](https://github.com/KinesisCorporation/Adv360-Pro-ZMK/pull/33)

10/23/2022 - Add a makefile to reuse the docker image every time [#29](https://github.com/KinesisCorporation/Adv360-Pro-ZMK/pull/29)

10/20/2022 - Update settings reset file to fully erase peripheral data from the central

10/12/2022 - Fix local docker build after V2.0 update [#25](https://github.com/KinesisCorporation/Adv360-Pro-ZMK/pull/25)

10/11/2022 - Set manufacturer information over BLE [#28](https://github.com/KinesisCorporation/Adv360-Pro-ZMK/pull/28)

10/9/2022 - Cleanup of keymap [#24](https://github.com/KinesisCorporation/Adv360-Pro-ZMK/pull/)

10/7/2022 - Add USB VID, PID and Manufacturer information to config files

9/26/2022 - Revise local building script to avoid errors after V2.0 update

### 9/17/2022 - V2.0 - Changes to support Zephyr 3 (adv360-z3)

8/9/2022 - Remove extraneous keys from the GUI [#5](https://github.com/KinesisCorporation/Adv360-Pro-ZMK/pull/5)

6/13/2022 - Change default keymap, add default macros

5/23/2022 - Add local building with Docker, Add a README [#4](https://github.com/KinesisCorporation/Adv360-Pro-ZMK/pull/4)

5/6/2022 - Change LFCLK accuracy for improved reliability [#2](https://github.com/KinesisCorporation/Adv360-Pro-ZMK/pull/2)

### 3/3/2022 - V1.0 - Initial config repo release [#1](https://github.com/KinesisCorporation/Adv360-Pro-ZMK/pull/1) (adv360-beta)

3/1/2022 - Initial publication of licence

## Base ZMK

There have beeen 3 mainline branches of ZMK used for the 360 Pro so far. Beta branches are not changelogged as they are subject to frequent changes and tweaks.

| Branch | Date From | Date To | Config Branch |
| -------- | ------- |-------|-----|
| [adv360-beta](https://github.com/ReFil/zmk/tree/adv360-beta)   | 3/1/2022 | 9/17/2022 | V1.0 (since deleted) |
| [adv360-z3](https://github.com/ReFil/zmk/tree/adv360-z3) | 9/17/2022 | 7/6/2023 | [V2.0](https://github.com/KinesisCorporation/Adv360-Pro-ZMK/tree/V2.0) |
| [adv360-z3.2](https://github.com/ReFil/zmk/tree/adv360-z3.2) | 7/6/2023 | To date | [V3.0](https://github.com/KinesisCorporation/Adv360-Pro-ZMK/tree/V3.0) |

### adv360-z3.2

7/31/2023 - Fix broken CI builds [#6](https://github.com/ReFil/zmk/pull/6)

5/30/2023 - Update RGB indicators code to match latest changes from pull requests

5/30/2023 - Merge latest HID indicators pull request alongside dependencies [#999](https://github.com/zmkfirmware/zmk/pull/999) [#1803](https://github.com/zmkfirmware/zmk/pull/1803)

5/30/2023 - Disable BLE battery reporting due to unreliability

5/30/2023 - Various fixes to allow compilation on zephyr 3.2

5/29/2023 - Merge latest upstream ZMK (Commit b276a3b)

### adv360-z3

3/27/2023 - Fix power on behaviour for RGB lighting

2/24/2023 - Fix indication leds for BLE profile 5

1/12/2023 - Merge latest upstream ZMK (Commit a82a0ec)

1/12/2023 - Fix pre-commit formatting

1/12/2023 - Fix a compile time warning by defining struct in header [#4](https://github.com/ReFil/zmk/pull/4)

11/25/2022 - Add extra BLE characteristic to fix HID light reporting on MacOS

10/19/2022 - Add BLE whitelist scanning to improve performance in environments with many BLE devices

10/19/2022 - Merge latest upstream ZMK (Commit c9eb631)

10/19/2022 - Fix initial power on lighting

10/2/2022 - Add ability to scale RGB and backlight brightness to improve battery life

9/13/2022 - Add custom lighting functionality on top of base ZMK 

9/12/2022 - Merge HID indicators pull request [#999](https://github.com/zmkfirmware/zmk/pull/999) atop of base ZMK

9/11/2022 - Diverge from base ZMK (Commit 6124d25)


### adv360-beta
This repository has been deprecated for a year and as such will not be documented, it is advisable to upgrade to V3.0 as this has more features and improved reliability
