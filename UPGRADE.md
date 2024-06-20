# Advantage 360 Pro ZMK upgrade guide

The last V2.0 update and the new V3.0 branch have introduced changes into the keymap files that causes merge conflicts for people updating with custom keymaps. This guide covers what changed, why it changed and how to fix it.

## What changed and why

To resolve issues some users were encountering with out of matrix keypresses, as well as to streamline the keymap for all future updates, several keys that are unused were removed from the keymap and [matrix transform](https://zmk.dev/docs/config/kscan#matrix-transform). Formatting was also standardised to fall in line with ZMK formatting conventions. As a result the board definition for the Advantage 360 Pro as it stands to get merged into ZMK main [here](https://github.com/zmkfirmware/zmk/pull/1454) matches the one in this repository to the greatest extent possible. 
These changes result in a merge conflict when two diverging git branches try to get added together in the updating procedure.
This sort of breaking change shouldn't happen again in the future.

## How to solve the merge conflict

In order to solve the merge conflict all that has to be done is for the conflicting key behaviours to be manually removed from two files.
- adv360.keymap

![The highlighted &none behaviours that need removing](/assets/keymap.jpg)
- keymap.json

![The highlighted &none behaviours that need removing](/assets/json.jpg)

These highlighted keys must be removed from each layer in both files. Be careful to preserve a comma in between every key behaviour in the keymap.json and at least one space between every behaviour in adv360.keymap or firmware builds will fail. The quotes need correctly preserving on the behaviours in keymap.json. Each behaviour needs to be wrapped in quotes. Whitespace within the quotes is ignored.
If you try to update your fork using the GitHub web interface you will see an error saying "This branch has merge conflicts and cannot be merged automatically" and you will be prompted to open a pull request instead. Solving the merge conflict this way is more challenging than doing it on GitHub desktop.

### Github Desktop 

This assumes you already have [GitHub desktop](https://desktop.github.com/) downloaded, installed and you have logged in using the GitHub credentials for your account. Whilst it would be helpful to have an alternative text editor such as VSCode installed this task can be completed with notepad 
1. Clone your repository

        Navigate in the menu to File->Clone repository. Your fork of the Adv360-Pro-ZMK repository should be visible in the menu of repositories to choose from. Click the blue "Clone" button
2. Open the folder

    Open the folder by using the "Show in your file manager" option and navigate to the "config" folder
3. Edit keymap.json

    Open keymap.json, and for each layer remove the 8 highlighted &none behaviours including the quotes wrapping them, and the commas
4. Edit adv 360.keymap

    Open adv360.keymap and remove the 8 highlighted &none behaviours in each layer
5. Commit your changes

    Returning to GitHub desktop you should see the changes you made in the bar on the left. Type an appropriate commit summary and click "Commit to *branch name*"

    ![The commit dialog of GitHub Desktop](/assets/commit.jpg)

6. Merge

    Navigate to Branch->Merge into current branch and select "upstream/V2.0" or "upstream/V3.0". You will see a warning that there will be two conflicted files. Click "Create a merge commit".

    ![The merge dialog showing a warning of conflicts](/assets/merge.jpg)

7. Resolve Conflicts

    The conflict resolution window has powerful options to soresolve the merge conflict, you will want to click on the down arrow next to "Open in *your text editor*" and click use the modified file from *your branch name*. In the case of this example it is called V2.0-beta. Using the file from upstream/V2.0 or upstream/V3.0 will result in none of your keymap changes being preserved. 
    Do this for both files then you will be able to click the "Continue Merge" option

    ![The merge dialog showing a warning of conflicts](/assets/conflict.jpg)
8. Push

    Once the merge is complete you should be able to click the "push origin" button in the top bar. At this point your changes should be uploaded to GitHub servers and the build should start
9. Test your firmware

    When the build succeeds download the uf2 files and flash them as normal. Test the keymap, if keys are shifted one way or the other it's likely you deleted too many or not enough behaviours. 